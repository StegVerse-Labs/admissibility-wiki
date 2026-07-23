#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_selected_cedar_binary.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"
PATCH = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.patch.md"

REQUIRED_SCRIPT_MARKERS = [
    "0807ec154afd7ffa14a658c9955d25bfe12770ca",
    '["cargo", "build", "--locked", "--release", "-p", "cedar-policy-cli"]',
    "BUILT_HASHED_UNEXECUTED",
    '"executed_after_build": False',
    '"runtime_execution_authorized": False',
    '"external_consequence_allowed": False',
    "inspect_binary_build_receipt_then_attach_separate_authority_and_consequence_boundary_review",
]
REQUIRED_WORKFLOW_MARKERS = [
    "build-selected-cedar-binary:",
    "dtolnay/rust-toolchain@1.89.0",
    "python scripts/build_selected_cedar_binary.py",
    "cedar-selected-binary-build",
    "reports/external-frameworks/cedar-build",
]
FORBIDDEN_SCRIPT_MARKERS = [
    " cedar authorize ",
    "subprocess.run([binary",
    'runtime_execution_authorized": True',
    'external_consequence_allowed": True',
]


def mirror_delta_is_controlled(workflow: str, mirror: str) -> bool:
    if workflow == mirror:
        return True
    return PATCH.exists() and "not activation evidence" in PATCH.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    for path in [SCRIPT, WORKFLOW, MIRROR]:
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    script_text = SCRIPT.read_text(encoding="utf-8") if SCRIPT.exists() else ""
    workflow_text = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.exists() else ""
    mirror_text = MIRROR.read_text(encoding="utf-8") if MIRROR.exists() else ""

    for marker in REQUIRED_SCRIPT_MARKERS:
        if marker not in script_text:
            failures.append(f"build script missing marker: {marker}")
    for marker in FORBIDDEN_SCRIPT_MARKERS:
        if marker in script_text:
            failures.append(f"build script contains forbidden execution marker: {marker}")
    for marker in REQUIRED_WORKFLOW_MARKERS:
        if marker not in workflow_text:
            failures.append(f"workflow missing marker: {marker}")
    if not mirror_delta_is_controlled(workflow_text, mirror_text):
        failures.append("canonical and iOS workflow mirrors differ without controlled patch record")

    print("CEDAR SELECTED BINARY BUILD HARNESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
