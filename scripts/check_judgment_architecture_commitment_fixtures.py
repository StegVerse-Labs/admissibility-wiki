#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/fixtures/judgment-architecture-decision-commitment-record-cases.json"
STATUS = ROOT / "static/status/judgment-architecture-fixture-status.json"

REQUIRED = {
    "record_id", "decision_maker", "authority_basis", "commitment_timestamp",
    "committed_action", "decision_criteria", "evidence_refs", "known_unknowns",
    "alternatives_considered", "threshold_trigger", "stop_mechanism",
    "recoverability_profile", "authority_boundary",
}
RECOVERY_REQUIRED = {
    "rollback_test_receipt", "irreversibility_boundary", "recovery_owner", "validity_window"
}


def nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        return bool(value)
    return value is not None


def evaluate(record: dict[str, object]) -> tuple[str, list[str]]:
    missing = sorted(key for key in REQUIRED if key not in record or not nonempty(record.get(key)))
    recovery = record.get("recoverability_profile")
    if not isinstance(recovery, dict):
        missing.append("recoverability_profile")
    else:
        missing.extend(
            f"recoverability_profile.{key}"
            for key in sorted(RECOVERY_REQUIRED)
            if key not in recovery or not nonempty(recovery.get(key))
        )
    boundary = record.get("authority_boundary")
    if not isinstance(boundary, dict):
        missing.append("authority_boundary")
    else:
        if boundary.get("record_is_execution_authority") is not False:
            missing.append("authority_boundary.record_is_execution_authority=false")
        if boundary.get("human_commitment_is_admissibility") is not False:
            missing.append("authority_boundary.human_commitment_is_admissibility=false")
    return ("FAIL-CLOSED", sorted(set(missing))) if missing else ("REVIEW_READY_NON_AUTHORIZING", [])


def main() -> int:
    failures: list[str] = []
    if not CASES.exists():
        print("JUDGMENT ARCHITECTURE COMMITMENT FIXTURES: FAIL")
        print(f"- missing {CASES.relative_to(ROOT)}")
        return 1

    payload = json.loads(CASES.read_text(encoding="utf-8"))
    results = []
    for case in payload.get("cases", []):
        actual, reasons = evaluate(case.get("record", {}))
        expected = case.get("expected_result")
        if actual != expected:
            failures.append(f"{case.get('case_id')}: expected {expected}, got {actual}")
        results.append({
            "case_id": case.get("case_id"),
            "expected_result": expected,
            "actual_result": actual,
            "fail_closed_reasons": reasons,
            "passed": actual == expected,
        })

    status = {
        "artifact_type": "judgment_architecture_fixture_status",
        "schema_version": "0.1",
        "overall_status": "FAIL" if failures else "PASS",
        "mapping_state": "fixture_ready",
        "runtime_observation_state": "DETERMINISTIC_LOCAL_FIXTURE_ONLY",
        "results": results,
        "authority_boundary": {
            "fixture_is_execution_authority": False,
            "review_ready_is_allow": False,
            "human_commitment_is_admissibility": False,
            "compatibility_is_established": False,
        },
        "next_required_action": "attach stable source citations and observed Decision Commitment Record evidence before replay-ready promotion",
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    print("JUDGMENT ARCHITECTURE COMMITMENT FIXTURES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
