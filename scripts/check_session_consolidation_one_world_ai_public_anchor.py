#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "static" / "status" / "session-consolidation-one-world-ai-public-anchor-2026-08-02.json"


def fail(message: str) -> None:
    raise SystemExit(f"SESSION CONSOLIDATION INVENTORY: FAIL - {message}")


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
    for key in ("overall_handoff", "coordination_record", "owned_track_handoff", "canonical_workflow"):
        value = continuation.get(key)
        if not isinstance(value, str) or not value:
            fail(f"canonical continuation missing {key}")
        if not (ROOT / value).exists():
            fail(f"canonical continuation path missing: {value}")

    goals = data.get("session_goals", [])
    if not isinstance(goals, list) or len(goals) != 4:
        fail("exactly four session goals are required")
    goal_ids = {item.get("goal_id") for item in goals if isinstance(item, dict)}
    expected = {
        "OWAI-INTAKE-001",
        "PUBLIC-ANCHOR-FREEZE-002",
        "PUBLIC-ANCHOR-INVITE-003",
        "PUBLIC-ANCHOR-ACTIVATE-004",
    }
    if goal_ids != expected:
        fail("session goal inventory mismatch")

    allowed_claim_states = {
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
    for goal in goals:
        if not isinstance(goal, dict):
            fail("goal entry must be an object")
        if goal.get("claim_state") not in allowed_claim_states:
            fail(f"invalid claim state for {goal.get('goal_id')}")
        locations = goal.get("locations", [])
        if not locations:
            fail(f"goal {goal.get('goal_id')} has no durable locations")
        for location in locations:
            if not (ROOT / location).exists():
                fail(f"goal location missing: {location}")
        if not goal.get("next_action"):
            fail(f"goal {goal.get('goal_id')} has no next executable action")

    claim = data.get("active_claim", {})
    if claim.get("role") != "CLAIMED_FOR_VALIDATION":
        fail("active role must remain CLAIMED_FOR_VALIDATION")
    if not claim.get("claim_timestamp"):
        fail("active claim timestamp missing")
    if not claim.get("release_condition"):
        fail("active claim release condition missing")
    if not claim.get("collision_boundary"):
        fail("active claim collision boundary missing")
    for location in claim.get("files", []):
        if not (ROOT / location).exists():
            fail(f"claimed file missing: {location}")

    if data.get("archive_state") != "ACTIVE_DISTINCT_SUPPORT_ROLE":
        fail("archive state must remain ACTIVE_DISTINCT_SUPPORT_ROLE until claim release")
    blockers = data.get("archive_blockers", [])
    if not isinstance(blockers, list) or len(blockers) < 2:
        fail("archive blockers must remain explicit")

    boundary = data.get("authority_boundary", {})
    for key in (
        "inventory_creates_execution_authority",
        "claim_creates_downstream_mutation_authority",
        "local_file_presence_establishes_validation",
        "session_transfer_establishes_activation",
    ):
        if boundary.get(key) is not False:
            fail(f"authority boundary {key} must be false")

    print("SESSION CONSOLIDATION INVENTORY: PASS - goals, claims, continuation paths, and archive blockers are durable")


if __name__ == "__main__":
    main()
