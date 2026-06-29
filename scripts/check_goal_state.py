#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL_STATE = ROOT / "docs" / "GOAL_STATE.json"

CURRENT_DONE_WHEN = [
    "all chain-status records are machine-verifiable",
    "all human-readable records match machine-readable state",
    "all automation manifests agree on the validation package",
    "the canonical workflow runs the full validator set",
    "the repository fails closed on drift",
]

PARALLEL_SAFE = [
    "framework registry draft",
    "framework manifest schema draft",
    "source/version citation fields",
    "overlap taxonomy draft",
    "SPE comparison test scaffolding",
    "transition-table mapping test scaffolding",
    "generated compatibility report template",
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
    if data.get("schema_version") != "1.0":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")

    current = data.get("current_goal", {})
    if current.get("goal_id") != "self-validating-governance-package":
        failures.append("current goal id mismatch")
    if current.get("status") != "COMPLETE":
        failures.append("current goal status mismatch")
    if current.get("completion_percent") != 100:
        failures.append("completion percent mismatch")
    if current.get("closure_result") != "SELF_VALIDATING_PACKAGE_COMPLETE":
        failures.append("closure result mismatch")
    for item in CURRENT_DONE_WHEN:
        if item not in current.get("done_when", []):
            failures.append(f"missing done criterion: {item}")

    next_goal = data.get("next_goal", {})
    if next_goal.get("goal_id") != "external-framework-compatibility-testbench":
        failures.append("next goal id mismatch")
    if next_goal.get("status") != "QUEUED_FOR_NEXT_ACTIVATION":
        failures.append("next goal status mismatch")
    if next_goal.get("initial_completion_percent_on_activation") != 0:
        failures.append("next goal reset mismatch")
    for item in PARALLEL_SAFE:
        if item not in next_goal.get("parallel_safe_before_activation", []):
            failures.append(f"missing parallel-safe item: {item}")

    boundary = data.get("boundary", {})
    for key in [
        "current_goal_does_not_activate_next_goal",
        "parallel_safe_work_must_not_destabilize_current_goal",
        "no_external_framework_validation_claim_yet",
        "next_goal_progress_reset_required",
    ]:
        if boundary.get(key) is not True:
            failures.append(f"boundary mismatch: {key}")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
