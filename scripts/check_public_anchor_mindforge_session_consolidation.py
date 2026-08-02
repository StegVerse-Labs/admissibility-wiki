#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/session-consolidation/public-anchor-mindforge-session-consolidation.md"
STATUS = ROOT / "static/status/public-anchor-mindforge-session-consolidation.json"
REQUIRED_PATHS = (
    "ADMISSIBILITY_MIRROR_HANDOFF.md",
    "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    "docs/WIKI_PUBLICATION_PIPELINE_MIRROR_HANDOFF.md",
    "docs/WIKI_PUBLIC_ANCHOR_TASK_MESH_HANDOFF.md",
    "docs/WIKI_PUBLIC_ANCHOR_ACTIVATION_COORDINATION.md",
    "docs/external-frameworks/mindforge.md",
    "static/status/wiki-public-anchor-task-mesh-registry.json",
    "static/status/wiki-public-anchor-internal-task-registry.json",
    "scripts/run_wiki_public_anchor_internal_tasks.py",
    "scripts/run_wiki_public_anchor_task_mesh.py",
    "scripts/run_wiki_public_anchor_completion_cycles.py",
    "scripts/check_wiki_public_anchor_completion_cycles.py",
)
REQUIRED_DOC_MARKERS = (
    "MERGED_INTO_CANONICAL_WORKSTREAM",
    "unique_chat_only_requirements_remaining: 0",
    "session_specific_claims_remaining: 0",
    "originating_conversation_required_for_future_execution: false",
    "There are no unspecified external tasks.",
    "docs/WIKI_PUBLICATION_PIPELINE_MIRROR_HANDOFF.md",
    "static/status/wiki-public-anchor-task-mesh-registry.json",
    "docs/external-frameworks/mindforge.md",
)


def fail(messages: list[str]) -> int:
    print("PUBLIC-ANCHOR MINDFORGE SESSION CONSOLIDATION: FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def main() -> int:
    failures: list[str] = []
    if not DOC.exists():
        failures.append(f"missing {DOC.relative_to(ROOT)}")
    if not STATUS.exists():
        failures.append(f"missing {STATUS.relative_to(ROOT)}")
    if failures:
        return fail(failures)

    text = DOC.read_text(encoding="utf-8")
    for marker in REQUIRED_DOC_MARKERS:
        if marker not in text:
            failures.append(f"consolidation document missing marker: {marker}")

    try:
        status = json.loads(STATUS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail([f"invalid status JSON: {exc}"])

    if status.get("schema_version") != "session-consolidation.v1":
        failures.append("schema version mismatch")
    if status.get("state") != "MERGED_INTO_CANONICAL_WORKSTREAM":
        failures.append("state must be MERGED_INTO_CANONICAL_WORKSTREAM")
    if status.get("unique_chat_only_requirements_remaining") != 0:
        failures.append("chat-only requirements remain")
    if status.get("originating_conversation_required_for_future_execution") is not False:
        failures.append("future execution still depends on the conversation")
    if status.get("unresolved_work_is_repository_owned") is not True:
        failures.append("unresolved work is not fully repository-owned")

    claims = status.get("claims", {})
    if claims.get("implementation") != "RELEASED":
        failures.append("implementation claim not released")
    if claims.get("validation") != "RELEASED_TO_MACHINE_OWNER":
        failures.append("validation claim not transferred")
    if claims.get("integration") != "RELEASED_TO_CANONICAL_WORKSTREAM":
        failures.append("integration claim not transferred")

    inventory = status.get("inventory")
    if not isinstance(inventory, list) or len(inventory) != 9:
        failures.append("inventory must contain exactly 9 durable task records")
    else:
        ids = set()
        for index, item in enumerate(inventory):
            if not isinstance(item, dict):
                failures.append(f"inventory[{index}] is not an object")
                continue
            task_id = item.get("task_id")
            if not task_id or task_id in ids:
                failures.append(f"inventory[{index}] has missing or duplicate task_id")
            ids.add(task_id)
            for field in (
                "goal", "destination", "branch", "location", "owner",
                "claim_state", "completion_state", "validation_state",
                "integration_state", "evidence", "next_action",
            ):
                if not item.get(field):
                    failures.append(f"{task_id or index} missing {field}")
            if "archival_dependency" not in item:
                failures.append(f"{task_id or index} missing archival_dependency")

    loss = status.get("archive_loss_test", {})
    for key in (
        "goal_inventory_preserved",
        "exact_locations_preserved",
        "claims_released_or_transferred",
        "machine_observers_assigned",
        "release_conditions_preserved",
    ):
        if loss.get(key) is not True:
            failures.append(f"archive-loss test failed: {key}")
    if loss.get("deleting_chat_impairs_execution") is not False:
        failures.append("archive-loss test says deleting chat impairs execution")

    boundary = status.get("authority_boundary", {})
    for key in (
        "session_archival_completes_workstream",
        "session_archival_grants_publication",
        "session_archival_grants_certification",
        "session_archival_grants_execution_authority",
    ):
        if boundary.get(key) is not False:
            failures.append(f"authority boundary {key} must be false")

    for path in REQUIRED_PATHS:
        if not (ROOT / path).exists():
            failures.append(f"missing canonical continuation path: {path}")

    if failures:
        return fail(failures)

    print("PUBLIC-ANCHOR MINDFORGE SESSION CONSOLIDATION: PASS - 13 session goals are complete or durably transferred; no future execution requires chat history")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
