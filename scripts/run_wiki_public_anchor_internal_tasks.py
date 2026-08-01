#!/usr/bin/env python3
"""Execute the Wiki public-anchor internal task queue without global stalling.

Each leaf task observer runs independently. A failed observer is recorded for its task
and does not prevent later independent tasks from running. Aggregate/self-referential
tasks are not recursively invoked; they are recorded as DEFERRED_SELF_OBSERVATION and
are evaluated by the canonical caller after this executor returns.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static" / "status" / "wiki-public-anchor-internal-task-registry.json"
REPORT = ROOT / "reports" / "wiki-public-anchor-internal-task-execution.json"

# PA-INT-002 invokes this executor through the multi-docket aggregate.
# PA-INT-007 is the canonical aggregate and is evaluated by its caller.
# PA-INT-009 points directly back to this executor.
# Running any of them from inside this queue would recurse and could halt development.
DEFERRED_AGGREGATE_TASK_IDS = {"PA-INT-002", "PA-INT-007", "PA-INT-009"}
RUNNABLE_STATES = {"READY_INTERNAL", "ACTIVE_INTERNAL"}


def load_registry() -> dict[str, Any]:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("registry must contain a JSON object")
    return value


def run_observer(task: dict[str, Any]) -> dict[str, Any]:
    task_id = task["task_id"]
    observer = task["observer"]
    observer_path = ROOT / observer

    if task_id in DEFERRED_AGGREGATE_TASK_IDS or observer_path.resolve() == Path(__file__).resolve():
        return {
            "task_id": task_id,
            "state": "DEFERRED_SELF_OBSERVATION",
            "observer": observer,
            "exit_code": None,
            "output": "Aggregate or self-referential observer is evaluated by the canonical caller after the internal executor returns.",
        }

    if not observer_path.exists():
        return {
            "task_id": task_id,
            "state": "BLOCKED_MISSING_OBSERVER",
            "observer": observer,
            "exit_code": None,
            "output": f"Missing observer: {observer}",
        }

    result = subprocess.run(
        [sys.executable, str(observer_path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {
        "task_id": task_id,
        "state": "PASS_INTERNAL" if result.returncode == 0 else "FAIL_INTERNAL_CONTINUABLE",
        "observer": observer,
        "exit_code": result.returncode,
        "output": result.stdout[-12000:],
    }


def main() -> int:
    failures: list[str] = []
    try:
        registry = load_registry()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"WIKI PUBLIC-ANCHOR INTERNAL EXECUTOR: FAIL - {exc}")
        return 1

    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        print("WIKI PUBLIC-ANCHOR INTERNAL EXECUTOR: FAIL - tasks must be an array")
        return 1

    results: list[dict[str, Any]] = []
    for task in tasks:
        if not isinstance(task, dict):
            failures.append("non-object task entry")
            continue
        task_id = task.get("task_id")
        state = task.get("state")
        if not isinstance(task_id, str) or not task_id:
            failures.append("task missing task_id")
            continue
        if state == "COMPLETE_INTERNAL":
            results.append({
                "task_id": task_id,
                "state": "ALREADY_COMPLETE_INTERNAL",
                "observer": task.get("observer"),
                "exit_code": 0,
                "output": "Registry marks this task complete.",
            })
            continue
        if state not in RUNNABLE_STATES:
            results.append({
                "task_id": task_id,
                "state": "NOT_RUN_STATE_NOT_RUNNABLE",
                "observer": task.get("observer"),
                "exit_code": None,
                "output": f"Registry state {state!r} is not runnable.",
            })
            continue
        results.append(run_observer(task))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "wiki-public-anchor-internal-task-execution.v1",
        "registry_id": registry.get("registry_id"),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_policy": {
            "continue_after_task_failure": True,
            "external_tasks_exist": False,
            "failed_task_blocks_unrelated_tasks": False,
            "deferred_aggregate_tasks": sorted(DEFERRED_AGGREGATE_TASK_IDS),
            "recursion_prevention_active": True,
        },
        "results": results,
        "summary": {
            "total": len(results),
            "pass": sum(item["state"] in {"PASS_INTERNAL", "ALREADY_COMPLETE_INTERNAL"} for item in results),
            "fail_continuable": sum(item["state"] == "FAIL_INTERNAL_CONTINUABLE" for item in results),
            "blocked_missing_observer": sum(item["state"] == "BLOCKED_MISSING_OBSERVER" for item in results),
            "deferred_self": sum(item["state"] == "DEFERRED_SELF_OBSERVATION" for item in results),
        },
        "authority_boundary": {
            "task_execution_grants_certification": False,
            "task_execution_grants_execution_authority": False,
            "internal_pass_is_external_validation": False,
            "internal_simulation_is_independent_reconstruction": False,
        },
    }
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if failures:
        print("WIKI PUBLIC-ANCHOR INTERNAL EXECUTOR: FAIL - structural task errors")
        for failure in failures:
            print(f"- {failure}")
        return 1

    for item in results:
        print(f"{item['task_id']}: {item['state']} ({item.get('observer')})")
    print(f"WIKI PUBLIC-ANCHOR INTERNAL EXECUTOR: PASS - report written to {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
