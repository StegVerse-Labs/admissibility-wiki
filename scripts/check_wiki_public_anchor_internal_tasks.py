#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static" / "status" / "wiki-public-anchor-internal-task-registry.json"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    require(REGISTRY.exists(), "missing internal task registry", failures)
    if failures:
        print("WIKI PUBLIC-ANCHOR INTERNAL TASKS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"WIKI PUBLIC-ANCHOR INTERNAL TASKS: FAIL\n- invalid JSON: {exc}")
        return 1

    require(registry.get("schema_version") == "wiki-public-anchor-internal-task-registry.v1", "schema version mismatch", failures)
    require(registry.get("state") == "BEING_BUILT_INTERNAL_EXECUTION_ACTIVE", "registry state mismatch", failures)

    activation = registry.get("activation", {})
    require(activation.get("installed") is True, "internal continuation must be installed", failures)
    require(activation.get("executor_active") is True, "internal executor must be active", failures)
    require(activation.get("external_tasks_exist") is False, "activation must deny external tasks", failures)
    require(activation.get("development_may_continue_when_evidence_is_missing") is True, "missing evidence must not halt development", failures)
    require("run_wiki_public_anchor_internal_tasks.py" in str(activation.get("canonical_binding", "")), "canonical binding must include the internal executor", failures)

    policy = registry.get("policy", {})
    require(policy.get("external_tasks_exist") is False, "external_tasks_exist must be false", failures)
    require(policy.get("missing_external_evidence_blocks_unrelated_development") is False, "external evidence gaps must not block unrelated development", failures)
    require(policy.get("every_task_requires_repository_location") is True, "repository-location requirement missing", failures)
    require(policy.get("every_task_requires_observer") is True, "observer requirement missing", failures)
    require(policy.get("every_task_requires_completion_predicate") is True, "completion-predicate requirement missing", failures)

    tasks = registry.get("tasks", [])
    require(isinstance(tasks, list) and bool(tasks), "tasks must be a non-empty array", failures)
    ids: set[str] = set()
    for index, task in enumerate(tasks if isinstance(tasks, list) else []):
        prefix = f"tasks[{index}]"
        require(isinstance(task, dict), f"{prefix} must be an object", failures)
        if not isinstance(task, dict):
            continue
        task_id = task.get("task_id")
        require(isinstance(task_id, str) and task_id, f"{prefix}.task_id missing", failures)
        if isinstance(task_id, str):
            require(task_id not in ids, f"duplicate task id: {task_id}", failures)
            ids.add(task_id)
        require(task.get("state") in {"READY_INTERNAL", "ACTIVE_INTERNAL", "COMPLETE_INTERNAL", "BLOCKED_BY_INTERNAL_FAILURE"}, f"{prefix}.state invalid", failures)
        owner = task.get("owner_record")
        require(isinstance(owner, str) and owner, f"{prefix}.owner_record missing", failures)
        if isinstance(owner, str) and owner:
            require((ROOT / owner).exists(), f"{prefix} owner path does not exist: {owner}", failures)
        locations = task.get("work_locations")
        require(isinstance(locations, list) and bool(locations), f"{prefix}.work_locations missing", failures)
        for location in locations if isinstance(locations, list) else []:
            require(isinstance(location, str) and location, f"{prefix} has invalid work location", failures)
            if isinstance(location, str) and location:
                require((ROOT / location).exists(), f"{prefix} work path does not exist: {location}", failures)
        generated_output = task.get("generated_output")
        if generated_output is not None:
            require(isinstance(generated_output, str) and bool(generated_output), f"{prefix}.generated_output invalid", failures)
        observer = task.get("observer")
        require(isinstance(observer, str) and observer, f"{prefix}.observer missing", failures)
        if isinstance(observer, str) and observer:
            require((ROOT / observer).exists(), f"{prefix} observer path does not exist: {observer}", failures)
        require(isinstance(task.get("completion_predicate"), str) and bool(task.get("completion_predicate")), f"{prefix}.completion_predicate missing", failures)
        require(isinstance(task.get("fallback"), str) and bool(task.get("fallback")), f"{prefix}.fallback missing", failures)

    require("PA-INT-009" in ids, "executor task PA-INT-009 missing", failures)

    gaps = registry.get("evidence_gaps", [])
    require(isinstance(gaps, list), "evidence_gaps must be an array", failures)
    for index, gap in enumerate(gaps if isinstance(gaps, list) else []):
        require(isinstance(gap, dict), f"evidence_gaps[{index}] must be an object", failures)
        if not isinstance(gap, dict):
            continue
        require(str(gap.get("state", "")).endswith("NON_BLOCKING"), f"evidence_gaps[{index}] must be explicitly non-blocking", failures)
        require(isinstance(gap.get("internal_continuation"), str) and bool(gap.get("internal_continuation")), f"evidence_gaps[{index}] internal continuation missing", failures)

    boundary = registry.get("authority_boundary", {})
    for key in (
        "certification_granted",
        "execution_authority_granted",
        "government_recognition_claimed",
        "synthetic_result_is_external_validation",
        "internal_simulation_is_independent_reconstruction",
    ):
        require(boundary.get(key) is False, f"authority boundary {key} must be false", failures)

    if failures:
        print("WIKI PUBLIC-ANCHOR INTERNAL TASKS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"WIKI PUBLIC-ANCHOR INTERNAL TASKS: PASS - {len(tasks)} located internal tasks, active executor, and {len(gaps)} non-blocking evidence gaps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
