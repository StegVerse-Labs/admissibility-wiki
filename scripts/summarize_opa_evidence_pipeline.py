#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAPTURE_ROOT = ROOT / "reports" / "summary-input" / "capture"
DEFAULT_REPLAY_ROOT = ROOT / "reports" / "summary-input" / "fresh-runner"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "opa-pipeline-summary" / "opa-evidence-pipeline-status.json"
COMPATIBILITY_RUNNER = ROOT / "scripts" / "run_opa_governance_compatibility.py"
COMPATIBILITY_RECEIPT_NAME = "opa-stegverse-governance-compatibility-receipt.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_json(root: Path, filename: str) -> Path | None:
    if not root.exists():
        return None
    matches = sorted(root.rglob(filename))
    return matches[0] if matches else None


def load_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def artifact_record(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {"present": False, "path": None, "sha256": None}
    try:
        shown = str(path.relative_to(ROOT))
    except ValueError:
        shown = str(path)
    return {"present": True, "path": shown, "sha256": sha256(path)}


def run_compatibility() -> tuple[str, str]:
    if not COMPATIBILITY_RUNNER.exists():
        return "BLOCKED_MISSING_RUNNER", "compatibility runner is missing"
    completed = subprocess.run(
        [sys.executable, str(COMPATIBILITY_RUNNER)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout.rstrip()
    if output:
        print(output)
    if completed.returncode != 0:
        return "FAILED", output or f"runner exited {completed.returncode}"
    return "OBSERVED", output


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize bounded OPA capture and replay evidence.")
    parser.add_argument("--capture-root", default=str(DEFAULT_CAPTURE_ROOT))
    parser.add_argument("--replay-root", default=str(DEFAULT_REPLAY_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    capture_root = Path(args.capture_root).resolve()
    replay_root = Path(args.replay_root).resolve()
    output = Path(args.output).resolve()

    capture_status_path = find_json(capture_root, "opa-capture-status.json")
    same_runner_receipt_path = find_json(capture_root, "opa-replay-receipt.json")
    fresh_runner_receipt_path = find_json(replay_root, "opa-independent-replay-receipt.json")

    capture_status = load_json(capture_status_path)
    same_runner_receipt = load_json(same_runner_receipt_path)
    fresh_runner_receipt = load_json(fresh_runner_receipt_path)

    capture_validated = bool(
        capture_status
        and (
            capture_status.get("validation_status") == "PASS"
            or capture_status.get("overall_status") == "PASS"
        )
    )
    same_runner_confirmed = bool(
        same_runner_receipt
        and same_runner_receipt.get("replay_state") == "replay_confirmed_same_environment"
    )
    fresh_runner_confirmed = bool(
        fresh_runner_receipt
        and fresh_runner_receipt.get("replay_state") == "replay_confirmed_independent_environment"
    )

    compatibility_execution_state = "NOT_RUN"
    compatibility_output = ""
    if fresh_runner_confirmed and capture_validated and same_runner_confirmed:
        compatibility_execution_state, compatibility_output = run_compatibility()

    compatibility_receipt_path = find_json(replay_root, COMPATIBILITY_RECEIPT_NAME)
    compatibility_receipt = load_json(compatibility_receipt_path)
    compatibility_observed = bool(
        compatibility_execution_state == "OBSERVED"
        and compatibility_receipt
        and compatibility_receipt.get("summary", {}).get("bounded_compatibility_state")
        == "GOVERNANCE_COMPATIBILITY_OBSERVED"
        and compatibility_receipt.get("summary", {}).get("all_expected_results_matched") is True
    )

    if fresh_runner_confirmed and capture_validated and same_runner_confirmed and compatibility_observed:
        pipeline_state = "governance_compatibility_observed"
    elif fresh_runner_confirmed and capture_validated and same_runner_confirmed:
        pipeline_state = "fresh_runner_replay_confirmed_compatibility_pending_or_failed"
    elif capture_validated and same_runner_confirmed:
        pipeline_state = "same_runner_replay_confirmed_fresh_runner_pending"
    elif capture_status_path or same_runner_receipt_path or fresh_runner_receipt_path:
        pipeline_state = "artifacts_present_incomplete_or_unverified"
    else:
        pipeline_state = "artifacts_not_available"

    receipt = {
        "artifact_type": "external_framework_evidence_pipeline_status",
        "schema_version": "0.2",
        "framework_id": "opa",
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
            "capture_artifacts_present": capture_status_path is not None,
            "capture_artifacts_validated": capture_validated,
            "same_runner_replay_confirmed": same_runner_confirmed,
            "fresh_runner_replay_confirmed": fresh_runner_confirmed,
            "governance_compatibility_execution": compatibility_execution_state,
            "governance_compatibility_observed": compatibility_observed,
            "independent_implementation_or_provider_review": "not_performed",
            "compatibility_state": "bounded_observed" if compatibility_observed else "not_claimed",
            "standing_state": "not_created",
            "execution_authority_state": "not_created",
        },
        "artifacts": {
            "capture_status": artifact_record(capture_status_path),
            "same_runner_replay_receipt": artifact_record(same_runner_receipt_path),
            "fresh_runner_replay_receipt": artifact_record(fresh_runner_receipt_path),
            "governance_compatibility_receipt": artifact_record(compatibility_receipt_path),
        },
        "compatibility_runner_output": compatibility_output,
        "authority_boundary": {
            "pipeline_summary_is_execution_authority": False,
            "fresh_runner_replay_is_independent_implementation": False,
            "fresh_runner_replay_is_independent_provider_review": False,
            "matching_outputs_create_stegverse_standing": False,
            "bounded_compatibility_is_general_compatibility": False,
            "compatibility_receipt_grants_execution_authority": False,
        },
        "limitations": [
            "A fresh GitHub Actions runner is a separate execution environment within the same repository and provider.",
            "Missing artifacts are reported as unavailable rather than inferred as success or failure.",
            "The deterministic StegVerse evaluator is a compatibility fixture, not a production SPE deployment.",
            "A bounded compatibility observation applies only to the pinned implementation, policy, inputs, mappings, cases, and commit-time conditions.",
            "The summary does not create delegation, standing, admissibility, certification, general compatibility, or execution authority.",
        ],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    try:
        shown = output.relative_to(ROOT)
    except ValueError:
        shown = output
    print(f"OPA EVIDENCE PIPELINE SUMMARY: {pipeline_state} -> {shown}")
    if compatibility_execution_state == "FAILED":
        return 1
    if compatibility_execution_state == "BLOCKED_MISSING_RUNNER":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
