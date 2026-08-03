#!/usr/bin/env python3
"""Validate the durable session-consolidation inventory for wiki publication."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = (
    ROOT
    / "data"
    / "session-consolidation"
    / "admissibility-wiki-publication-session-inventory.v1.json"
)
HANDOFF = ROOT / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
RELEASED_SESSION_OWNER = "publication-session-validation-lane-released"

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

REQUIRED_GOAL_FIELDS = {
    "goal_id",
    "originating_session_goal",
    "destination_organization",
    "destination_repository",
    "branch",
    "location",
    "current_owner",
    "claim_state",
    "completion_state",
    "validation_state",
    "integration_state",
    "archival_dependency",
    "evidence_location",
    "next_executable_action",
}


def fail(message: str) -> None:
    raise SystemExit(f"PUBLICATION SESSION CONSOLIDATION: FAIL - {message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing inventory: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail("inventory root must be an object")
    return value


def require_nonempty_string(record: dict[str, Any], field: str, label: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} missing non-empty {field}")
    return value.strip()


def main() -> int:
    inventory = load_json(INVENTORY)

    if inventory.get("schema") != "stegverse.session-consolidation-inventory.v1":
        fail("unexpected schema")
    if inventory.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository identity mismatch")
    if inventory.get("branch") != "main":
        fail("canonical branch must remain main")
    if inventory.get("archive_state") != "COMPLETE_ARCHIVE_READY":
        fail("archive state is not complete")

    active_goal = inventory.get("active_goal")
    if not isinstance(active_goal, dict):
        fail("active_goal must be an object")
    for field in (
        "goal_id",
        "description",
        "originating_session_goal",
        "canonical_continuation",
        "canonical_workflow",
        "current_role",
        "claimant",
        "claim_created_at",
        "claim_released_at",
        "claim_release_condition",
    ):
        require_nonempty_string(active_goal, field, "active_goal")

    if active_goal["canonical_continuation"] != (
        "StegVerse-Labs/admissibility-wiki/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
    ):
        fail("canonical continuation must point to the root mirror handoff")
    if active_goal["canonical_workflow"] != (
        ".github/workflows/validate-chain-continuation.yml"
    ):
        fail("canonical workflow identity mismatch")
    if active_goal["current_role"] != "COMPLETE":
        fail("session goal must be complete before archival")
    if active_goal["claimant"] != RELEASED_SESSION_OWNER:
        fail("released claimant identity mismatch")
    release_condition = active_goal["claim_release_condition"]
    for marker in (
        "SATISFIED",
        "30841948608",
        "CAT evidence validator",
        "CAT landing-page marker step",
    ):
        if marker not in release_condition:
            fail(f"release condition missing evidence marker: {marker}")

    goals = inventory.get("session_goals")
    if not isinstance(goals, list) or not goals:
        fail("session_goals must be a non-empty array")

    goal_ids: set[str] = set()
    session_claims = 0
    external_claims = 0
    for index, goal in enumerate(goals):
        if not isinstance(goal, dict):
            fail(f"session_goals[{index}] must be an object")
        missing = sorted(REQUIRED_GOAL_FIELDS - set(goal))
        if missing:
            fail(f"session_goals[{index}] missing fields: {', '.join(missing)}")
        for field in REQUIRED_GOAL_FIELDS:
            require_nonempty_string(goal, field, f"session_goals[{index}]")

        goal_id = goal["goal_id"]
        if goal_id in goal_ids:
            fail(f"duplicate goal_id: {goal_id}")
        goal_ids.add(goal_id)

        claim_state = goal["claim_state"]
        if claim_state not in ALLOWED_CLAIM_STATES:
            fail(f"unsupported claim state for {goal_id}: {claim_state}")

        owner = goal["current_owner"]
        dependency = goal["archival_dependency"]
        if claim_state.startswith("CLAIMED_FOR_"):
            if "publication-session-validation-lane" in owner:
                session_claims += 1
            else:
                external_claims += 1
                if "NONE_FOR_THIS_SESSION" not in dependency:
                    fail(f"external claim must release this session: {goal_id}")

        if owner.strip().lower() in {"unknown", "tbd", "none"}:
            fail(f"goal has no durable owner: {goal_id}")
        if goal["next_executable_action"].strip().lower() in {"unknown", "tbd", "later"}:
            fail(f"goal has no executable next action: {goal_id}")
        if claim_state in {"MACHINE_OWNED", "MERGED_INTO_CANONICAL_WORKSTREAM"}:
            if "NONE_FOR_THIS_SESSION" not in dependency:
                fail(f"transferred goal must release this session: {goal_id}")
        if goal_id in {"AWP-PUB-001", "AWP-CI-002"}:
            if claim_state != "COMPLETE":
                fail(f"session-owned claim not released: {goal_id}")
            if "NONE_FOR_THIS_SESSION" not in dependency:
                fail(f"completed session goal still blocks archival: {goal_id}")

    required_goal_ids = {
        "AWP-PUB-001",
        "AWP-CI-002",
        "AWP-RIVERBRAID-003",
        "AWP-HIL-004",
        "AWP-FORMALISM-005",
        "AWP-VALIDATION-006",
    }
    if goal_ids != required_goal_ids:
        missing = sorted(required_goal_ids - goal_ids)
        unexpected = sorted(goal_ids - required_goal_ids)
        fail(f"goal inventory drift; missing={missing}, unexpected={unexpected}")
    if session_claims != 0:
        fail(f"session claims remain active: {session_claims}")
    if external_claims != 1:
        fail(f"expected exactly one preserved external implementation claim, found {external_claims}")

    policy = inventory.get("claim_policy")
    if not isinstance(policy, dict):
        fail("claim_policy must be an object")
    if set(policy.get("allowed_claim_states", [])) != ALLOWED_CLAIM_STATES:
        fail("allowed claim states drift")
    for boolean_field in (
        "one_active_owner_per_workload",
        "stale_claim_release_required",
    ):
        if policy.get(boolean_field) is not True:
            fail(f"claim policy must enable {boolean_field}")
    for false_field in (
        "missing_evidence_is_success",
        "cross_repository_authority_inferred",
    ):
        if policy.get(false_field) is not False:
            fail(f"claim policy must keep {false_field}=false")

    completion = inventory.get("completion_inventory")
    if not isinstance(completion, dict):
        fail("completion_inventory must be an object")
    integer_fields = (
        "required_session_goals",
        "transferred_or_complete_session_goals",
        "required_files_for_session_goal",
        "developed_files",
        "scaffolding_or_stubs",
        "missing_required_files",
        "required_validation_gates",
        "validated_gates",
        "required_integration_bindings",
        "integrated_bindings",
        "task_completion_percent",
        "developed_files_percent",
        "validation_percent",
        "integration_percent",
        "propagation_percent",
        "goal_activation_percent",
        "session_consolidation_percent",
    )
    for field in integer_fields:
        if not isinstance(completion.get(field), int):
            fail(f"completion_inventory.{field} must be an integer")
    if completion["required_session_goals"] != len(goals):
        fail("required_session_goals does not match inventory length")
    if completion["transferred_or_complete_session_goals"] != len(goals):
        fail("all session goals must be durably transferred or complete")
    if completion["developed_files"] != completion["required_files_for_session_goal"]:
        fail("developed file inventory is incomplete")
    if completion["scaffolding_or_stubs"] != 0 or completion["missing_required_files"] != 0:
        fail("session deliverables still contain stubs or missing files")
    if completion["validated_gates"] != completion["required_validation_gates"]:
        fail("session validation gates are incomplete")
    if completion["integrated_bindings"] != completion["required_integration_bindings"]:
        fail("session integration bindings are incomplete")
    for field in (
        "task_completion_percent",
        "developed_files_percent",
        "validation_percent",
        "integration_percent",
        "propagation_percent",
        "goal_activation_percent",
        "session_consolidation_percent",
    ):
        if completion[field] != 100:
            fail(f"archive-complete percentage must equal 100: {field}")

    archive_conditions = inventory.get("archive_conditions")
    if not isinstance(archive_conditions, list) or len(archive_conditions) < 4:
        fail("archive_conditions must preserve all release gates")
    for item in archive_conditions:
        if not isinstance(item, str) or not item.startswith("SATISFIED:"):
            fail("archive condition is not satisfied")

    archive_evidence = inventory.get("archive_evidence")
    if not isinstance(archive_evidence, dict):
        fail("archive_evidence must be an object")
    expected_evidence = {
        "run_id": 30841948608,
        "head_sha": "ac2e4f75dbe046cfbd42da62156e7959679096a0",
        "validation_job": 91781047986,
        "build_pages_job": 91781631840,
        "deploy_pages_job": 91782075870,
        "verify_public_pages_job": 91782126780,
        "canonical_prescan_artifact": 8867141195,
        "full_validation_artifact": 8867206490,
        "pages_build_receipt_artifact": 8867258088,
        "github_pages_artifact": 8867259392,
    }
    for field, expected in expected_evidence.items():
        if archive_evidence.get(field) != expected:
            fail(f"archive evidence mismatch: {field}")
    require_nonempty_string(archive_evidence, "claims_released_at", "archive_evidence")

    authority = inventory.get("authority")
    if not isinstance(authority, dict) or not authority:
        fail("authority boundary missing")
    if any(value is not False for value in authority.values()):
        fail("session inventory must not grant authority")

    if not HANDOFF.is_file():
        fail("canonical mirror handoff is missing")
    if not WORKFLOW.is_file():
        fail("canonical workflow is missing")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    if "Verify CAT governance stack publication" not in workflow_text:
        fail("canonical workflow does not verify the session-specific public marker")
    if "schedule:" in workflow_text.split("jobs:", 1)[0]:
        fail("canonical workflow must remain event driven")

    print(
        "PUBLICATION SESSION CONSOLIDATION: PASS - "
        f"goals={len(goals)} session_claims={session_claims} "
        f"external_claims={external_claims} archive_state={inventory['archive_state']}"
    )
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
