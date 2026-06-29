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
    "each framework page has explicit native terminology definitions",
    "terminology reconciliation classes are machine-verifiable",
    "transition-table mapping tests run for every listed framework",
    "generated compatibility reports are reproducible",
    "framework pages do not claim certification, endorsement, or execution authority",
    "the testbench fails closed on missing sources, stale versions, or undefined overlap",
]

BUILT_SURFACES = [
    "transition-table-based framework registry",
    "framework manifest schema",
    "registry validator",
    "normalized seed framework manifest",
    "framework manifest validator",
    "first complete compatibility report",
    "compatibility report validator",
    "canonical workflow manifest validation step",
    "iOS workflow mirror manifest validation step",
    "canonical workflow report validation step",
    "iOS workflow mirror report validation step",
    "source-blocked provisional framework manifest",
    "source-blocked compatibility report",
    "source-blocked registry state",
    "source-blocked manifest validation",
    "source-blocked report validation",
    "deterministic compatibility report generator",
    "report reproducibility verifier",
    "canonical workflow reproducibility validation step",
    "iOS workflow mirror reproducibility validation step",
    "all listed framework registry entries",
    "all listed framework compatibility manifests",
    "all listed framework compatibility reports",
    "governed terminology reconciliation rule",
    "terminology reconciliation glossary entry",
    "per-framework native term definition tables",
    "external framework terminology validator",
    "canonical workflow terminology validation step",
    "iOS workflow mirror terminology validation step",
    "auto-state terminology validation declaration",
    "auto-state report-generation validation declaration",
    "auto-state generator declaration",
    "explicit unresolved intake boundary",
]

UNRESOLVED_FINAL_INTAKE_STATES = [
    "source-blocked framework entries remain fail-closed until official sources exist",
    "artifact-package-required entries remain bounded to artifact-specific intake evidence",
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
    if data.get("schema_version") != "2.0":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")

    previous_goals = data.get("previous_goals", [])
    if not previous_goals:
        failures.append("missing previous goals")
    else:
        previous = previous_goals[0]
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
    if current.get("status") != "COMPLETE":
        failures.append("current goal status mismatch")
    if current.get("completion_percent") != 100:
        failures.append("current goal completion mismatch")
    if current.get("cycle_status") != "COMPLETE_WITH_EXPLICIT_UNRESOLVED_INTAKE":
        failures.append("cycle status mismatch")
    if current.get("closure_result") != "TESTBENCH_COMPLETE_WITH_FAIL_CLOSED_UNRESOLVED_STATES":
        failures.append("closure result mismatch")
    for item in CURRENT_DONE_WHEN:
        if item not in current.get("done_when", []):
            failures.append(f"missing done criterion: {item}")
    for item in BUILT_SURFACES:
        if item not in current.get("built_surfaces", []):
            failures.append(f"missing built surface: {item}")
    for item in UNRESOLVED_FINAL_INTAKE_STATES:
        if item not in current.get("unresolved_final_intake_states", []):
            failures.append(f"missing unresolved intake state: {item}")

    next_goal = data.get("next_goal", {})
    if next_goal.get("goal_id") != "external-framework-expansion-cycle":
        failures.append("next goal id mismatch")
    if next_goal.get("status") != "QUEUED_FOR_NEXT_ACTIVATION":
        failures.append("next goal status mismatch")
    if next_goal.get("initial_completion_percent_on_activation") != 0:
        failures.append("next goal reset mismatch")

    boundary = data.get("boundary", {})
    for key in [
        "self_validating_package_remains_closed",
        "external_framework_testbench_complete",
        "next_goal_not_activated",
        "no_framework_certification_claim",
        "no_external_endorsement_claim",
        "no_execution_authority_claim",
        "testbench_outputs_are_compatibility_evidence_only",
        "source_blocked_entries_fail_closed",
        "generated_reports_are_evidence_only",
        "declared_validation_package_aligned",
        "unresolved_intake_states_are_non_authorizing",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"boundary mismatch: {key}")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
