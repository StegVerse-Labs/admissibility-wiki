#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "session-consolidation" / "discovery-governance-session-inventory.json"
CANONICAL_HANDOFF = ROOT / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
GOAL_HANDOFF = ROOT / "docs" / "DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md"
ORCHESTRATION = ROOT / "data" / "admissibility-wiki-orchestration-state.json"

ALLOWED_CLAIMS = {
    "UNCLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED", "BLOCKED", "COMPLETE",
    "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM",
}
REQUIRED_TASK_FIELDS = {
    "task_id", "originating_goal", "destination", "branch", "location",
    "owner", "claim_state", "completion_state", "validation_state",
    "integration_state", "archival_dependency", "evidence_location",
    "next_executable_action",
}


def main() -> int:
    failures: list[str] = []
    for path in (INVENTORY, CANONICAL_HANDOFF, GOAL_HANDOFF, ORCHESTRATION):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return report(failures)

    record = json.loads(INVENTORY.read_text(encoding="utf-8"))
    if record.get("record_type") != "session_consolidation_inventory":
        failures.append("record_type mismatch")
    if record.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repository mismatch")
    if record.get("branch") != "main":
        failures.append("branch must be main")
    if record.get("canonical_handoff") != "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md":
        failures.append("canonical handoff mismatch")
    if record.get("session_role") != "MERGED_INTO_CANONICAL_WORKSTREAM":
        failures.append("session role must be merged into canonical workstream")

    inventory = record.get("inventory")
    if not isinstance(inventory, list) or not inventory:
        failures.append("inventory must be a non-empty list")
        inventory = []
    task_ids: set[str] = set()
    for index, task in enumerate(inventory):
        missing = REQUIRED_TASK_FIELDS - set(task)
        if missing:
            failures.append(f"inventory[{index}] missing fields: {sorted(missing)}")
        task_id = task.get("task_id")
        if task_id in task_ids:
            failures.append(f"duplicate task_id: {task_id}")
        task_ids.add(task_id)
        if task.get("claim_state") not in ALLOWED_CLAIMS:
            failures.append(f"invalid claim state for {task_id}: {task.get('claim_state')}")
        if not task.get("owner"):
            failures.append(f"unassigned owner for {task_id}")
        if not task.get("location"):
            failures.append(f"unassigned location for {task_id}")
        if task.get("completion_state") == "BLOCKED_BUT_OBSERVED" and not task.get("release_condition"):
            failures.append(f"blocked task lacks machine-observable release condition: {task_id}")

    consolidation = record.get("session_consolidation", {})
    total = consolidation.get("total_session_goals")
    transferred = consolidation.get("transferred_or_complete")
    if total != len(inventory):
        failures.append("total_session_goals must equal inventory length")
    if transferred != total:
        failures.append("all session goals must be transferred or complete before archival")
    if consolidation.get("unique_chat_only_requirements_remaining") != 0:
        failures.append("chat-only requirements remain")
    if consolidation.get("session_execution_authority_remaining") is not False:
        failures.append("session execution authority must be released")
    if consolidation.get("archive_ready") is not True:
        failures.append("archive_ready must be true after complete transfer")

    convergence = record.get("convergence", {})
    if convergence.get("classification") != "MERGED_INTO_CANONICAL_WORKSTREAM":
        failures.append("convergence classification mismatch")
    if convergence.get("merged_into") != "StegVerse-Labs/admissibility-wiki/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md":
        failures.append("canonical merge location mismatch")
    if convergence.get("duplicate_execution_prohibited") is not True:
        failures.append("duplicate execution must be prohibited")

    active_claims = record.get("active_claims", [])
    for claim in active_claims:
        for field in (
            "task_id", "claimant", "role", "claim_timestamp",
            "claim_expiration_or_release_condition", "expected_evidence",
            "collision_boundaries", "next_task_after_release",
        ):
            if field not in claim:
                failures.append(f"active claim missing {field}")
        if claim.get("task_id") not in task_ids:
            failures.append(f"claim references unknown task: {claim.get('task_id')}")

    canonical_text = CANONICAL_HANDOFF.read_text(encoding="utf-8")
    if "complete thread is ready for archiving" not in canonical_text.lower():
        failures.append("canonical handoff does not preserve archive-ready posture")
    if "data/admissibility-wiki-orchestration-state.json" not in canonical_text:
        failures.append("canonical handoff lacks orchestration-state reference")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        print("DISCOVERY GOVERNANCE SESSION CONSOLIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE SESSION CONSOLIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
