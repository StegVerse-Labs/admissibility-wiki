#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def record(path: Path) -> dict[str, Any]:
    return {
        "present": path.exists(),
        "path": str(path.relative_to(ROOT)) if path.exists() else str(path),
        "sha256": sha256(path) if path.exists() else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a reusable external-command evidence pipeline without inferring execution success.")
    parser.add_argument("--framework-id", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--validation-status", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    receipt_path = Path(args.receipt).resolve()
    status_path = Path(args.validation_status).resolve()
    output_path = Path(args.output).resolve()
    receipt = load(receipt_path)
    status = load(status_path)

    capture_present = receipt is not None
    capture_validated = bool(status and status.get("overall_status") == "PASS")
    if capture_validated:
        pipeline_state = "captured_unverified_validated"
    elif capture_present or status is not None:
        pipeline_state = "artifacts_present_incomplete_or_unverified"
    else:
        pipeline_state = "artifacts_not_available"

    summary = {
        "artifact_type": "external_framework_evidence_pipeline_status",
        "schema_version": "0.1",
        "framework_id": args.framework_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "github_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "sha": os.environ.get("GITHUB_SHA"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "runner_name": os.environ.get("RUNNER_NAME"),
            "runner_os": os.environ.get("RUNNER_OS"),
            "runner_arch": os.environ.get("RUNNER_ARCH"),
        },
        "pipeline_state": pipeline_state,
        "evidence_states": {
            "capture_artifact_present": capture_present,
            "capture_artifact_validated": capture_validated,
            "capture_state": receipt.get("capture_state") if receipt else "not_available",
            "same_runner_replay": "not_performed",
            "fresh_runner_replay": "not_performed",
            "independent_implementation_or_provider_review": "not_performed",
            "compatibility_state": "not_claimed",
            "standing_state": "not_created",
            "execution_authority_state": "not_created",
        },
        "artifacts": {
            "capture_receipt": record(receipt_path),
            "validation_status": record(status_path),
        },
        "authority_boundary": {
            "pipeline_summary_is_execution_authority": False,
            "protocol_response_is_stegverse_standing": False,
            "validated_capture_is_compatibility_proof": False,
            "validated_capture_creates_delegation": False,
        },
        "limitations": [
            "The summary reports artifact availability and structural validation only.",
            "No replay, independent implementation review, compatibility, standing, delegation, admissibility, certification, or execution authority is inferred.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"COMMAND EVIDENCE PIPELINE SUMMARY: {pipeline_state} -> {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
