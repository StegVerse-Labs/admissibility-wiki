#!/usr/bin/env python3
"""Execute the Wiki public-anchor internal task queue without global stalling.

Each leaf task observer runs independently. Failed observers are recorded and do not
prevent later independent tasks from running. Located registry extensions are merged
into the canonical queue so newly discovered internal work cannot remain outside the
executor merely because the primary registry has not yet been rewritten.

Extension registries are allowed to retain their repository-local task identifiers.
When two located extensions reuse the same local task_id, the execution projection
qualifies the later occurrence with its extension id instead of treating an otherwise
runnable queue as structurally invalid. The original task id and source registry are
preserved in every generated result for reconstruction.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static/status/wiki-public-anchor-internal-task-registry.json"
EXTENSION_GLOB = "wiki-public-anchor-internal-task-registry.*-extension.json"
REPORT = ROOT / "reports/wiki-public-anchor-internal-task-execution.json"

DEFERRED_AGGREGATE_TASK_IDS = {"PA-INT-002", "PA-INT-007", "PA-INT-009"}
RUNNABLE_STATES = {"READY_INTERNAL", "ACTIVE_INTERNAL"}


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def _extension_execution_id(path: Path, extension: dict[str, Any], task_id: str) -> str:
    extension_id = extension.get("extension_id")
    if not isinstance(extension_id, str) or not extension_id:
        extension_id = path.stem.removeprefix("wiki-public-anchor-internal-task-registry.").removesuffix("-extension")
    return f"{extension_id}::{task_id}"


def load_registry() -> tuple[dict[str, Any], list[str]]:
    registry = load_json_object(REGISTRY)
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("primary registry tasks must be an array")

    merged = list(tasks)
    extension_paths = sorted((ROOT / "static/status").glob(EXTENSION_GLOB))
    extension_names: list[str] = []
    known_ids = {task.get("task_id") for task in merged if isinstance(task, dict)}

    for path in extension_paths:
        extension = load_json_object(path)
        extension_tasks = extension.get("tasks", [])
        if not isinstance(extension_tasks, list):
            raise ValueError(f"{path.relative_to(ROOT)} tasks must be an array")

        source_registry = str(path.relative_to(ROOT))
        local_ids: set[str] = set()
        for task in extension_tasks:
            if not isinstance(task, dict):
                raise ValueError(f"{path.relative_to(ROOT)} contains a non-object task")
            task_id = task.get("task_id")
            if not isinstance(task_id, str) or not task_id:
                raise ValueError(f"{path.relative_to(ROOT)} contains a task without task_id")
            if task_id in local_ids:
                raise ValueError(f"duplicate task_id within extension {source_registry}: {task_id}")
            local_ids.add(task_id)

            projected = dict(task)
            projected["source_task_id"] = task_id
            projected["source_registry"] = source_registry
            execution_id = task_id
            if execution_id in known_ids:
                execution_id = _extension_execution_id(path, extension, task_id)
                if execution_id in known_ids:
                    raise ValueError(f"duplicate qualified task_id across registries: {execution_id}")
                projected["execution_id_qualified"] = True
            else:
                projected["execution_id_qualified"] = False
            projected["task_id"] = execution_id
            known_ids.add(execution_id)
            merged.append(projected)
        extension_names.append(source_registry)

    registry["tasks"] = merged
    return registry, extension_names


def _result_identity(task: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"task_id": task["task_id"]}
    if task.get("source_task_id"):
        result["source_task_id"] = task["source_task_id"]
    if task.get("source_registry"):
        result["source_registry"] = task["source_registry"]
    if task.get("execution_id_qualified") is not None:
        result["execution_id_qualified"] = task["execution_id_qualified"]
    return result


def run_observer(task: dict[str, Any]) -> dict[str, Any]:
    task_id = task["task_id"]
    source_task_id = task.get("source_task_id", task_id)
    observer = task["observer"]
    observer_path = ROOT / observer
    identity = _result_identity(task)

    if source_task_id in DEFERRED_AGGREGATE_TASK_IDS or observer_path.resolve() == Path(__file__).resolve():
        return {
            **identity,
            "state": "DEFERRED_SELF_OBSERVATION",
            "observer": observer,
            "exit_code": None,
            "output": "Aggregate or self-referential observer is evaluated by the canonical caller after the internal executor returns.",
        }

    if not observer_path.exists():
        return {
            **identity,
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
        **identity,
        "state": "PASS_INTERNAL" if result.returncode == 0 else "FAIL_INTERNAL_CONTINUABLE",
        "observer": observer,
        "exit_code": result.returncode,
        "output": result.stdout[-12000:],
    }


def main() -> int:
    failures: list[str] = []
    try:
        registry, loaded_extensions = load_registry()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"WIKI PUBLIC-ANCHOR INTERNAL EXECUTOR: FAIL - {exc}")
        return 1

    tasks = registry.get("tasks", [])
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
                **_result_identity(task),
                "state": "ALREADY_COMPLETE_INTERNAL",
                "observer": task.get("observer"),
                "exit_code": 0,
                "output": "Registry marks this task complete.",
            })
            continue
        if state not in RUNNABLE_STATES:
            results.append({
                **_result_identity(task),
                "state": "NOT_RUN_STATE_NOT_RUNNABLE",
                "observer": task.get("observer"),
                "exit_code": None,
                "output": f"Registry state {state!r} is not runnable.",
            })
            continue
        results.append(run_observer(task))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "wiki-public-anchor-internal-task-execution.v3",
        "registry_id": registry.get("registry_id"),
        "loaded_extensions": loaded_extensions,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_policy": {
            "continue_after_task_failure": True,
            "external_tasks_exist": False,
            "failed_task_blocks_unrelated_tasks": False,
            "deferred_aggregate_tasks": sorted(DEFERRED_AGGREGATE_TASK_IDS),
            "recursion_prevention_active": True,
            "located_registry_extensions_are_executed": True,
            "extension_local_task_id_collisions_are_qualified": True,
        },
        "results": results,
        "summary": {
            "total": len(results),
            "pass": sum(item["state"] in {"PASS_INTERNAL", "ALREADY_COMPLETE_INTERNAL"} for item in results),
            "fail_continuable": sum(item["state"] == "FAIL_INTERNAL_CONTINUABLE" for item in results),
            "blocked_missing_observer": sum(item["state"] == "BLOCKED_MISSING_OBSERVER" for item in results),
            "deferred_self": sum(item["state"] == "DEFERRED_SELF_OBSERVATION" for item in results),
            "qualified_extension_task_ids": sum(bool(item.get("execution_id_qualified")) for item in results),
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
        source = item.get("source_task_id")
        suffix = f" source={source}" if source and source != item["task_id"] else ""
        print(f"{item['task_id']}: {item['state']} ({item.get('observer')}){suffix}")
    print(f"WIKI PUBLIC-ANCHOR INTERNAL EXECUTOR: PASS - report written to {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
