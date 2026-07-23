#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build_selected_cedar_binary.py"
INSPECT = ROOT / "scripts" / "inspect_cedar_binary_build_receipt.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"
PATCH = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.patch.md"

REQUIRED_INSPECT_MARKERS = [
    "READY_FOR_REGISTRY_PROMOTION_REVIEW",
    "BLOCKED_BUILD_RECEIPT_INVALID",
    '"registry_mutation_performed": False',
    '"runtime_execution_requested": False',
    '"runtime_execution_authorized": False',
    '"authorization_decision_observed": False',
    '"external_consequence_allowed": False',
    "promotion_candidate_may_mutate_registry",
    "promotion_candidate_may_execute_binary",
]
REQUIRED_BUILD_MARKERS = [
    "inspect_cedar_binary_build_receipt.py",
    "CEDAR BUILD RECEIPT INSPECTION",
]
REQUIRED_WORKFLOW_MARKERS = [
    "build-selected-cedar-binary:",
    "python scripts/build_selected_cedar_binary.py",
    "cedar-selected-binary-build",
    "reports/external-frameworks/cedar-build",
]
FORBIDDEN = [
    'registry_mutation_performed": True',
    'runtime_execution_requested": True',
    'runtime_execution_authorized": True',
    'external_consequence_allowed": True',
]


def mirror_delta_is_controlled(workflow: str, mirror: str) -> bool:
    if workflow == mirror:
        return True
    return PATCH.exists() and "not activation evidence" in PATCH.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    for path in (BUILD, INSPECT, WORKFLOW, MIRROR):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    build_text = BUILD.read_text(encoding="utf-8") if BUILD.exists() else ""
    inspect_text = INSPECT.read_text(encoding="utf-8") if INSPECT.exists() else ""
    workflow_text = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.exists() else ""
    mirror_text = MIRROR.read_text(encoding="utf-8") if MIRROR.exists() else ""

    for marker in REQUIRED_INSPECT_MARKERS:
        if marker not in inspect_text:
            failures.append(f"inspection script missing marker: {marker}")
    for marker in REQUIRED_BUILD_MARKERS:
        if marker not in build_text:
            failures.append(f"build script missing chained inspection marker: {marker}")
    for marker in REQUIRED_WORKFLOW_MARKERS:
        if marker not in workflow_text:
            failures.append(f"workflow missing marker: {marker}")
    for marker in FORBIDDEN:
        if marker in inspect_text:
            failures.append(f"inspection script contains forbidden marker: {marker}")
    if not mirror_delta_is_controlled(workflow_text, mirror_text):
        failures.append("canonical and iOS workflow mirrors differ without controlled patch record")

    print("CEDAR BINARY PROMOTION AUTOMATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
