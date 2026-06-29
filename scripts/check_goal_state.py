#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL_STATE = ROOT / "docs" / "GOAL_STATE.json"

CURRENT_DONE_WHEN = [
    "expansion intake rules exist and are machine-verifiable",
    "new framework entries require a source state before report generation",
    "source-recorded frameworks receive generated compatibility reports",
    "source-blocked frameworks remain fail-closed",
    "artifact-package-required frameworks remain bounded to artifact-specific intake",
    "new framework pages include native terminology definitions",
    "the expansion cycle preserves all prior non-authority boundaries",
]

BUILT_SURFACES = [
    "expansion policy",
    "expansion policy validator",
    "canonical workflow expansion-policy validation step",
    "iOS workflow mirror expansion-policy validation step",
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
    if data.get("schema_version") != "2.2":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")

    previous_goals = data.get("previous_goals", [])
    if len(previous_goals) < 2:
        failures.append("missing previous goal closures")
    else:
        if previous_goals[0].get("closure_result") != "SELF_VALIDATING_PACKAGE_COMPLETE":
            failures.append("self-validating closure mismatch")
        if previous_goals[1].get("closure_result") != "TESTBENCH_COMPLETE_WITH_FAIL_CLOSED_UNRESOLVED_STATES":
            failures.append("testbench closure mismatch")

    current = data.get("current_goal", {})
    if current.get("goal_id") != "external-framework-expansion-cycle":
        failures.append("current goal id mismatch")
    if current.get("status") != "ACTIVE":
        failures.append("current goal status mismatch")
    if current.get("completion_percent") != 12:
        failures.append("current goal completion mismatch")
    if current.get("cycle_status") != "EXPANSION_CONTROL_SURFACE_ACTIVE":
        failures.append("cycle status mismatch")
    for item in CURRENT_DONE_WHEN:
        if item not in current.get("done_when", []):
            failures.append(f"missing done criterion: {item}")
    for item in BUILT_SURFACES:
        if item not in current.get("built_surfaces", []):
            failures.append(f"missing built surface: {item}")
    if not current.get("next_required_action"):
        failures.append("missing next required action")

    boundary = data.get("boundary", {})
    for key in [
        "prior_testbench_remains_closed",
        "external_framework_expansion_cycle_active",
        "no_framework_certification_claim",
        "no_external_endorsement_claim",
        "no_execution_authority_claim",
        "testbench_outputs_are_compatibility_evidence_only",
        "source_blocked_entries_fail_closed",
        "unresolved_intake_states_are_non_authorizing",
        "expansion_policy_is_non_authorizing",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"boundary mismatch: {key}")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
