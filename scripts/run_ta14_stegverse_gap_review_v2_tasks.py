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
    evidence_gaps: list[str] = []
    invalid: list[str] = []
    observations: list[dict[str, object]] = []

    for task in tasks:
        work = ROOT / task["work_path"]
        evidence = ROOT / task["evidence_path"]
        completion = ROOT / task["completion_path"]
        work_exists = work.exists()
        evidence_exists = evidence.exists()
        completion_exists = completion.exists()

        if completion_exists:
            observed_state = "COMPLETED"
            completed.append(task["task_id"])
        elif work_exists:
            observed_state = "ACTIONABLE_EVIDENCE_PRESENT" if evidence_exists else "ACTIONABLE_EVIDENCE_GAP"
            actionable.append(task["task_id"])
            if not evidence_exists:
                evidence_gaps.append(task["task_id"])
        else:
            observed_state = "INVALID_MISSING_WORK_ARTIFACT"
            invalid.append(task["task_id"])

        observations.append({
            "task_id": task["task_id"],
            "declared_state": task["state"],
            "observed_state": observed_state,
            "work_path": task["work_path"],
            "work_exists": work_exists,
            "evidence_path": task["evidence_path"],
            "evidence_exists": evidence_exists,
            "completion_path": task["completion_path"],
            "completion_exists": completion_exists,
        })

    status = {
        "schema_version": "governed-review-task-execution-status.v1",
        "registry": str(REGISTRY.relative_to(ROOT)),
        "execution_mode": "INTERNAL_NONBLOCKING",
        "external_tasks_allowed": False,
        "development_halted": False,
        "completed_tasks": completed,
        "actionable_tasks": actionable,
        "evidence_gap_tasks": evidence_gaps,
        "invalid_tasks": invalid,
        "observations": observations,
        "rules": {
            "evidence_gap_prevents_claim_promotion": True,
            "evidence_gap_prevents_unrelated_work": False,
            "task_without_repository_path_is_invalid": True,
            "status_is_recomputed_from_repository_state": True,
            "completion_requires_completion_path": True,
            "missing_evidence_remains_actionable": True,
        },
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(
        "TA-14 REVIEW TASK OBSERVER: PASS - "
        f"{len(completed)} completed, {len(actionable)} actionable, "
        f"{len(evidence_gaps)} evidence gaps, {len(invalid)} invalid, "
        "development_halted=false"
    )
    if invalid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
