#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs" / "external-frameworks" / "generated-page-downstream-tasks.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"
CI_REQUEST_CHECK = ROOT / "scripts" / "check_generated_page_ci_evidence_request.py"


def main() -> int:
    failures: list[str] = []
    if not TASKS.exists():
        print("GENERATED PAGE DOWNSTREAM TASKS: FAIL")
        print("- downstream task manifest missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE DOWNSTREAM TASKS: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(TASKS.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    downstream = model.get("downstream", {})
    if data.get("artifact_type") != "generated_page_downstream_tasks":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("activation_condition") != downstream.get("activation_condition"):
        failures.append("activation condition mismatch")

    tasks = {item.get("destination"): item for item in data.get("tasks", [])}
    model_tasks = {item.get("destination"): item for item in downstream.get("tasks", [])}
    for destination, expected in model_tasks.items():
        item = tasks.get(destination)
        if not item:
            failures.append(f"missing destination: {destination}")
            continue
        for key in ["task_id", "required_input", "status"]:
            if item.get(key) != expected.get(key):
                failures.append(f"{key} mismatch: {destination}")

    boundary = data.get("boundary", {})
    if boundary.get("downstream_tasks_are_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_downstream_task_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("release_tag_required_before_downstream_install") is not True:
        failures.append("release gate boundary mismatch")
    if model.get("boundary", {}).get("release_without_authorization_allowed") is not False:
        failures.append("state model release boundary mismatch")

    if CI_REQUEST_CHECK.exists():
        result = subprocess.run(["python", str(CI_REQUEST_CHECK)], check=False)
        if result.returncode != 0:
            failures.append("CI evidence request check failed")

    print("GENERATED PAGE DOWNSTREAM TASKS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
