#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACQUIRE = ROOT / "scripts/acquire_external_chat_activation_evidence.py"
SYNC = ROOT / "scripts/sync_external_chat_activation_evidence.py"
IMPORTER = ROOT / "scripts/import_external_chat_activation_evidence.py"
WORKFLOW = ROOT / ".github/workflows/validate-chain-continuation.yml"
IOS_WORKFLOW = ROOT / "iosnoperiod/github/workflows/validate-chain-continuation.yml"


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION SYNC CONTRACT: FAIL - {message}")
    return 1


def main() -> int:
    for path in (ACQUIRE, SYNC, IMPORTER, WORKFLOW, IOS_WORKFLOW):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    acquire = ACQUIRE.read_text(encoding="utf-8")
    sync = SYNC.read_text(encoding="utf-8")
    importer = IMPORTER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    ios_workflow = IOS_WORKFLOW.read_text(encoding="utf-8")

    required_acquire = (
        'OWNER = "StegVerse-Labs"',
        'REPO = "Site"',
        'WORKFLOW_NAME = "Site Task Runner"',
        'ARTIFACT_PREFIX = "external-chat-activation-evidence-"',
        'head_branch") == "main"',
        'conclusion") == "success"',
        'payload workflow_run_id does not match selected run',
        'payload commit_sha does not match selected run head_sha',
        'projection_written": False',
        '"state": "FAIL_CLOSED"',
    )
    for marker in required_acquire:
        if marker not in acquire:
            return fail(f"acquisition client missing marker: {marker}")

    required_sync = (
        'state == "FAIL_CLOSED"',
        'state == "SKIPPED"',
        'state != "ACQUIRED_EXACT_ARTIFACT"',
        'projected evidence hash drift',
        'provenance run identity drift',
        'provenance commit identity drift',
        'receipt["state"] = "IMPORTED_EXACT_ARTIFACT"',
    )
    for marker in required_sync:
        if marker not in sync:
            return fail(f"sync orchestrator missing marker: {marker}")

    for marker in (
        'payload.get("repository") != "StegVerse-Labs/Site"',
        'activation evidence SHA-256 mismatch',
        'mutation_required_disabled',
        'import_is_repository_mutation_authority": False',
        'import_is_publication_authority": False',
        'import_is_certification": False',
        'import_creates_standing": False',
    ):
        if marker not in importer:
            return fail(f"importer boundary missing marker: {marker}")

    workflow_markers = (
        "Sync External Chat activation evidence",
        "python scripts/sync_external_chat_activation_evidence.py",
        "Upload External Chat activation evidence intake",
        "reports/external-chat-activation-evidence-acquisition.json",
        "static/status/external-chat-activation-evidence*.json",
        "if: always()",
    )
    for marker in workflow_markers:
        if marker not in workflow:
            return fail(f"canonical workflow missing marker: {marker}")
        if marker not in ios_workflow:
            return fail(f"iOS workflow mirror missing marker: {marker}")

    if workflow != ios_workflow:
        return fail("canonical and iOS workflow mirror differ")

    print("EXTERNAL CHAT ACTIVATION SYNC CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
