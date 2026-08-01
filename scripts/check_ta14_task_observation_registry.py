#!/usr/bin/env python3
"""Validate the TA-14 task observation registry.

This validator ensures that every issue has a repository location and a next
executable action, and that missing external evidence does not become a generic
development blocker or silently transfer ownership to StegVerse.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static/reviews/ta14/task-observation-registry.v0.1.json"

ALLOWED_STATES = {
    "BUILD_INTERNAL",
    "OBSERVE",
    "EVIDENCE_ABSENT_FAIL_CLOSED",
    "SIMULATED_ONLY",
    "VERIFIED_BOUNDED",
    "DISPUTED_REVIEWER_BURDEN",
    "COMPLETE",
}

ALLOWED_OWNERSHIP = {
    "STEGVERSE_OWNED",
    "SHARED_INTERFACE",
    "EXTERNAL_OWNER",
    "REVIEWER_BURDEN",
    "EVIDENCE_COORDINATION_ONLY",
    "OWNERSHIP_UNRESOLVED",
}

EXPECTED_IDS = {f"T14-{number:03d}" for number in range(1, 19)}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []

    require(REGISTRY.is_file(), f"missing registry: {REGISTRY}", failures)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    policy = data.get("policy", {})

    require(policy.get("external_tasks_exist") is False,
            "external_tasks_exist must be false", failures)
    require(policy.get("external_evidence_absence_blocks_only_bounded_claim") is True,
            "external evidence absence must block only the bounded claim", failures)
    require(policy.get("generic_blocked_state_prohibited") is True,
            "generic blocked state must be prohibited", failures)
    require(policy.get("silent_ownership_transfer_prohibited") is True,
            "silent ownership transfer must be prohibited", failures)

    tasks = data.get("tasks", [])
    ids = {task.get("id") for task in tasks}
    require(ids == EXPECTED_IDS,
            f"task coverage mismatch: expected {sorted(EXPECTED_IDS)}, got {sorted(ids)}",
            failures)

    for task in tasks:
        task_id = task.get("id", "UNKNOWN")
        state = task.get("state")
        ownership = task.get("ownership")
        task_file = task.get("task_file")
        implementation_paths = task.get("implementation_paths")
        observer_paths = task.get("observer_paths")
        next_action = task.get("next_action")
        claim_effect = task.get("claim_effect")

        require(state in ALLOWED_STATES,
                f"{task_id}: invalid state {state!r}", failures)
        require(state != "BLOCKED",
                f"{task_id}: generic BLOCKED state is prohibited", failures)
        require(ownership in ALLOWED_OWNERSHIP,
                f"{task_id}: invalid ownership {ownership!r}", failures)
        require(isinstance(task_file, str) and bool(task_file.strip()),
                f"{task_id}: missing task_file", failures)
        require(isinstance(implementation_paths, list) and bool(implementation_paths),
                f"{task_id}: missing implementation_paths", failures)
        require(isinstance(observer_paths, list) and bool(observer_paths),
                f"{task_id}: missing observer_paths", failures)
        require(isinstance(next_action, str) and bool(next_action.strip()),
                f"{task_id}: missing next executable action", failures)
        require(isinstance(claim_effect, str) and bool(claim_effect.strip()),
                f"{task_id}: missing bounded claim effect", failures)

        if ownership in {"EXTERNAL_OWNER", "OWNERSHIP_UNRESOLVED", "EVIDENCE_COORDINATION_ONLY"}:
            require(state in {
                "OBSERVE",
                "BUILD_INTERNAL",
                "EVIDENCE_ABSENT_FAIL_CLOSED",
                "SIMULATED_ONLY",
                "DISPUTED_REVIEWER_BURDEN",
                "VERIFIED_BOUNDED",
                "COMPLETE",
            }, f"{task_id}: external-origin evidence must remain observable and non-halting", failures)

        if state in {"OBSERVE", "EVIDENCE_ABSENT_FAIL_CLOSED", "SIMULATED_ONLY"}:
            forbidden = {"PROVEN", "CERTIFIED", "UNIVERSAL", "INDEPENDENTLY_VERIFIED"}
            require(not any(token in claim_effect for token in forbidden),
                    f"{task_id}: claim effect silently upgrades absent or simulated evidence",
                    failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(f"PASS: validated {len(tasks)} TA-14 tasks with repository locations and non-halting next actions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
