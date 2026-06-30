#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "docs" / "external-frameworks" / "generated-page-ci-evidence-request.json"
TAG_CHECK = ROOT / "scripts" / "check_generated_page_tag_candidate.py"

REQUIRED_EVIDENCE = [
    "single canonical workflow conclusion",
    "generated page status validation conclusion",
    "generated page progress validation conclusion",
    "generated page release readiness validation conclusion",
    "generated page downstream task validation conclusion",
    "generated page tag candidate validation conclusion",
    "generated page closeout bundle validation conclusion",
    "generated page validation summary generation conclusion",
    "public GitHub Pages verification conclusion",
]


def main() -> int:
    failures: list[str] = []
    if not REQUEST.exists():
        print("GENERATED PAGE CI EVIDENCE REQUEST: FAIL")
        print("- request file missing")
        return 1

    data = json.loads(REQUEST.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_ci_evidence_request":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("current_state") != "pending_next_workflow_run":
        failures.append("current state mismatch")
    if data.get("release_gate") != "blocked_until_green_ci_and_public_verification":
        failures.append("release gate mismatch")

    evidence = data.get("requested_evidence", [])
    for item in REQUIRED_EVIDENCE:
        if item not in evidence:
            failures.append(f"missing evidence request: {item}")

    removed = data.get("manual_tasks_removed", [])
    for task in ["manual_ci_evidence_reconstruction", "manual_public_verification_reconstruction"]:
        if task not in removed:
            failures.append(f"manual task not removed: {task}")

    boundary = data.get("boundary", {})
    if boundary.get("ci_request_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("missing_ci_fails_closed") is not True:
        failures.append("missing CI boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")

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
