#!/usr/bin/env python3
"""Run all registered Wiki public-anchor task queues without global stalling."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static" / "status" / "wiki-public-anchor-task-mesh-registry.json"
REPORT = ROOT / "reports" / "wiki-public-anchor-task-mesh-execution.json"


def load_registry() -> dict[str, Any]:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("task-mesh registry must contain an object")
    queues = value.get("queues")
    if not isinstance(queues, list) or not queues:
        raise ValueError("task-mesh registry must contain at least one queue")
    return value


def main() -> int:
    try:
        registry = load_registry()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"WIKI PUBLIC-ANCHOR TASK MESH: FAIL - {exc}")
        return 1

    results: list[dict[str, Any]] = []
    structural_failures: list[str] = []
    for queue in registry["queues"]:
        if not isinstance(queue, dict):
            structural_failures.append("non-object queue entry")
            continue
        queue_id = queue.get("queue_id")
        runner_value = queue.get("runner")
        registry_value = queue.get("registry")
        report_value = queue.get("report")
        validator_value = queue.get("validator")
        required_values = (queue_id, runner_value, registry_value, report_value, validator_value)
        if not all(isinstance(value, str) and value for value in required_values):
            structural_failures.append(f"invalid queue declaration: {queue!r}")
            continue

        runner = ROOT / runner_value
        queue_registry = ROOT / registry_value
        queue_report = ROOT / report_value
        validator = ROOT / validator_value
        required_paths = (runner, queue_registry, validator)
        if any(not path.exists() for path in required_paths):
            missing = [str(path.relative_to(ROOT)) for path in required_paths if not path.exists()]
            results.append({
                "queue_id": queue_id,
                "runner": runner_value,
                "registry": registry_value,
                "report": report_value,
                "validator": validator_value,
                "state": "BLOCKED_MISSING_QUEUE_ARTIFACT",
                "missing": missing,
            })
            structural_failures.extend(missing)
            continue

        result = subprocess.run(
            [sys.executable, str(runner)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        results.append({
            "queue_id": queue_id,
            "runner": runner_value,
            "registry": registry_value,
            "report": report_value,
            "validator": validator_value,
            "state": "PASS_INTERNAL" if result.returncode == 0 else "FAIL_INTERNAL_CONTINUABLE",
            "exit_code": result.returncode,
            "report_exists": queue_report.exists(),
            "output": result.stdout[-12000:],
        })

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "wiki-public-anchor-task-mesh-execution.v1",
        "registry": str(REGISTRY.relative_to(ROOT)),
        "registry_id": registry.get("registry_id"),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_policy": {
            "external_tasks_exist": False,
            "registry_driven_queue_discovery": True,
            "continue_after_queue_failure": True,
            "failed_queue_blocks_unrelated_queue": False,
            "evidence_gap_halts_development": False,
        },
        "queues": results,
        "summary": {
            "registered": len(registry["queues"]),
            "observed": len(results),
            "pass": sum(item["state"] == "PASS_INTERNAL" for item in results),
            "fail_continuable": sum(item["state"] == "FAIL_INTERNAL_CONTINUABLE" for item in results),
            "blocked_structural": sum(item["state"] == "BLOCKED_MISSING_QUEUE_ARTIFACT" for item in results),
        },
        "authority_boundary": {
            "task_mesh_pass_is_external_validation": False,
            "task_mesh_pass_grants_certification": False,
            "task_mesh_pass_grants_execution_authority": False,
        },
    }
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for item in results:
        print(f"{item['queue_id']}: {item['state']} ({item['runner']})")
    if structural_failures:
        print("WIKI PUBLIC-ANCHOR TASK MESH: FAIL - missing or invalid queue structure")
        for failure in structural_failures:
            print(f"- {failure}")
        return 1
    print(
        "WIKI PUBLIC-ANCHOR TASK MESH: PASS - "
        f"{len(results)} registered queues observed; report written to {REPORT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
