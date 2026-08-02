#!/usr/bin/env python3
"""Validate the internal, repository-addressable TA-14 review task layer.

This check accepts incomplete evidence while forbidding external/manual waiting
states. Every task must remain observable, actionable, and nonblocking until a
task-specific completion receipt exists.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.task-registry.json"
STATUS = ROOT / "static/status/ta-14-stegverse-gap-review-v2.execution-status.json"
ADJUDICATION = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.adjudication.json"
ROUTE_MANIFEST = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-route-complete-evidence-manifest.v1.json"
OBSERVER = ROOT / "scripts/run_ta14_stegverse_gap_review_v2_tasks.py"
ADJUDICATION_CHECK = ROOT / "scripts/check_ta14_stegverse_gap_review_v2_adjudication.py"
ROUTE_MANIFEST_CHECK = ROOT / "scripts/check_ta14_stegverse_route_complete_evidence_manifest.py"


def fail(message: str) -> None:
    print(f"TA-14 REVIEW TASK EXECUTION: FAIL - {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"top-level object required: {path.relative_to(ROOT)}")
    return value


def run_check(path: Path, label: str) -> None:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    result = subprocess.run(
        [sys.executable, str(path)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    print(result.stdout.rstrip())
    if result.returncode != 0:
        fail(f"{label} failed")


def main() -> None:
    for path in (OBSERVER, ADJUDICATION, ROUTE_MANIFEST, ADJUDICATION_CHECK, ROUTE_MANIFEST_CHECK):
        if not path.is_file():
            fail(f"missing {path.relative_to(ROOT)}")

    registry = load(REGISTRY)
    status = load(STATUS)
    policy = registry.get("execution_policy")
    if not isinstance(policy, dict):
        fail("execution_policy object required")
    if policy.get("external_tasks_allowed") is not False:
        fail("external_tasks_allowed must remain false")
    if policy.get("unresolved_evidence_halts_unrelated_work") is not False:
        fail("unresolved evidence must not halt unrelated work")
    if policy.get("evidence_gaps_remain_actionable") is not True:
        fail("evidence gaps must remain actionable")

    tasks = registry.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        fail("non-empty tasks array required")

    task_ids: set[str] = set()
    completion_paths: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict):
            fail("each task must be an object")
        task_id = task.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            fail("every task requires task_id")
        if task_id in task_ids:
            fail(f"duplicate task_id: {task_id}")
        task_ids.add(task_id)
        for field in ("work_path", "evidence_path", "completion_path"):
            value = task.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"{task_id} missing {field}")
            if value.startswith(("http://", "https://")):
                fail(f"{task_id} {field} must be repository-addressable, not external")
        completion_path = task["completion_path"]
        if completion_path in completion_paths:
            fail(f"completion path must be task-specific: {completion_path}")
        completion_paths.add(completion_path)
        if task.get("state") in {"WAITING_EXTERNAL", "MANUAL_REQUIRED", "BLOCKED_EXTERNAL"}:
            fail(f"{task_id} contains prohibited external/manual state")

    if status.get("execution_mode") != "INTERNAL_NONBLOCKING":
        fail("execution_mode must be INTERNAL_NONBLOCKING")
    if status.get("external_tasks_allowed") is not False:
        fail("status must prohibit external tasks")
    if status.get("development_halted") is not False:
        fail("development_halted must remain false")

    rules = status.get("rules")
    if not isinstance(rules, dict):
        fail("status rules object required")
    required_rules = {
        "evidence_gap_prevents_claim_promotion": True,
        "evidence_gap_prevents_unrelated_work": False,
        "task_without_repository_path_is_invalid": True,
        "status_is_recomputed_from_repository_state": True,
        "completion_requires_completion_path": True,
        "missing_evidence_remains_actionable": True,
    }
    for key, expected in required_rules.items():
        if rules.get(key) is not expected:
            fail(f"status rule mismatch: {key}")

    observations = status.get("observations")
    if not isinstance(observations, list):
        fail("status observations array required")
    observed_ids = {item.get("task_id") for item in observations if isinstance(item, dict)}
    if observed_ids != task_ids:
        fail("status observations must cover every registry task exactly")
    if status.get("invalid_tasks") != []:
        fail("invalid_tasks must be empty before canonical binding")

    run_check(ADJUDICATION_CHECK, "bounded finding adjudication")
    run_check(ROUTE_MANIFEST_CHECK, "route-complete evidence manifest structure")

    print(f"TA-14 REVIEW TASK EXECUTION: PASS - {len(task_ids)} internal tasks are repository-addressable, actionable, and nonblocking")


if __name__ == "__main__":
    main()
