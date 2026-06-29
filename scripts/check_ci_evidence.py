#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI_EVIDENCE = ROOT / "docs" / "CI_EVIDENCE.json"


def main() -> int:
    failures: list[str] = []

    if not CI_EVIDENCE.exists():
        print("CI EVIDENCE: FAIL")
        print("- missing docs/CI_EVIDENCE.json")
        return 1

    data = json.loads(CI_EVIDENCE.read_text(encoding="utf-8"))

    if data.get("artifact_type") != "ci_evidence_state":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.2":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("ci_evidence_result") != "NO_CI_EVIDENCE_FAIL_CLOSED":
        failures.append("CI evidence result mismatch")
    if data.get("standing_effect") != "DO_NOT_CLOSE_EXPANSION_CYCLE":
        failures.append("standing effect mismatch")
    if data.get("workflow_runs_returned") != 0:
        failures.append("workflow run count mismatch")
    if data.get("combined_statuses_returned") != 0:
        failures.append("combined status count mismatch")
    if not data.get("commit_checked"):
        failures.append("missing checked commit")

    boundary = data.get("boundary", {})
    if boundary.get("no_ci_evidence_is_green") is not False:
        failures.append("green boundary mismatch")
    if boundary.get("ci_evidence_is_execution_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("missing_ci_fails_closed") is not True:
        failures.append("missing-CI fail-closed boundary mismatch")
    if boundary.get("expansion_cycle_closure_blocked") is not True:
        failures.append("closure blocked boundary mismatch")
    if boundary.get("manual_task_required") is not False:
        failures.append("manual task boundary mismatch")
    if boundary.get("manual_confirmation_substitutes_for_ci") is not False:
        failures.append("manual confirmation boundary mismatch")
    if boundary.get("scheduled_validation_path_exists") is not True:
        failures.append("scheduled validation boundary mismatch")

    print("CI EVIDENCE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
