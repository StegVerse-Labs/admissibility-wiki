#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CAPTURE_ROOT = ROOT / "reports" / "external-frameworks" / "cedar"
OUTPUT_DIR = ROOT / "reports" / "external-frameworks" / "cedar-pipeline-summary"
OUTPUT = OUTPUT_DIR / "cedar-evidence-pipeline-status.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def artifact_record(path: Path) -> dict[str, Any]:
    return {
        "present": path.exists(),
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path) if path.exists() else None,
    }


def main() -> int:
    status_path = CAPTURE_ROOT / "cedar-capture-status.json"
    allow_path = CAPTURE_ROOT / "cedar-allow-capture.json"
    deny_path = CAPTURE_ROOT / "cedar-deny-capture.json"
    status = load_json(status_path)

    capture_validated = bool(status and status.get("overall_status") == "PASS")
    captures_present = allow_path.exists() and deny_path.exists()

    if capture_validated and captures_present:
        pipeline_state = "captured_unverified_validated"
    elif allow_path.exists() or deny_path.exists() or status_path.exists():
        pipeline_state = "artifacts_present_incomplete_or_unverified"
    else:
        pipeline_state = "artifacts_not_available"

    receipt = {
        "artifact_type": "external_framework_evidence_pipeline_status",
        "schema_version": "0.1",
        "framework_id": "cedar-policy",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "github_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "sha": os.environ.get("GITHUB_SHA"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "job": os.environ.get("GITHUB_JOB"),
            "runner_name": os.environ.get("RUNNER_NAME"),
            "runner_os": os.environ.get("RUNNER_OS"),
            "runner_arch": os.environ.get("RUNNER_ARCH"),
        },
        "pipeline_state": pipeline_state,
        "evidence_states": {
            "capture_artifacts_present": captures_present,
            "capture_artifacts_validated": capture_validated,
            "same_runner_replay_state": "not_performed",
            "fresh_runner_replay_state": "not_performed",
            "independent_implementation_or_provider_review": "not_performed",
            "compatibility_state": "not_claimed",
            "standing_state": "not_created",
            "execution_authority_state": "not_created",
        },
        "artifacts": {
            "allow_capture": artifact_record(allow_path),
            "deny_capture": artifact_record(deny_path),
            "capture_status": artifact_record(status_path),
        },
        "authority_boundary": {
            "pipeline_summary_is_execution_authority": False,
            "capture_validation_is_compatibility_proof": False,
            "implementation_selection_is_certification": False,
            "matching_decisions_create_stegverse_standing": False,
        },
        "limitations": [
            "No Cedar implementation is selected or pinned by this summary.",
            "Missing artifacts are reported as unavailable rather than inferred as success or failure.",
            "The summary does not create compatibility, delegation, standing, admissibility, certification, or execution authority.",
        ],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR EVIDENCE PIPELINE SUMMARY: {pipeline_state} -> {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
