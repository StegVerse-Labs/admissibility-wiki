#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_wiki_public_anchor_task_mesh.py"
REGISTRY = ROOT / "static" / "status" / "wiki-public-anchor-task-mesh-registry.json"
REPORT = ROOT / "reports" / "wiki-public-anchor-task-mesh-execution.json"


def load(path: Path, failures: list[str]) -> dict:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        failures.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"{path.relative_to(ROOT)} must contain an object")
        return {}
    return value


def main() -> int:
    failures: list[str] = []
    registry = load(REGISTRY, failures)

    if registry:
        if registry.get("schema_version") != "wiki-public-anchor-task-mesh-registry.v1":
            failures.append("task-mesh registry schema mismatch")
        if registry.get("state") != "ACTIVE_INTERNAL_MULTI_QUEUE_EXECUTION":
            failures.append("task-mesh registry state mismatch")
        policy = registry.get("policy", {})
        if policy.get("external_tasks_exist") is not False:
            failures.append("task-mesh registry must deny external tasks")
        if policy.get("queue_failure_blocks_unrelated_queues") is not False:
            failures.append("queue failure must not block unrelated queues")
        if policy.get("evidence_gap_halts_development") is not False:
            failures.append("evidence gaps must not halt development")

        queue_ids: set[str] = set()
        for index, queue in enumerate(registry.get("queues", [])):
            if not isinstance(queue, dict):
                failures.append(f"queues[{index}] must be an object")
                continue
            queue_id = queue.get("queue_id")
            if not isinstance(queue_id, str) or not queue_id:
                failures.append(f"queues[{index}] missing queue_id")
                continue
            if queue_id in queue_ids:
                failures.append(f"duplicate queue id: {queue_id}")
            queue_ids.add(queue_id)
            for key in ("owner_record", "runner", "registry", "validator"):
                value = queue.get(key)
                if not isinstance(value, str) or not value:
                    failures.append(f"{queue_id} missing {key}")
                elif not (ROOT / value).exists():
                    failures.append(f"{queue_id} path does not exist: {value}")
            report = queue.get("report")
            if not isinstance(report, str) or not report:
                failures.append(f"{queue_id} missing report location")
            if not isinstance(queue.get("completion_predicate"), str) or not queue.get("completion_predicate"):
                failures.append(f"{queue_id} missing completion predicate")

        if queue_ids != {"public-anchor-internal", "ta14-gap-review-v2"}:
            failures.append("task-mesh registry queue set mismatch")

    if not RUNNER.exists():
        failures.append(f"missing {RUNNER.relative_to(ROOT)}")
    else:
        result = subprocess.run(
            [sys.executable, str(RUNNER)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        print(result.stdout.rstrip())
        if result.returncode != 0:
            failures.append("task-mesh runner structural validation failed")

    report = load(REPORT, failures)
    if report:
        policy = report.get("execution_policy", {})
        if policy.get("external_tasks_exist") is not False:
            failures.append("task mesh must deny external tasks")
        if policy.get("continue_after_queue_failure") is not True:
            failures.append("task mesh must continue after queue failure")
        if policy.get("failed_queue_blocks_unrelated_queue") is not False:
            failures.append("failed queue must not block unrelated queues")
        if policy.get("evidence_gap_halts_development") is not False:
            failures.append("evidence gaps must not halt development")
        queues = report.get("queues", [])
        ids = {item.get("queue_id") for item in queues if isinstance(item, dict)}
        if ids != {"public-anchor-internal", "ta14-gap-review-v2"}:
            failures.append("task-mesh report queue set mismatch")
        boundary = report.get("authority_boundary", {})
        for key in (
            "task_mesh_pass_is_external_validation",
            "task_mesh_pass_grants_certification",
            "task_mesh_pass_grants_execution_authority",
        ):
            if boundary.get(key) is not False:
                failures.append(f"authority boundary {key} must be false")

    if failures:
        print("WIKI PUBLIC-ANCHOR TASK MESH CHECK: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("WIKI PUBLIC-ANCHOR TASK MESH CHECK: PASS - located public-anchor and TA-14 queues execute without global stalling")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
