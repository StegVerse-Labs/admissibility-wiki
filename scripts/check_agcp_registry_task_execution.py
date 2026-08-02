#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_agcp_registry_tasks.py"
REPORT = ROOT / "reports/agcp-registry-task-execution.json"
VALID_STATES = {"COMPLETE", "BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED"}


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
        if result.returncode not in (0, 1):
            failures.append(f"unexpected runner exit code {result.returncode}")

    if not REPORT.exists():
        failures.append(f"missing {REPORT.relative_to(ROOT)}")
        report = {}
    else:
        try:
            report = json.loads(REPORT.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid task report: {exc}")
            report = {}

    if report:
        if report.get("schema_version") != "agcp-registry-task-execution.v1":
            failures.append("schema_version mismatch")
        if report.get("task_id") != "ADMISSIBILITY-AGCP-001":
            failures.append("task_id mismatch")
        if report.get("state") not in VALID_STATES:
            failures.append("invalid lifecycle state")
        if report.get("external_tasks_exist") is not False:
            failures.append("external_tasks_exist must be false")
        if report.get("development_halted") is not False:
            failures.append("development_halted must be false")
        if report.get("manual_user_tasks_required") != []:
            failures.append("manual_user_tasks_required must be empty")
        release = report.get("release_condition", {})
        if release.get("machine_observable") is not True:
            failures.append("release condition must be machine observable")
        next_task = report.get("next_executable_task", {})
        if next_task.get("owner") != "repository_canonical_workflow":
            failures.append("next task must remain repository-owned")
        if next_task.get("location") != "scripts/run_agcp_registry_tasks.py":
            failures.append("next task location mismatch")
        duplicate = report.get("duplicate_execution_control", {})
        if duplicate.get("canonical_task_id") != "ADMISSIBILITY-AGCP-001":
            failures.append("duplicate control task identity mismatch")
        if duplicate.get("single_report_path") != "reports/agcp-registry-task-execution.json":
            failures.append("single report path mismatch")
        if duplicate.get("append_only_parallel_queue_forbidden") is not True:
            failures.append("parallel duplicate queue must be forbidden")
        boundary = report.get("authority_boundary", {})
        if any(value is not False for value in boundary.values()):
            failures.append("authority boundary weakened")

    if failures:
        print("AGCP REGISTRY TASK EXECUTION CHECK: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("AGCP REGISTRY TASK EXECUTION CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
