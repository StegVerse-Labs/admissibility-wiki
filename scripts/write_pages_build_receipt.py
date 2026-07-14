#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "pages-build-receipt.json"
BUILD_DIR = ROOT / "build"
CANDIDATE_GENERATOR = ROOT / "scripts" / "generate_pages_build_verification_candidate.py"
ROLLUP = ROOT / "static" / "status" / "canonical-workflow-observation-rollup.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_rollup_binding() -> dict:
    if not ROLLUP.exists():
        return {
            "state": "FAIL_CLOSED_ROLLUP_MISSING",
            "repository_path": str(ROLLUP.relative_to(ROOT)),
            "sha256": None,
            "terminal_envelope": None,
            "recursive_derivative_expansion_allowed": None,
            "completeness_state": None,
            "artifact_count": None,
            "present_count": None,
            "missing_count": None,
            "missing_artifact_ids": [],
            "manual_tasks_required": [],
            "user_action_required": False,
        }

    payload = json.loads(ROLLUP.read_text(encoding="utf-8"))
    valid_terminal = (
        payload.get("terminal_envelope") is True
        and payload.get("recursive_derivative_expansion_allowed") is False
        and payload.get("manual_tasks_required") == []
        and payload.get("user_action_required") is False
    )
    return {
        "state": "ROLLUP_BOUND" if valid_terminal else "FAIL_CLOSED_ROLLUP_INVALID",
        "repository_path": str(ROLLUP.relative_to(ROOT)),
        "sha256": sha256(ROLLUP),
        "schema": payload.get("schema"),
        "generated_at": payload.get("generated_at"),
        "public_endpoint": payload.get("public_endpoint"),
        "terminal_envelope": payload.get("terminal_envelope"),
        "recursive_derivative_expansion_allowed": payload.get("recursive_derivative_expansion_allowed"),
        "completeness_state": payload.get("completeness_state"),
        "artifact_count": payload.get("artifact_count"),
        "present_count": payload.get("present_count"),
        "missing_count": payload.get("missing_count"),
        "missing_artifact_ids": payload.get("missing_artifact_ids", []),
        "manual_tasks_required": [],
        "user_action_required": False,
    }


def main() -> int:
    build_outcome = os.environ.get("BUILD_OUTCOME", "unknown").strip().lower()
    build_present = BUILD_DIR.is_dir()
    files = sorted(path for path in BUILD_DIR.rglob("*") if path.is_file()) if build_present else []
    manifest_lines = [
        f"{path.relative_to(BUILD_DIR).as_posix()}\t{path.stat().st_size}\t{sha256(path)}"
        for path in files
    ]
    manifest_sha256 = hashlib.sha256(("\n".join(manifest_lines) + ("\n" if manifest_lines else "")).encode("utf-8")).hexdigest()

    rollup_binding = load_rollup_binding()
    success = (
        build_outcome == "success"
        and build_present
        and bool(files)
        and rollup_binding.get("state") == "ROLLUP_BOUND"
        and rollup_binding.get("completeness_state") == "COMPLETE_LOCAL_CHAIN"
    )
    receipt = {
        "artifact_type": "admissibility_wiki_pages_build_receipt",
        "schema_version": "0.2",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "workflow_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "job": os.environ.get("GITHUB_JOB"),
            "event_name": os.environ.get("GITHUB_EVENT_NAME"),
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "ref": os.environ.get("GITHUB_REF"),
            "sha": os.environ.get("GITHUB_SHA"),
        },
        "build": {
            "command": "npm run build",
            "step_outcome": build_outcome,
            "state": "PAGES_BUILD_COMPLETE" if success else "PAGES_BUILD_FAILED_OR_INCOMPLETE",
            "build_directory_present": build_present,
            "file_count": len(files),
            "total_size_bytes": sum(path.stat().st_size for path in files),
            "manifest_sha256": manifest_sha256,
        },
        "terminal_rollup_binding": rollup_binding,
        "deployment_requested": False,
        "deployment_completed": False,
        "public_verification_completed": False,
        "release_authorized": False,
        "manual_tasks_required": [],
        "user_action_required": False,
        "authority_boundary": {
            "pages_build_is_deployment_authority": False,
            "pages_build_is_public_verification": False,
            "pages_build_is_release_authority": False,
            "receipt_is_execution_authority": False,
            "rollup_binding_is_semantic_reclassification": False,
        },
        "required_next_transition": (
            "generate_verification_candidate_then_observe_pages_artifact_upload"
            if success
            else "repair_exact_build_or_rollup_failure_then_rebuild"
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        f"PAGES BUILD RECEIPT: {receipt['build']['state']} "
        f"rollup={rollup_binding.get('state')} -> {OUTPUT.relative_to(ROOT)}"
    )

    candidate_return_code = 1
    if CANDIDATE_GENERATOR.exists():
        completed = subprocess.run(
            [sys.executable, str(CANDIDATE_GENERATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip())
        candidate_return_code = completed.returncode
    else:
        print(f"PAGES BUILD VERIFICATION CANDIDATE: BLOCKED — missing {CANDIDATE_GENERATOR.relative_to(ROOT)}")

    return 0 if success and candidate_return_code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
