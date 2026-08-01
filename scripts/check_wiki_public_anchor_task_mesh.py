#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_wiki_public_anchor_task_mesh.py"
REPORT = ROOT / "reports" / "wiki-public-anchor-task-mesh-execution.json"


def main() -> int:
    failures: list[str] = []
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

    if not REPORT.exists():
        failures.append(f"missing {REPORT.relative_to(ROOT)} after runner execution")
    else:
        try:
            report = json.loads(REPORT.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid task-mesh report: {exc}")
            report = {}
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
        if "public-anchor-internal" not in ids:
            failures.append("public-anchor internal queue missing")
        if "ta14-gap-review-v2" not in ids:
            failures.append("TA-14 gap-review queue missing")
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
    print("WIKI PUBLIC-ANCHOR TASK MESH CHECK: PASS - public-anchor and TA-14 queues are observed without global stalling")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
