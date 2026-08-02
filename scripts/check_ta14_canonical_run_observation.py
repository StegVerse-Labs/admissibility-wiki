#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/status/ta14-canonical-run-observation.json"
ALLOWED_LAYER_STATES = {
    "BOUNDED_LAYER_VALIDATION_PASS_REPOSITORY_ACTIVATION_FAIL_CLOSED",
    "TA14_CORE_PASS_SUPPORT_VALIDATORS_FAIL_CLOSED",
}


def fail(message: str) -> None:
    raise SystemExit(f"TA-14 CANONICAL RUN OBSERVATION: FAIL - {message}")


def main() -> int:
    if not STATUS.exists():
        fail(f"missing {STATUS.relative_to(ROOT)}")

    payload = json.loads(STATUS.read_text(encoding="utf-8"))
    observed = payload.get("observed_run")
    layer = payload.get("ta14_layer_result")
    policy = payload.get("policy")
    next_tasks = payload.get("next_ta14_tasks")
    if next_tasks is None:
        single = payload.get("next_ta14_task")
        next_tasks = [single] if isinstance(single, dict) else None

    if not isinstance(observed, dict):
        fail("observed canonical run is missing")
    if not isinstance(observed.get("run_id"), int) or observed.get("run_id") <= 0:
        fail("observed canonical run_id must be a positive integer")
    if not isinstance(observed.get("run_number"), int) or observed.get("run_number") <= 0:
        fail("observed canonical run_number must be a positive integer")
    if not observed.get("commit") or not observed.get("workflow"):
        fail("observed canonical run must bind workflow and commit")
    if observed.get("conclusion") not in {"failure", "success"}:
        fail("observed canonical run conclusion must be success or failure")

    if not isinstance(layer, dict):
        fail("missing bounded TA-14 layer result")
    if layer.get("task_registry_validator") != "PASS":
        fail("task registry validator pass not preserved")
    if layer.get("observation_fixture_validator") != "PASS":
        fail("observation fixture validator pass not preserved")
    if layer.get("development_halt") is not False:
        fail("development_halt must remain false")
    if layer.get("state") not in ALLOWED_LAYER_STATES:
        fail("bounded layer/repository activation distinction is missing")

    failures = payload.get("repository_failures_outside_ta14_bounded_checks")
    if failures is None:
        failures = payload.get("repository_failures_outside_ta14_layer")
    if observed.get("conclusion") == "failure" and (not isinstance(failures, list) or not failures):
        fail("repository failures are not mapped to located internal tasks")
    if isinstance(failures, list):
        for item in failures:
            if not isinstance(item, dict):
                fail("repository failure record must be an object")
            if not item.get("task_id") or not item.get("location") or not item.get("state"):
                fail("repository failure record lacks task_id, location, or state")
            if item.get("state") == "BLOCKED":
                fail(f"generic BLOCKED state prohibited: {item.get('task_id')}")

    if not isinstance(policy, dict) or policy.get("external_tasks") != []:
        fail("external_tasks must be an empty list")
    if policy.get("ta14_development_continues_after_repository_failure") is not True:
        fail("non-halting continuation policy is absent")
    if policy.get("repository_activation_requires_full_canonical_pass") is not True:
        fail("repository activation boundary is weakened")

    if not isinstance(next_tasks, list) or not next_tasks:
        fail("next TA-14 tasks are missing")
    for task in next_tasks:
        if not isinstance(task, dict) or not task.get("location") or not task.get("action"):
            fail("next TA-14 task lacks a repository location or action")

    print(
        "TA-14 CANONICAL RUN OBSERVATION: PASS - "
        f"run={observed['run_id']} repository={observed['conclusion']} "
        f"layer={layer['state']} development_halt=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
