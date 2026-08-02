#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "static" / "status" / "session-consolidation-mindforge-public-anchor-2026-08-02.json"

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

EXPECTED_GOALS = {
    "MINDFORGE-BOUNDARY-001",
    "MINDFORGE-ATTRIBUTION-002",
    "MINDFORGE-PUBLICATION-003",
    "PUBLIC-ANCHOR-COORDINATION-004",
    "SESSION-CONSOLIDATION-005",
}


def fail(message: str) -> None:
    raise SystemExit(f"MINDFORGE PUBLIC-ANCHOR SESSION CONSOLIDATION: FAIL - {message}")


def require_path(path: str, label: str) -> None:
    candidate = ROOT / path
    if not candidate.exists():
        fail(f"{label} path missing: {path}")


def main() -> None:
    if not INVENTORY.exists():
        fail("inventory missing")
    try:
        data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

    if data.get("schema_version") != "session-consolidation-inventory.v1":
        fail("schema version mismatch")
    if data.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if data.get("branch") != "main":
        fail("branch mismatch")

    continuation = data.get("canonical_continuation", {})
    required_continuation = (
        "overall_handoff",
        "mindforge_handoff",
        "public_anchor_coordination",
        "public_anchor_reconstruction_handoff",
        "canonical_workflow",
        "canonical_aggregate",
    )
    for key in required_continuation:
        value = continuation.get(key)
        if not isinstance(value, str) or not value:
            fail(f"canonical continuation missing {key}")
        require_path(value, f"canonical continuation {key}")

    goals = data.get("session_goals", [])
    if not isinstance(goals, list) or len(goals) != 5:
        fail("exactly five session goals are required")
    observed_ids = {item.get("goal_id") for item in goals if isinstance(item, dict)}
    if observed_ids != EXPECTED_GOALS:
        fail("session goal inventory mismatch")

    for goal in goals:
        if not isinstance(goal, dict):
            fail("goal entry must be an object")
        goal_id = goal.get("goal_id")
        if goal.get("claim_state") not in ALLOWED_CLAIM_STATES:
            fail(f"invalid claim state for {goal_id}")
        for field in (
            "originating_goal",
            "destination",
            "branch",
            "owner",
            "completion_state",
            "validation_state",
            "integration_state",
            "archival_dependency",
            "next_action",
        ):
            if not goal.get(field):
                fail(f"goal {goal_id} missing {field}")
        locations = goal.get("locations", [])
        if not isinstance(locations, list) or not locations:
            fail(f"goal {goal_id} has no durable locations")
        for location in locations:
            require_path(location, f"goal {goal_id}")
        evidence = goal.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            fail(f"goal {goal_id} has no evidence")
        for evidence_path in evidence:
            if isinstance(evidence_path, str) and "/" in evidence_path and not evidence_path.startswith(("run:", "job:", "artifact:")):
                require_path(evidence_path, f"goal {goal_id} evidence")

    claims = data.get("active_claims", [])
    if not isinstance(claims, list) or len(claims) != 2:
        fail("exactly two machine-owned claims are required")
    for claim in claims:
        if claim.get("role") != "MACHINE_OWNED":
            fail(f"active claim {claim.get('task_id')} must be MACHINE_OWNED")
        for field in (
            "task_id",
            "originating_goal",
            "organization_repository",
            "branch",
            "claimant",
            "claim_timestamp",
            "expiration_or_release_condition",
            "expected_evidence",
            "collision_boundary",
            "next_task_after_release",
        ):
            if not claim.get(field):
                fail(f"active claim missing {field}")
        surfaces = claim.get("surfaces", [])
        if not isinstance(surfaces, list) or not surfaces:
            fail(f"active claim {claim.get('task_id')} has no surfaces")
        for surface in surfaces:
            require_path(surface, f"active claim {claim.get('task_id')}")

    released = data.get("released_session_claim", {})
    if released.get("prior_role") != "CLAIMED_FOR_IMPLEMENTATION_AND_VALIDATION":
        fail("released session claim prior role mismatch")
    if released.get("released_to") != "REPOSITORY_NATIVE_HANDOFFS_AND_MACHINE_OWNED_OBSERVERS":
        fail("released session claim destination mismatch")
    for field in (
        "task_id",
        "claim_timestamp",
        "release_timestamp",
        "release_condition_satisfied_by",
        "expected_next_evidence",
    ):
        if not released.get(field):
            fail(f"released session claim missing {field}")
    continuation_locations = released.get("continuation_locations", [])
    if not isinstance(continuation_locations, list) or len(continuation_locations) < 3:
        fail("released session claim continuation locations incomplete")
    for path in continuation_locations:
        require_path(path, "released session claim continuation")

    if data.get("archive_state") != "COMPLETE_ARCHIVE":
        fail("archive state must be COMPLETE_ARCHIVE")
    if data.get("archive_blockers") != []:
        fail("archive blockers must be empty")
    archive_evidence = data.get("archive_evidence", [])
    if not isinstance(archive_evidence, list) or len(archive_evidence) < 5:
        fail("archive evidence incomplete")

    metrics = data.get("completion_metrics", {})
    if metrics.get("task_completion") != {"complete_or_transferred": 5, "required": 5}:
        fail("task completion metric mismatch")
    if metrics.get("session_consolidation") != {"complete_or_transferred": 5, "required": 5}:
        fail("session consolidation metric mismatch")
    if metrics.get("archival_readiness_percent") != 100:
        fail("archival readiness must be 100")

    boundary = data.get("authority_boundary", {})
    for key in (
        "inventory_creates_execution_authority",
        "claim_creates_downstream_mutation_authority",
        "local_file_presence_establishes_validation",
        "session_transfer_establishes_activation",
        "archive_readiness_establishes_repository_completion",
        "publication_creates_execution_authority",
    ):
        if boundary.get(key) is not False:
            fail(f"authority boundary {key} must be false")

    print(
        "MINDFORGE PUBLIC-ANCHOR SESSION CONSOLIDATION: PASS - "
        "five goals are durable, two continuation claims are machine-owned, and the chat session owns no unique execution work"
    )


if __name__ == "__main__":
    main()
