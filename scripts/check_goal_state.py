#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL_STATE = ROOT / "docs" / "GOAL_STATE.json"

CURRENT_DONE_WHEN = [
    "framework registry exists and is machine-verifiable",
    "each framework has a manifest with source/version and allowed-use boundaries",
    "each framework maps claims and non-claims to SPE and ecosystem overlap fields",
    "transition-table mapping tests run for every listed framework",
    "generated compatibility reports are reproducible",
    "framework pages do not claim certification, endorsement, or execution authority",
    "the testbench fails closed on missing sources, stale versions, or undefined overlap",
]


def main() -> int:
    failures: list[str] = []

    if not GOAL_STATE.exists():
        print("GOAL STATE: FAIL")
        print("- missing docs/GOAL_STATE.json")
        return 1

    data = json.loads(GOAL_STATE.read_text(encoding="utf-8"))

    if data.get("artifact_type") != "goal_state":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "1.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")

    previous = data.get("previous_goal", {})
    if previous.get("goal_id") != "self-validating-governance-package":
        failures.append("previous goal id mismatch")
    if previous.get("status") != "COMPLETE":
        failures.append("previous goal status mismatch")
    if previous.get("completion_percent") != 100:
        failures.append("previous goal completion mismatch")
    if previous.get("closure_result") != "SELF_VALIDATING_PACKAGE_COMPLETE":
        failures.append("previous closure result mismatch")

    current = data.get("current_goal", {})
    if current.get("goal_id") != "external-framework-compatibility-testbench":
        failures.append("current goal id mismatch")
    if current.get("status") != "ACTIVE":
        failures.append("current goal status mismatch")
    if current.get("completion_percent") != 0:
        failures.append("current goal completion mismatch")
    for item in CURRENT_DONE_WHEN:
        if item not in current.get("done_when", []):
            failures.append(f"missing done criterion: {item}")

    boundary = data.get("boundary", {})
    for key in [
        "self_validating_package_remains_closed",
        "external_framework_testbench_active",
        "no_framework_certification_claim",
        "no_external_endorsement_claim",
        "no_execution_authority_claim",
        "testbench_outputs_are_compatibility_evidence_only",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"boundary mismatch: {key}")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
