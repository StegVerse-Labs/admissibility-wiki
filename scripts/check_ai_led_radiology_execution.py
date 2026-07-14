#!/usr/bin/env python3
"""Deterministically validate AI-led radiology execution-boundary fixtures."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "ai-led-radiology-execution-cases.json"
SCHEMA = ROOT / "static" / "schemas" / "ai-led-radiology-execution-case.schema.json"
FORMALISM = ROOT / "docs" / "formalisms" / "ai-led-radiology-execution-boundary.md"
STATUS = ROOT / "static" / "status" / "ai-led-radiology-execution-status.json"
REPORT = ROOT / "reports" / "ai-led-radiology-execution-receipt.json"

DECISIONS = {
    "ADMIT_ASSISTIVE_USE",
    "ADMIT_AI_FIRST_WITH_MANDATORY_HUMAN_REVIEW",
    "REVIEW_REQUIRED",
    "DENY_AUTONOMOUS_CLEARANCE",
    "FAIL_CLOSED",
}

REQUIRED_FIELDS = {
    "case_id", "operating_mode", "patient_study_bound", "model_identity_verified",
    "model_version_approved", "approved_indication", "image_series_complete",
    "image_quality_acceptable", "out_of_distribution_clear", "clinical_context_available",
    "prior_study_required", "prior_study_available", "human_review_required",
    "human_review_completed", "independent_image_access", "policy_ref",
    "delegation_ref", "provenance_complete", "requested_disposition", "decision",
}


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def decide(record: Dict[str, Any]) -> str:
    evidence_fields = (
        "patient_study_bound", "model_identity_verified", "model_version_approved",
        "approved_indication", "image_series_complete", "image_quality_acceptable",
        "out_of_distribution_clear", "clinical_context_available", "provenance_complete",
    )
    if any(not bool(record[field]) for field in evidence_fields):
        return "FAIL_CLOSED"

    if record["prior_study_required"] and not record["prior_study_available"]:
        return "REVIEW_REQUIRED"

    if record.get("automation_bias_risk", False) or (
        record["human_review_completed"] and not record["independent_image_access"]
    ):
        return "REVIEW_REQUIRED"

    if record["requested_disposition"] == "AUTONOMOUS_NORMAL" or record["operating_mode"] == "AUTONOMOUS_NEGATIVE_CLEARANCE":
        return "DENY_AUTONOMOUS_CLEARANCE"

    if record["operating_mode"] == "ASSISTIVE" and record["requested_disposition"] == "ASSISTIVE_OUTPUT":
        return "ADMIT_ASSISTIVE_USE"

    if record["operating_mode"] == "AI_FIRST_HUMAN_REVIEW":
        if not record["human_review_required"] or not record["human_review_completed"]:
            return "REVIEW_REQUIRED"
        return "ADMIT_AI_FIRST_WITH_MANDATORY_HUMAN_REVIEW"

    return "FAIL_CLOSED"


def validate_record(record: Dict[str, Any], case_id: str) -> List[str]:
    errors: List[str] = []
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        return [f"{case_id}: missing required fields: {', '.join(missing)}"]
    if record["decision"] not in DECISIONS:
        errors.append(f"{case_id}: invalid decision")
    if not isinstance(record["policy_ref"], str) or not record["policy_ref"]:
        errors.append(f"{case_id}: policy_ref must be non-empty")
    if not isinstance(record["delegation_ref"], str) or not record["delegation_ref"]:
        errors.append(f"{case_id}: delegation_ref must be non-empty")
    return errors


def main() -> int:
    required_paths = (FIXTURES, SCHEMA, FORMALISM, STATUS)
    missing_files = [str(path.relative_to(ROOT)) for path in required_paths if not path.exists()]
    if missing_files:
        print("AI-led radiology validation failed: missing " + ", ".join(missing_files), file=sys.stderr)
        return 1

    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        print("AI-led radiology validation failed: fixtures require non-empty cases", file=sys.stderr)
        return 1

    errors: List[str] = []
    receipts: List[Dict[str, str]] = []
    seen_ids = set()

    for case in cases:
        case_id = case.get("case_id")
        record = case.get("record")
        expected = case.get("expected_decision")
        if not isinstance(case_id, str) or not case_id:
            errors.append("fixture case missing non-empty case_id")
            continue
        if case_id in seen_ids:
            errors.append(f"duplicate case_id: {case_id}")
            continue
        seen_ids.add(case_id)
        if not isinstance(record, dict):
            errors.append(f"{case_id}: record must be an object")
            continue
        if expected not in DECISIONS:
            errors.append(f"{case_id}: invalid expected_decision")
            continue
        errors.extend(validate_record(record, case_id))
        actual = decide(record)
        if actual != expected:
            errors.append(f"{case_id}: expected {expected}, got {actual}")
        if record.get("decision") != expected:
            errors.append(f"{case_id}: recorded decision does not match expected decision")
        receipts.append({"case_id": case_id, "decision": actual, "record_sha256": canonical_hash(record)})

    observed = {receipt["decision"] for receipt in receipts}
    missing_decisions = DECISIONS - observed
    if missing_decisions:
        errors.append("fixture coverage missing decisions: " + ", ".join(sorted(missing_decisions)))

    if status.get("fixture_case_count") != len(cases):
        errors.append("status fixture_case_count does not match fixtures")
    if set(status.get("decision_classes", [])) != DECISIONS:
        errors.append("status decision_classes do not match validator decisions")
    if status.get("additional_active_workflow_created") is not False:
        errors.append("status must preserve single canonical workflow posture")
    if status.get("clinical_authority") is not False or status.get("execution_authority") is not False:
        errors.append("status must not claim clinical or execution authority")

    receipt = {
        "validator": "check_ai_led_radiology_execution.py",
        "result": "FAIL" if errors else "PASS",
        "case_count": len(receipts),
        "decision_coverage": sorted(observed),
        "fixture_sha256": canonical_hash(payload),
        "schema_sha256": hashlib.sha256(SCHEMA.read_bytes()).hexdigest(),
        "formalism_sha256": hashlib.sha256(FORMALISM.read_bytes()).hexdigest(),
        "status_sha256": canonical_hash(status),
        "receipts": receipts,
        "authority_boundary": {
            "clinical_authority": False,
            "execution_authority": False,
            "certification": False,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if errors:
        print("AI-led radiology validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
