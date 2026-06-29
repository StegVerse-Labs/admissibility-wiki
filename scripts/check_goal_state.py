#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL_STATE = ROOT / "docs" / "GOAL_STATE.json"

CURRENT_DONE_WHEN = [
    "framework-page displayed evaluation status is generated from manifests and compatibility reports",
    "manual framework-page evaluation status editing is not required",
    "generated page-status blocks are non-authorizing",
    "workflow generates page-status blocks before validation and publication",
    "validator detects drift between generated page-status blocks and source reports",
    "framework narrative remains separable from generated status",
]

BUILT_SURFACES = [
    "framework page-status generator",
    "framework page-status validator",
    "canonical workflow page-status generation step",
    "canonical workflow page-status validation step",
    "iOS workflow mirror page-status generation step",
    "iOS workflow mirror page-status validation step",
    "workflow-manifest page-status declarations",
    "auto-state page-status declarations",
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
    if data.get("schema_version") != "3.2":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")

    previous_goals = data.get("previous_goals", [])
    if len(previous_goals) < 3:
        failures.append("missing previous goal closures")
    else:
        if previous_goals[0].get("closure_result") != "SELF_VALIDATING_PACKAGE_COMPLETE":
            failures.append("self-validating closure mismatch")
        if previous_goals[1].get("closure_result") != "TESTBENCH_COMPLETE_WITH_FAIL_CLOSED_UNRESOLVED_STATES":
            failures.append("testbench closure mismatch")
        if previous_goals[2].get("closure_result") != "EXPANSION_PIPELINE_GREEN_AND_SINGLE_WORKFLOW_CONFIRMED":
            failures.append("expansion closure mismatch")

    current = data.get("current_goal", {})
    if current.get("goal_id") != "declarative-external-framework-generation-pipeline":
        failures.append("current goal id mismatch")
    if current.get("status") != "ACTIVE":
        failures.append("current goal status mismatch")
    if current.get("completion_percent") != 18:
        failures.append("current goal completion mismatch")
    if current.get("cycle_status") != "PAGE_STATUS_GENERATION_DECLARED":
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
        "prior_expansion_cycle_remains_closed",
        "declarative_generation_pipeline_active",
        "no_framework_certification_claim",
        "no_external_endorsement_claim",
        "no_execution_authority_claim",
        "generated_reports_are_non_authorizing",
        "generated_framework_results_are_non_authorizing",
        "generated_framework_page_status_is_non_authorizing",
        "scheduled_validation_path_exists",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"boundary mismatch: {key}")
    if boundary.get("manual_task_required") is not False:
        failures.append("manual task boundary mismatch")
    if boundary.get("manual_framework_page_status_editing_required") is not False:
        failures.append("manual page-status boundary mismatch")
    if boundary.get("active_workflow_count") != 1:
        failures.append("active workflow count mismatch")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
