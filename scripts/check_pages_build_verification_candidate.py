#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pages_build_verification_candidate.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"

GENERATOR_MARKERS = [
    '"artifact_type": "pages_build_verification_candidate"',
    '"candidate_only": True',
    '"deployment_authorized": False',
    '"public_verification_complete": False',
    '"PAGES_BUILD_PASS_ARTIFACT_PENDING"',
    '"FAIL_CLOSED"',
    '"candidate generation does not mutate canonical status"',
    '"observe_pages_artifact_upload_and_bind_artifact_id_and_digest"',
]
WORKFLOW_MARKERS = [
    "Generate Pages build verification candidate",
    "python scripts/generate_pages_build_verification_candidate.py",
    "reports/pages-build-verification-candidate.json",
    "name: pages-build-receipt",
]


def main() -> int:
    failures: list[str] = []
    for path in (GENERATOR, WORKFLOW, MIRROR):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    generator = GENERATOR.read_text(encoding="utf-8") if GENERATOR.exists() else ""
    workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.exists() else ""
    mirror = MIRROR.read_text(encoding="utf-8") if MIRROR.exists() else ""

    if generator:
        try:
            ast.parse(generator)
        except SyntaxError as exc:
            failures.append(f"generator syntax error: {exc}")

    for marker in GENERATOR_MARKERS:
        if marker not in generator:
            failures.append(f"generator missing marker: {marker}")
    for marker in WORKFLOW_MARKERS:
        if marker not in workflow:
            failures.append(f"workflow missing marker: {marker}")
    if workflow != mirror:
        failures.append("canonical and iOS workflow mirrors differ")

    write_index = workflow.find("python scripts/write_pages_build_receipt.py")
    candidate_index = workflow.find("python scripts/generate_pages_build_verification_candidate.py")
    upload_index = workflow.find("name: pages-build-receipt")
    enforce_index = workflow.find("Enforce Pages build result")
    if min(write_index, candidate_index, upload_index, enforce_index) >= 0:
        if not (write_index < candidate_index < upload_index < enforce_index):
            failures.append("candidate generation must occur after receipt writing and before artifact upload/enforcement")

    print("PAGES BUILD VERIFICATION CANDIDATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
