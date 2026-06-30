#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "docs" / "external-frameworks" / "generated-page-progress.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"
RELEASE_CHECK = ROOT / "scripts" / "check_generated_page_release_readiness.py"
DOWNSTREAM_CHECK = ROOT / "scripts" / "check_generated_page_downstream_tasks.py"


def run_optional_check(path: Path, label: str, failures: list[str]) -> None:
    if path.exists():
        result = subprocess.run(["python", str(path)], check=False)
        if result.returncode != 0:
            failures.append(f"{label} failed")


def main() -> int:
    failures: list[str] = []
    if not PROGRESS.exists():
        print("GENERATED PAGE PROGRESS: FAIL")
        print("- progress file missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE PROGRESS: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(PROGRESS.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_progress":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("org") != model.get("org"):
        failures.append("org mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("current_checkpoint") != model.get("current_checkpoint"):
        failures.append("checkpoint mismatch")
    if data.get("repo_percent_complete") != model.get("repo_percent_complete"):
        failures.append("repo percent mismatch")
    if data.get("goal_activation_percent_complete") != model.get("goal_activation_percent_complete"):
        failures.append("activation percent mismatch")

    delta = data.get("actual_vs_recorded", {})
    if delta.get("actual_percent") != model.get("repo_percent_complete"):
        failures.append("actual percent mismatch")
    if delta.get("recorded_goal_state_percent") != model.get("recorded_goal_state_percent"):
        failures.append("recorded percent mismatch")
    if delta.get("reason") != model.get("checkpoint_reason"):
        failures.append("checkpoint reason mismatch")

    surfaces = data.get("active_surfaces", [])
    for surface in model.get("active_surfaces", []):
        if surface not in surfaces:
            failures.append(f"missing surface: {surface}")

    destinations = {item.get("destination") for item in data.get("remaining_tasks", [])}
    for item in model.get("remaining_tasks", []):
        destination = item.get("destination")
        if destination not in destinations:
            failures.append(f"missing destination: {destination}")

    boundary = data.get("boundary", {})
    if boundary.get("progress_record_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_progress_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")

    run_optional_check(RELEASE_CHECK, "release readiness check", failures)
    run_optional_check(DOWNSTREAM_CHECK, "downstream task check", failures)

    print("GENERATED PAGE PROGRESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
