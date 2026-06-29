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
    "every registry entry has a deterministic generated compatibility report",
    "CI evidence is recorded as green or fail-closed before cycle closure",
    "manual task state is false",
    "scheduled validation path exists",
    "only one active workflow exists",
    "workflow selection task is removed",
]

BUILT_SURFACES = [
    "expansion policy",
    "expansion policy validator",
    "canonical workflow expansion-policy validation step",
    "iOS workflow mirror expansion-policy validation step",
    "report coverage validator",
    "canonical workflow report coverage validation step",
    "iOS workflow mirror report coverage validation step",
    "auto-state report coverage declaration",
    "workflow-manifest report coverage declaration",
    "first expansion framework page",
    "first expansion framework manifest",
    "first expansion framework compatibility report",
    "first expansion framework registry entry",
    "second expansion framework page",
    "second expansion framework manifest",
    "second expansion framework compatibility report",
    "second expansion framework registry entry",
    "third expansion framework page",
    "third expansion framework manifest",
    "third expansion framework compatibility report",
    "third expansion framework registry entry",
    "all-entry report reproducibility validator",
    "CI evidence state record",
    "CI evidence validator",
    "canonical workflow CI evidence validation step",
    "iOS workflow mirror CI evidence validation step",
    "auto-state CI evidence declaration",
    "workflow-manifest CI evidence declaration",
    "non-manual CI evidence boundary",
    "single active workflow policy",
    "workflow sprawl validator",
    "extra active workflows removed",
    "extra iOS mirror workflow files removed",
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
    if data.get("schema_version") != "3.0":
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
    if current.get("completion_percent") != 96:
        failures.append("current goal completion mismatch")
    if current.get("cycle_status") != "SINGLE_ACTIVE_WORKFLOW_POLICY_RECORDED":
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
        "generated_reports_are_non_authorizing",
        "missing_ci_evidence_fails_closed",
        "scheduled_validation_path_exists",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"boundary mismatch: {key}")
    if boundary.get("manual_task_required") is not False:
        failures.append("manual task boundary mismatch")
    if boundary.get("manual_workflow_selection_required") is not False:
        failures.append("workflow selection boundary mismatch")
    if boundary.get("active_workflow_count") != 1:
        failures.append("active workflow count mismatch")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
