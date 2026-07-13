#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACQUISITION = ROOT / "reports/external-chat-activation-evidence-acquisition.json"
SOURCE = ROOT / "reports/external-chat-activation-evidence-source.json"
PROJECTION = ROOT / "static/status/external-chat-activation-evidence.json"
PROVENANCE = ROOT / "static/status/external-chat-activation-evidence.provenance.json"


def run(script: str, *args: str) -> int:
    completed = subprocess.run(
        [sys.executable, script, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    return completed.returncode


def main() -> int:
    acquire_code = run("scripts/acquire_external_chat_activation_evidence.py")
    if not ACQUISITION.exists():
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL - acquisition receipt missing")
        return 1
    receipt = json.loads(ACQUISITION.read_text(encoding="utf-8"))
    state = receipt.get("state")
    if acquire_code != 0 or state == "FAIL_CLOSED":
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL_CLOSED - acquisition failed")
        return 1
    if state == "SKIPPED":
        print(f"EXTERNAL CHAT ACTIVATION SYNC: SKIP - {receipt.get('reason')}")
        return 0
    if state != "ACQUIRED_EXACT_ARTIFACT" or not SOURCE.exists():
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL - acquisition state/source mismatch")
        return 1

    import_code = run("scripts/import_external_chat_activation_evidence.py", str(SOURCE))
    if import_code != 0 or not PROJECTION.exists() or not PROVENANCE.exists():
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL_CLOSED - import or projection failed")
        return 1

    projection = json.loads(PROJECTION.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    if projection.get("evidence_sha256") != receipt.get("source_evidence_sha256"):
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL - projected evidence hash drift")
        return 1
    if provenance.get("source_workflow_run_id") != receipt.get("source_run_id"):
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL - provenance run identity drift")
        return 1
    if provenance.get("source_commit_sha") != receipt.get("source_commit_sha"):
        print("EXTERNAL CHAT ACTIVATION SYNC: FAIL - provenance commit identity drift")
        return 1

    receipt["state"] = "IMPORTED_EXACT_ARTIFACT"
    receipt["projection_written"] = True
    receipt["projected_path"] = str(PROJECTION.relative_to(ROOT))
    receipt["provenance_path"] = str(PROVENANCE.relative_to(ROOT))
    ACQUISITION.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        "EXTERNAL CHAT ACTIVATION SYNC: PASS - "
        f"run {receipt.get('source_run_id')} commit {receipt.get('source_commit_sha')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
