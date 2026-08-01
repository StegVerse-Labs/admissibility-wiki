#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "docs/standards/personal-data-control-and-deletion-layer.md"
MANIFEST = ROOT / "static/data/governance/personal-data-control-layer.v1.json"
STATUS = ROOT / "static/status/personal-data-control-layer-status.json"
OBSERVATION = ROOT / "docs/external-frameworks/ta-14-account-data-request-channel-observation-2026-08-01.md"
AGGREGATE = ROOT / "scripts/check_admissibility_automation_handoff.py"

REQUIRED_STANDARD_MARKERS = (
    "A theoretical legal right is not an activated governance capability.",
    "CHANNEL_FAILED",
    "processor propagation",
    "Every task must contain",
    "external tasks",
)

REQUIRED_CAPABILITIES = {
    "controller_identification",
    "request_channel",
    "authenticated_submission",
    "request_state_observation",
    "processing_restriction",
    "data_inventory",
    "deletion",
    "processor_propagation",
    "appeal",
    "completion_receipt",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []

    for path in (STANDARD, MANIFEST, STATUS, OBSERVATION, AGGREGATE):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}", failures)

    if failures:
        for item in failures:
            print(f"- {item}")
        return 1

    standard_text = STANDARD.read_text(encoding="utf-8")
    for marker in REQUIRED_STANDARD_MARKERS:
        if marker not in standard_text:
            fail(f"standard missing marker: {marker}", failures)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    if manifest.get("external_dependency_required") is not False:
        fail("external_dependency_required must be false", failures)
    if manifest.get("authority_granted") is not False:
        fail("authority_granted must be false", failures)

    capabilities = set(manifest.get("capabilities", {}).keys())
    missing_capabilities = sorted(REQUIRED_CAPABILITIES - capabilities)
    if missing_capabilities:
        fail(f"missing capabilities: {', '.join(missing_capabilities)}", failures)

    tasks = manifest.get("tasks", [])
    if not tasks:
        fail("task manifest is empty", failures)
    task_ids: set[str] = set()
    required_task_fields = {
        "task_id", "repository", "path", "owner_role", "input_evidence",
        "completion_predicate", "status", "receipt_path",
    }
    for task in tasks:
        missing = required_task_fields - set(task)
        if missing:
            fail(f"task missing fields {sorted(missing)}", failures)
            continue
        task_id = task["task_id"]
        if task_id in task_ids:
            fail(f"duplicate task_id: {task_id}", failures)
        task_ids.add(task_id)
        if task["repository"] != "StegVerse-Labs/admissibility-wiki":
            fail(f"task {task_id} has external repository", failures)
        if not (ROOT / task["path"]).exists():
            fail(f"task {task_id} path does not exist: {task['path']}", failures)
        if task["status"] != "COMPLETE":
            fail(f"task {task_id} is not COMPLETE", failures)

    aggregate_text = AGGREGATE.read_text(encoding="utf-8")
    if "check_personal_data_control_layer.py" not in aggregate_text:
        fail("personal-data validator not bound into canonical aggregate", failures)

    if status.get("state") != "ACTIVATED_AND_CANONICALLY_BOUND":
        fail("status state is not ACTIVATED_AND_CANONICALLY_BOUND", failures)
    if status.get("all_internal_tasks_complete") is not True:
        fail("all_internal_tasks_complete must be true", failures)
    if status.get("external_tasks_required") is not False:
        fail("external_tasks_required must be false", failures)
    if status.get("authority_granted") is not False:
        fail("status authority_granted must be false", failures)

    if failures:
        print("PERSONAL DATA CONTROL LAYER: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PERSONAL DATA CONTROL LAYER: PASS")
    print(f"- tasks: {len(tasks)} complete")
    print("- external tasks required: false")
    print("- canonical aggregate binding: present")
    print("- authority granted: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
