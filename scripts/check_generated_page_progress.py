#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "docs" / "external-frameworks" / "generated-page-progress.json"

REQUIRED_SURFACES = [
    "metadata",
    "mapping",
    "page_status",
    "analysis_boundary",
    "surface_inventory",
    "surface_handoff",
    "root_addendum",
    "validation_summary",
]

REQUIRED_DESTINATIONS = [
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "stegguardian-wiki",
]


def main() -> int:
    failures: list[str] = []
    if not PROGRESS.exists():
        print("GENERATED PAGE PROGRESS: FAIL")
        print("- progress file missing")
        return 1

    data = json.loads(PROGRESS.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_progress":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("current_checkpoint") != "VALIDATION_SUMMARY_RECORDED":
        failures.append("checkpoint mismatch")
    if data.get("repo_percent_complete") != 74:
        failures.append("repo percent mismatch")
    if data.get("goal_activation_percent_complete") != 74:
        failures.append("activation percent mismatch")

    delta = data.get("actual_vs_recorded", {})
    if delta.get("actual_percent") != 74:
        failures.append("actual percent mismatch")
    if delta.get("recorded_goal_state_percent") != 44:
        failures.append("recorded percent mismatch")

    surfaces = data.get("active_surfaces", [])
    for surface in REQUIRED_SURFACES:
        if surface not in surfaces:
            failures.append(f"missing surface: {surface}")

    destinations = {item.get("destination") for item in data.get("remaining_tasks", [])}
    for destination in REQUIRED_DESTINATIONS:
        if destination not in destinations:
            failures.append(f"missing destination: {destination}")

    boundary = data.get("boundary", {})
    if boundary.get("progress_record_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_progress_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")

    print("GENERATED PAGE PROGRESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
