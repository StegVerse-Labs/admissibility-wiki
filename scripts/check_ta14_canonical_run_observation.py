#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/status/ta14-canonical-run-observation.json"


def fail(message: str) -> None:
    raise SystemExit(f"TA-14 CANONICAL RUN OBSERVATION: FAIL - {message}")


def main() -> int:
    if not STATUS.exists():
        fail(f"missing {STATUS.relative_to(ROOT)}")

    payload = json.loads(STATUS.read_text(encoding="utf-8"))
    observed = payload.get("observed_run")
    layer = payload.get("ta14_layer_result")
    policy = payload.get("policy")
    next_task = payload.get("next_ta14_task")

    if not isinstance(observed, dict) or observed.get("run_id") != 30715224273:
        fail("observed canonical run identity is missing or unexpected")
    if observed.get("conclusion") != "failure":
        fail("receipt must preserve the observed repository failure")
    if not isinstance(layer, dict):
        fail("missing bounded TA-14 layer result")
    if layer.get("task_registry_validator") != "PASS":
        fail("task registry validator pass not preserved")
    if layer.get("observation_fixture_validator") != "PASS":
        fail("observation fixture validator pass not preserved")
    if layer.get("development_halt") is not False:
        fail("development_halt must remain false")
    if layer.get("state") != "BOUNDED_LAYER_VALIDATION_PASS_REPOSITORY_ACTIVATION_FAIL_CLOSED":
        fail("bounded layer/repository activation distinction is missing")

    failures = payload.get("repository_failures_outside_ta14_layer")
    if not isinstance(failures, list) or not failures:
        fail("repository failures are not mapped to located internal tasks")
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

    if not isinstance(next_task, dict) or not next_task.get("location") or not next_task.get("action"):
        fail("next TA-14 task lacks a repository location or action")

    print(
        "TA-14 CANONICAL RUN OBSERVATION: PASS - "
        f"run={observed['run_id']} repository={observed['conclusion']} "
        f"layer={layer['state']} development_halt=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
