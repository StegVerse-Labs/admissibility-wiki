#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "discovery-governance-handoff-cases.json"
REQUIRED_NON_AUTHORITY = {
    "CONSENT", "STANDING", "AUTHORITY", "ADMISSIBILITY", "COMMITMENT",
    "EXECUTION_PERMISSION", "CERTIFICATION", "ENDORSEMENT",
}
REQUIRED_FIELDS = {
    "schema_version", "handoff_id", "recommendation_id", "discovery_system",
    "opportunity", "declared_context", "inferred_context", "provenance",
    "confidence_basis", "participants", "prerequisites", "boundaries",
    "unresolved_assumptions", "proposed_action", "destination_layer",
    "required_consent", "required_authority", "evidence_refs",
    "non_authority_declaration", "generated_at", "expires_at",
}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def evaluate(record: dict) -> str:
    if not REQUIRED_FIELDS.issubset(record):
        return "FAIL_CLOSED"
    if record.get("schema_version") != "discovery_governance_handoff.v1":
        return "FAIL_CLOSED"
    if not record.get("provenance") or not record.get("evidence_refs"):
        return "FAIL_CLOSED"
    if not record.get("participants") or not record.get("boundaries"):
        return "FAIL_CLOSED"
    declarations = set(record.get("non_authority_declaration", []))
    if not REQUIRED_NON_AUTHORITY.issubset(declarations):
        return "FAIL_CLOSED"
    try:
        if parse_time(record["expires_at"]) <= parse_time(record["generated_at"]):
            return "FAIL_CLOSED"
    except (TypeError, ValueError):
        return "FAIL_CLOSED"
    authority_assertions = set(record.get("authority_assertions", []))
    if authority_assertions & REQUIRED_NON_AUTHORITY:
        return "DENY"
    if record.get("unresolved_assumptions"):
        return "REVIEW_REQUIRED"
    return "HANDOFF_READY"


def main() -> int:
    failures: list[str] = []
    if not FIXTURES.exists():
        print("DISCOVERY GOVERNANCE HANDOFF: FAIL")
        print(f"- missing {FIXTURES.relative_to(ROOT)}")
        return 1
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    if not cases:
        failures.append("fixture set has no cases")
    for case in cases:
        actual = evaluate(case.get("record", {}))
        expected = case.get("expected")
        print(f"{case.get('case_id')}: {actual}")
        if actual != expected:
            failures.append(f"{case.get('case_id')} expected {expected}, got {actual}")
    required_outcomes = {"HANDOFF_READY", "REVIEW_REQUIRED", "DENY", "FAIL_CLOSED"}
    observed = {case.get("expected") for case in cases}
    if not required_outcomes.issubset(observed):
        failures.append("fixture set does not cover all deterministic outcomes")
    if failures:
        print("DISCOVERY GOVERNANCE HANDOFF: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE HANDOFF: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
