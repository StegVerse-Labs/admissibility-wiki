#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pages_build_verification_candidate.py"
BUILD_RECEIPT = ROOT / "reports" / "pages-build-receipt.json"
OUTPUT = ROOT / "reports" / "pages-build-verification-candidate.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def run_generator() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GENERATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        print("PAGES BUILD VERIFICATION CANDIDATE: FAIL")
        print(f"- missing {GENERATOR.relative_to(ROOT)}")
        return 1

    generator_text = GENERATOR.read_text(encoding="utf-8")
    for marker in (
        '"artifact_type": "pages_build_verification_candidate"',
        '"candidate_only": True',
        '"status_mutation_performed": False',
        '"deployment_authorized": False',
        '"public_verification_complete": False',
        '"release_authorized": False',
        '"downstream_propagation_authorized": False',
        '"PAGES_BUILD_PASS_ARTIFACT_PENDING"',
        '"FAIL_CLOSED"',
        '"REVIEW_REQUIRED"',
        '"candidate generation does not mutate canonical status"',
    ):
        if marker not in generator_text:
            failures.append(f"generator missing marker: {marker}")
    if "static/status/pages-build-verification.json" in generator_text:
        failures.append("candidate generator must not mutate canonical status")
    if "subprocess" in generator_text or "os.system" in generator_text:
        failures.append("candidate generator must not execute external commands")

    original_receipt = BUILD_RECEIPT.read_bytes() if BUILD_RECEIPT.exists() else None
    original_output = OUTPUT.read_bytes() if OUTPUT.exists() else None
    try:
        BUILD_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        BUILD_RECEIPT.write_text(json.dumps(valid_receipt(), indent=2) + "\n", encoding="utf-8")
        before = BUILD_RECEIPT.read_bytes()
        completed = run_generator()
        if completed.returncode != 0:
            failures.append(f"valid receipt generation failed: {completed.stdout.strip()}")
        elif not OUTPUT.exists():
            failures.append("valid receipt did not produce candidate")
        else:
            candidate = load(OUTPUT)
            if candidate.get("verification_state") != "PAGES_BUILD_PASS_ARTIFACT_PENDING":
                failures.append("valid receipt state mismatch")
            if candidate.get("candidate_only") is not True:
                failures.append("candidate-only boundary missing")
            if candidate.get("status_mutation_performed") is not False:
                failures.append("candidate claimed canonical mutation")
            if candidate.get("required_checks", {}).get("formalism_publication_validator", {}).get("status") != "REVIEW_REQUIRED":
                failures.append("formalism validator was inferred from build receipt")
            if candidate.get("required_checks", {}).get("pages_artifact_upload", {}).get("status") != "PENDING":
                failures.append("Pages artifact upload advanced without evidence")
            if BUILD_RECEIPT.read_bytes() != before:
                failures.append("generator mutated source build receipt")

        invalid = valid_receipt()
        invalid["build"]["step_outcome"] = "failure"
        invalid["build"]["state"] = "PAGES_BUILD_FAILED_OR_INCOMPLETE"
        BUILD_RECEIPT.write_text(json.dumps(invalid, indent=2) + "\n", encoding="utf-8")
        blocked = run_generator()
        if blocked.returncode == 0:
            failures.append("failed build receipt was accepted")
        elif not OUTPUT.exists():
            failures.append("failed build receipt did not produce fail-closed candidate")
        else:
            candidate = load(OUTPUT)
            if candidate.get("verification_state") != "FAIL_CLOSED":
                failures.append("failed receipt did not fail closed")
            if candidate.get("deployment_authorized") is not False:
                failures.append("failed candidate authorized deployment")
    finally:
        if original_receipt is None:
            BUILD_RECEIPT.unlink(missing_ok=True)
        else:
            BUILD_RECEIPT.write_bytes(original_receipt)
        if original_output is None:
            OUTPUT.unlink(missing_ok=True)
        else:
            OUTPUT.write_bytes(original_output)

    print("PAGES BUILD VERIFICATION CANDIDATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
