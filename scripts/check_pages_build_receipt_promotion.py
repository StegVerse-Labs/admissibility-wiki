#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMOTER = ROOT / "scripts" / "promote_pages_build_receipt.py"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run(receipt: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PROMOTER), "--receipt", str(receipt), "--output", str(output)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def valid_receipt() -> dict[str, Any]:
    return {
        "artifact_type": "admissibility_wiki_pages_build_receipt",
        "schema_version": "0.1",
        "generated_at_utc": "2026-07-13T00:00:00Z",
        "workflow_context": {
            "run_id": "123456",
            "run_attempt": "1",
            "workflow": "Validate chain continuation",
            "job": "build-pages",
            "event_name": "push",
            "repository": "StegVerse-Labs/admissibility-wiki",
            "ref": "refs/heads/main",
            "sha": "a" * 40,
        },
        "build": {
            "command": "npm run build",
            "step_outcome": "success",
            "state": "PAGES_BUILD_COMPLETE",
            "build_directory_present": True,
            "file_count": 10,
            "total_size_bytes": 1000,
            "manifest_sha256": "b" * 64,
        },
        "deployment_requested": False,
        "deployment_completed": False,
        "public_verification_completed": False,
        "release_authorized": False,
        "authority_boundary": {
            "pages_build_is_deployment_authority": False,
            "pages_build_is_public_verification": False,
            "pages_build_is_release_authority": False,
            "receipt_is_execution_authority": False,
        },
        "required_next_transition": "upload_pages_artifact_then_allow_separate_deployment_job",
    }


def main() -> int:
    failures: list[str] = []
    if not PROMOTER.exists():
        print("PAGES BUILD RECEIPT PROMOTION: FAIL")
        print(f"- missing {PROMOTER.relative_to(ROOT)}")
        return 1

    text = PROMOTER.read_text(encoding="utf-8")
    for marker in (
        "READY_FOR_PAGES_VERIFICATION_REVIEW",
        "BLOCKED_INVALID_BUILD_RECEIPT",
        "PAGES_BUILD_PASS_ARTIFACT_PENDING",
        '"status_mutation_performed": False',
        '"deployment_authorized": False',
        '"public_verification_complete": False',
        '"release_authorized": False',
        '"downstream_propagation_authorized": False',
    ):
        if marker not in text:
            failures.append(f"promoter missing marker: {marker}")

    with tempfile.TemporaryDirectory(prefix="pages-build-promotion-") as directory:
        temp = Path(directory)
        receipt = temp / "receipt.json"
        output = temp / "candidate.json"
        receipt.write_text(json.dumps(valid_receipt(), indent=2) + "\n", encoding="utf-8")
        before = receipt.read_bytes()

        completed = run(receipt, output)
        if completed.returncode != 0:
            failures.append(f"valid receipt promotion failed: {completed.stdout.strip()}")
        elif not output.exists():
            failures.append("valid receipt did not produce candidate")
        else:
            candidate = load(output)
            if candidate.get("candidate_state") != "READY_FOR_PAGES_VERIFICATION_REVIEW":
                failures.append("valid candidate state mismatch")
            if candidate.get("proposed_verification_state") != "PAGES_BUILD_PASS_ARTIFACT_PENDING":
                failures.append("valid proposed state mismatch")
            if candidate.get("status_mutation_performed") is not False:
                failures.append("candidate claimed status mutation")
            if candidate.get("required_checks", {}).get("pages_artifact_upload", {}).get("status") != "PENDING":
                failures.append("candidate advanced Pages artifact without evidence")
            if receipt.read_bytes() != before:
                failures.append("promoter mutated source receipt")

        invalid = valid_receipt()
        invalid["build"]["step_outcome"] = "failure"
        invalid["build"]["state"] = "PAGES_BUILD_FAILED_OR_INCOMPLETE"
        receipt.write_text(json.dumps(invalid, indent=2) + "\n", encoding="utf-8")
        blocked_output = temp / "blocked.json"
        blocked = run(receipt, blocked_output)
        if blocked.returncode == 0:
            failures.append("failed build receipt was accepted")
        elif not blocked_output.exists():
            failures.append("failed build receipt did not produce fail-closed candidate")
        else:
            candidate = load(blocked_output)
            if candidate.get("candidate_state") != "BLOCKED_INVALID_BUILD_RECEIPT":
                failures.append("failed receipt did not block")
            if candidate.get("proposed_verification_state") != "FAIL_CLOSED":
                failures.append("failed receipt did not propose FAIL_CLOSED")

    print("PAGES BUILD RECEIPT PROMOTION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
