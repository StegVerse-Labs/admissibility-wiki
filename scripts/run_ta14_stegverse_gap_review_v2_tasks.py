#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.task-registry.json"
STATUS = ROOT / "static/status/ta-14-stegverse-gap-review-v2.execution-status.json"


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    tasks = registry["tasks"]
    completed: list[str] = []
    actionable: list[str] = []
    blocked: list[str] = []
    observations: list[dict[str, object]] = []

    for task in tasks:
        work = ROOT / task["work_path"]
        evidence = ROOT / task["evidence_path"]
        work_exists = work.exists()
        evidence_exists = evidence.exists()
        if work_exists and evidence_exists:
            observed_state = "IMPLEMENTED" if task["state"] != "READY" else "READY_TO_EXECUTE"
            actionable.append(task["task_id"])
        elif not work_exists:
            observed_state = "MISSING_WORK_ARTIFACT"
            blocked.append(task["task_id"])
        else:
            observed_state = "MISSING_EVIDENCE_ARTIFACT"
            blocked.append(task["task_id"])
        observations.append({
            "task_id": task["task_id"],
            "declared_state": task["state"],
            "observed_state": observed_state,
            "work_path": task["work_path"],
            "work_exists": work_exists,
            "evidence_path": task["evidence_path"],
            "evidence_exists": evidence_exists,
            "completion_path": task["completion_path"],
        })

    status = {
        "schema_version": "governed-review-task-execution-status.v1",
        "registry": str(REGISTRY.relative_to(ROOT)),
        "execution_mode": "INTERNAL_NONBLOCKING",
        "external_tasks_allowed": False,
        "development_halted": False,
        "completed_tasks": completed,
        "actionable_tasks": actionable,
        "blocked_tasks": blocked,
        "observations": observations,
        "rules": {
            "blocked_task_prevents_claim_promotion": True,
            "blocked_task_prevents_unrelated_work": False,
            "task_without_repository_path_is_invalid": True,
            "status_is_recomputed_from_repository_state": True,
        },
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"TA-14 REVIEW TASK OBSERVER: PASS - {len(actionable)} actionable, {len(blocked)} blocked, development_halted=false")


if __name__ == "__main__":
    main()
