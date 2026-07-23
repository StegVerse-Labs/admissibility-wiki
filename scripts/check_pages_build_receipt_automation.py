#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_pages_build_receipt.py"
GENERATOR = ROOT / "scripts" / "generate_pages_build_verification_candidate.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"
PATCH = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.patch.md"

WRITER_MARKERS = [
    "admissibility_wiki_pages_build_receipt", "PAGES_BUILD_COMPLETE",
    "PAGES_BUILD_FAILED_OR_INCOMPLETE", '"deployment_requested": False',
    '"deployment_completed": False', '"public_verification_completed": False',
    '"release_authorized": False', "pages_build_is_deployment_authority",
    "generate_verification_candidate_then_observe_pages_artifact_upload",
    "generate_pages_build_verification_candidate.py", "candidate_return_code",
    "repair_build_failure_and_rebuild_before_deployment",
]
GENERATOR_MARKERS = [
    '"artifact_type": "pages_build_verification_candidate"',
    '"candidate_only": True', '"status_mutation_performed": False',
    '"deployment_authorized": False', '"PAGES_BUILD_PASS_ARTIFACT_PENDING"',
    '"FAIL_CLOSED"',
]
WORKFLOW_MARKERS = [
    "id: site-build", "continue-on-error: true",
    "BUILD_OUTCOME: ${{ steps.site-build.outcome }}",
    "python scripts/write_pages_build_receipt.py", "name: pages-build-receipt",
    "path: reports/pages-build-receipt.json", "Enforce Pages build result",
]


def mirror_delta_is_controlled(workflow: str, mirror: str) -> bool:
    if workflow == mirror:
        return True
    return PATCH.exists() and "not activation evidence" in PATCH.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    for path in (WRITER, GENERATOR, WORKFLOW, MIRROR):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    writer = WRITER.read_text(encoding="utf-8") if WRITER.exists() else ""
    generator = GENERATOR.read_text(encoding="utf-8") if GENERATOR.exists() else ""
    workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.exists() else ""
    mirror = MIRROR.read_text(encoding="utf-8") if MIRROR.exists() else ""
    for marker in WRITER_MARKERS:
        if marker not in writer:
            failures.append(f"writer missing marker: {marker}")
    for marker in GENERATOR_MARKERS:
        if marker not in generator:
            failures.append(f"generator missing marker: {marker}")
    for marker in WORKFLOW_MARKERS:
        if marker not in workflow:
            failures.append(f"workflow missing marker: {marker}")
    if not mirror_delta_is_controlled(workflow, mirror):
        failures.append("canonical and iOS workflow mirrors differ without controlled patch record")
    build_index = workflow.find("id: site-build")
    receipt_index = workflow.find("python scripts/write_pages_build_receipt.py")
    upload_index = workflow.find("name: pages-build-receipt")
    enforce_index = workflow.find("Enforce Pages build result")
    pages_upload_index = workflow.find("Upload Pages artifact")
    if min(build_index, receipt_index, upload_index, enforce_index, pages_upload_index) >= 0:
        if not (build_index < receipt_index < upload_index < enforce_index < pages_upload_index):
            failures.append("Pages receipt steps are not ordered fail-closed before Pages artifact upload")
    if "static/status/pages-build-verification.json" in generator:
        failures.append("candidate generator must not mutate canonical verification status")
    print("PAGES BUILD RECEIPT AUTOMATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
