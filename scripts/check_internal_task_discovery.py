#!/usr/bin/env python3
"""Validate the continuous internal task discovery registry."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static/status/internal-task-registry.json"
REQUIRED = {
    "task_id", "title", "owner_record", "work_locations", "completion_predicate",
    "fallback", "state", "blocking", "external_task"
}


def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INTERNAL TASK DISCOVERY VALIDATION: FAIL - {exc}")
        return 1
    errors: list[str] = []
    if data.get("external_tasks_exist") is not False:
        errors.append("external_tasks_exist must be false")
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        errors.append("tasks must be an array")
        tasks = []
    seen: set[str] = set()
    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"tasks[{i}] must be an object")
            continue
        missing = sorted(REQUIRED - set(task))
        if missing:
            errors.append(f"tasks[{i}] missing {missing}")
        task_id = task.get("task_id")
        if task_id in seen:
            errors.append(f"duplicate task_id {task_id}")
        if isinstance(task_id, str):
            seen.add(task_id)
        if task.get("external_task") is not False:
            errors.append(f"{task_id}: external_task must be false")
        if task.get("blocking") is not False:
            errors.append(f"{task_id}: blocking must be false")
        locations = task.get("work_locations", [])
        if not isinstance(locations, list) or not locations:
            errors.append(f"{task_id}: work_locations must be non-empty")
        owner = task.get("owner_record")
        if isinstance(owner, str) and not (ROOT / owner).exists():
            errors.append(f"{task_id}: missing owner_record {owner}")
    if errors:
        print("INTERNAL TASK DISCOVERY VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"INTERNAL TASK DISCOVERY VALIDATION: PASS - {len(tasks)} task(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
