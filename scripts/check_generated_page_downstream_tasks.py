#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs" / "external-frameworks" / "generated-page-downstream-tasks.json"

REQUIRED = {
    "StegVerse-Labs/Site": "site.generated-framework-results-summary",
    "GCAT-BCAT-Engine/Publisher": "publisher.generated-framework-results-import-awareness",
    "stegguardian-wiki": "guardian.execution-authority-boundary-summary",
}


def main() -> int:
    failures: list[str] = []
    if not TASKS.exists():
        print("GENERATED PAGE DOWNSTREAM TASKS: FAIL")
        print("- downstream task manifest missing")
        return 1

    data = json.loads(TASKS.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_downstream_tasks":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("activation_condition") != "after release tag and green public verification":
        failures.append("activation condition mismatch")

    tasks = {item.get("destination"): item for item in data.get("tasks", [])}
    for destination, task_id in REQUIRED.items():
        item = tasks.get(destination)
        if not item:
            failures.append(f"missing destination: {destination}")
            continue
        if item.get("task_id") != task_id:
            failures.append(f"task id mismatch: {destination}")
        if item.get("status") != "pending_release_tag":
            failures.append(f"task status mismatch: {destination}")
        if not item.get("required_input"):
            failures.append(f"required input missing: {destination}")

    boundary = data.get("boundary", {})
    if boundary.get("downstream_tasks_are_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_downstream_task_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("release_tag_required_before_downstream_install") is not True:
        failures.append("release gate boundary mismatch")

    print("GENERATED PAGE DOWNSTREAM TASKS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
