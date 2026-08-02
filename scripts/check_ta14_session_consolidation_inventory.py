#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "static/reviews/ta14/session-consolidation-inventory.v0.1.json"
REQUIRED_TASK_IDS = {f"TA14-GOAL-{index:03d}" for index in range(1, 9)}
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
ARCHIVE_SAFE_SESSION_ROLES = {
    "MERGED_INTO_CANONICAL_WORKSTREAM",
    "COMPLETE_ARCHIVE",
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

    if payload.get("schema_version") not in {"0.1.0", "0.2.0", "0.3.0"}:
        return fail("schema_version must be one of 0.1.0, 0.2.0, or 0.3.0")
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

    archival_dependencies = []
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
        if goal.get("archival_dependency") is True:
            archival_dependencies.append(goal)
            if not goal.get("release_condition"):
                return fail(f"{task_id} archival dependency missing release_condition")

    convergence = payload.get("convergence")
    if not isinstance(convergence, dict) or not convergence.get("canonical_workstream"):
        return fail("convergence must name canonical_workstream")

    observation = payload.get("current_observation")
    if observation is not None:
        if not isinstance(observation, dict):
            return fail("current_observation must be an object")
        for key in ("workflow", "run_id", "run_number", "status", "development_halt"):
            if key not in observation:
                return fail(f"current_observation missing {key}")
        if observation.get("development_halt") is not False:
            return fail("current_observation must preserve development_halt=false")

    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        return fail("metrics must be an object")
    required_metric_keys = {
        "required_tasks", "complete_or_implemented_tasks", "required_developed_files",
        "developed_files", "scaffolding_or_stubs", "missing_required_files",
        "required_validations", "validated", "required_integrations", "integrated",
        "session_goals", "transferred_or_complete", "goal_activation_percent",
        "archival_ready",
    }
    if not required_metric_keys.issubset(metrics):
        return fail("metrics missing required denominator fields")
    if metrics.get("required_tasks") != len(goals):
        return fail("required_tasks must equal number of goals")
    if metrics.get("session_goals") != len(goals):
        return fail("session_goals must equal number of goals")
    if metrics.get("transferred_or_complete") != len(goals):
        return fail("all session goals must be durably transferred before this inventory can pass")

    archival_ready = metrics.get("archival_ready") is True
    session_role = payload.get("session_role")
    if archival_ready:
        if session_role not in ARCHIVE_SAFE_SESSION_ROLES:
            return fail("archival_ready requires an archive-safe session_role")
        if payload.get("unique_session_work_remaining") is not False:
            return fail("archival_ready requires unique_session_work_remaining=false")
        if not payload.get("archive_receipt"):
            return fail("archival_ready requires archive_receipt")
        for goal in archival_dependencies:
            if goal.get("claim_state") not in {
                "MACHINE_OWNED", "BLOCKED", "CLAIMED_FOR_IMPLEMENTATION",
                "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION",
                "MERGED_INTO_CANONICAL_WORKSTREAM", "COMPLETE", "SUPERSEDED",
            }:
                return fail(f"{goal.get('task_id')} is not durably owned for archival transfer")

    archive_conditions = payload.get("archive_conditions")
    if not isinstance(archive_conditions, list) or not archive_conditions:
        return fail("archive_conditions must be a nonempty list")

    print(
        "TA-14 SESSION CONSOLIDATION INVENTORY: PASS - "
        f"goals={len(goals)} transferred={metrics['transferred_or_complete']} "
        f"archival_ready={str(archival_ready).lower()} external_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
