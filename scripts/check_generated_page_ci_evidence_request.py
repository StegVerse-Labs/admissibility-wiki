#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "docs" / "external-frameworks" / "generated-page-ci-evidence-request.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"
TAG_CHECK = ROOT / "scripts" / "check_generated_page_tag_candidate.py"


def main() -> int:
    failures: list[str] = []
    if not REQUEST.exists():
        print("GENERATED PAGE CI EVIDENCE REQUEST: FAIL")
        print("- request file missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE CI EVIDENCE REQUEST: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(REQUEST.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    ci = model.get("ci", {})
    boundary_model = model.get("boundary", {})

    if data.get("artifact_type") != "generated_page_ci_evidence_request":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("current_state") != ci.get("current_state"):
        failures.append("current state mismatch")
    if data.get("release_gate") != ci.get("release_gate"):
        failures.append("release gate mismatch")

    evidence = data.get("requested_evidence", [])
    required_evidence = ci.get("requested_evidence", [])
    for item in required_evidence:
        if item not in evidence:
            failures.append(f"missing evidence request: {item}")
    for item in evidence:
        if item not in required_evidence:
            failures.append(f"undeclared evidence request: {item}")

    removed = data.get("manual_tasks_removed", [])
    required_removed = ci.get("manual_tasks_removed", [])
    for task in required_removed:
        if task not in removed:
            failures.append(f"manual task not removed: {task}")
    for task in removed:
        if task not in required_removed:
            failures.append(f"undeclared removed manual task: {task}")

    boundary = data.get("boundary", {})
    if boundary.get("ci_request_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("missing_ci_fails_closed") is not True:
        failures.append("missing CI boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")
    if boundary_model.get("release_without_authorization_allowed") is not False:
        failures.append("state model release boundary mismatch")

    if TAG_CHECK.exists():
        result = subprocess.run(["python", str(TAG_CHECK)], check=False)
        if result.returncode != 0:
            failures.append("tag candidate check failed")

    print("GENERATED PAGE CI EVIDENCE REQUEST:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
