#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL_STATE = ROOT / "docs" / "GOAL_STATE.json"

REQUIRED_SURFACES = [
    "framework page-status generator",
    "framework page-status validator",
    "canonical workflow build-pages page-status regeneration step",
    "root handoff synchronized",
    "current task sync synchronized",
    "remaining installation targets listed",
]

REQUIRED_DONE = [
    "framework-page displayed evaluation status is generated from manifests and compatibility reports",
    "published site build regenerates page-status blocks before Docusaurus build",
    "handoff files reflect the active workflow and declarative generation state",
    "remaining installation targets are listed",
]


def main() -> int:
    failures: list[str] = []
    if not GOAL_STATE.exists():
        print("GOAL STATE: FAIL")
        print("- missing docs/GOAL_STATE.json")
        return 1

    data = json.loads(GOAL_STATE.read_text(encoding="utf-8"))
    current = data.get("current_goal", {})
    boundary = data.get("boundary", {})

    checks = {
        "artifact type": data.get("artifact_type") == "goal_state",
        "schema version": data.get("schema_version") == "3.4",
        "repo": data.get("repo") == "StegVerse-Labs/admissibility-wiki",
        "goal id": current.get("goal_id") == "declarative-external-framework-generation-pipeline",
        "status": current.get("status") == "ACTIVE",
        "completion": current.get("completion_percent") == 44,
        "cycle": current.get("cycle_status") == "HANDOFF_SYNC_RECORDED",
        "active workflow count": boundary.get("active_workflow_count") == 1,
        "scheduled validation": boundary.get("scheduled_validation_path_exists") is True,
    }
    for label, ok in checks.items():
        if not ok:
            failures.append(f"{label} mismatch")

    surfaces = current.get("built_surfaces", [])
    for item in REQUIRED_SURFACES:
        if item not in surfaces:
            failures.append(f"missing built surface: {item}")

    done_when = current.get("done_when", [])
    for item in REQUIRED_DONE:
        if item not in done_when:
            failures.append(f"missing done criterion: {item}")

    previous_goals = data.get("previous_goals", [])
    if len(previous_goals) < 3:
        failures.append("missing previous goal closures")

    print("GOAL STATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
