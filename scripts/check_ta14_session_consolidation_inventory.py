#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "static/reviews/ta14/session-consolidation-inventory.v0.1.json"
REQUIRED_TASK_IDS = {f"TA14-GOAL-{index:03d}" for index in range(1, 9)}
ALLOWED_SCHEMA_VERSIONS = {"0.1.0", "0.2.0"}
ALLOWED_CLAIM_STATES = {
    "UNCLAIMED",
    "CLAIMED_FOR_IMPLEMENTATION",
    "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION",
    "MACHINE_OWNED",
    "BLOCKED",
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}


def fail(message: str) -> int:
    print(f"TA-14 SESSION CONSOLIDATION INVENTORY: FAIL - {message}")
    return 1


def main() -> int:
    if not INVENTORY.exists():
        return fail(f"missing inventory: {INVENTORY.relative_to(ROOT)}")

    try:
        payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"invalid JSON: {exc}")

    if payload.get("schema_version") not in ALLOWED_SCHEMA_VERSIONS:
        return fail(f"schema_version must be one of {sorted(ALLOWED_SCHEMA_VERSIONS)}")
    if payload.get("goal_id") != "TA14-RECIPROCAL-REVIEW-LAYER":
        return fail("unexpected goal_id")

    continuation = payload.get("canonical_continuation")
    if not isinstance(continuation, dict):
        return fail("canonical_continuation must be an object")
    for key in ("repository", "branch", "pull_request", "handoff", "task_registry", "status", "workflow_observation"):
        if not continuation.get(key):
            return fail(f"canonical_continuation missing {key}")

    goals = payload.get("goals")
    if not isinstance(goals, list):
        return fail("goals must be a list")
    ids = {goal.get("task_id") for goal in goals if isinstance(goal, dict)}
    if ids != REQUIRED_TASK_IDS:
        return fail(f"expected goal IDs {sorted(REQUIRED_TASK_IDS)}, found {sorted(ids)}")

    for goal in goals:
        if not isinstance(goal, dict):
            return fail("every goal must be an object")
        task_id = goal.get("task_id")
        for key in (
            "goal", "destination", "branch", "location", "owner", "claim_state",
            "completion_state", "validation_state", "integration_state",
            "archival_dependency", "evidence", "next_action",
        ):
            if key not in goal or goal.get(key) in (None, ""):
                return fail(f"{task_id} missing {key}")
        if goal.get("claim_state") not in ALLOWED_CLAIM_STATES:
            return fail(f"{task_id} has invalid claim_state {goal.get('claim_state')}")
        if "external" in str(goal.get("owner", "")).lower():
            return fail(f"{task_id} owner must not be an unspecified external task")
        if goal.get("claim_state") == "BLOCKED" and not goal.get("release_condition"):
            return fail(f"{task_id} BLOCKED without machine-observable release_condition")

    convergence = payload.get("convergence")
    if not isinstance(convergence, dict) or not convergence.get("canonical_workstream"):
        return fail("convergence must name canonical_workstream")

    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        return fail("metrics must be an object")
    required_metric_keys = {
        "required_tasks", "complete_or_implemented_tasks", "required_developed_files",
        "developed_files", "scaffolding_or_stubs", "missing_required_files",
        "required_validations", "validated", "required_integrations", "integrated",
        "session_goals", "transferred_or_complete", "goal_activation_percent", "archival_ready",
    }
    if not required_metric_keys.issubset(metrics):
        return fail("metrics missing required denominator fields")
    if metrics.get("required_tasks") != len(goals):
        return fail("required_tasks must equal number of goals")
    if metrics.get("session_goals") != len(goals):
        return fail("session_goals must equal number of goals")
    if metrics.get("transferred_or_complete") != len(goals):
        return fail("all session goals must be durably transferred before this inventory can pass")
    if metrics.get("archival_ready") is True:
        return fail("inventory may not claim archival readiness while archival dependencies remain")

    current_observation = payload.get("current_observation")
    if payload.get("schema_version") == "0.2.0":
        if not isinstance(current_observation, dict):
            return fail("schema 0.2.0 requires current_observation")
        for key in ("workflow", "run_id", "run_number", "status", "development_halt"):
            if key not in current_observation:
                return fail(f"current_observation missing {key}")
        if current_observation.get("development_halt") is not False:
            return fail("current_observation must preserve development_halt=false")

    archive_conditions = payload.get("archive_conditions")
    if not isinstance(archive_conditions, list) or not archive_conditions:
        return fail("archive_conditions must be a nonempty list")

    print(
        "TA-14 SESSION CONSOLIDATION INVENTORY: PASS - "
        f"schema={payload['schema_version']} goals={len(goals)} "
        f"transferred={metrics['transferred_or_complete']} "
        f"archival_ready={str(metrics['archival_ready']).lower()} external_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
