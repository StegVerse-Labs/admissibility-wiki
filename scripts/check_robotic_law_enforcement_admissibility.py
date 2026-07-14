#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "static" / "status" / "robotic-law-enforcement-adoption-status.json"
SCHEMA_PATH = ROOT / "static" / "schemas" / "robotic-law-enforcement-deployment-admissibility.schema.json"
FIXTURES_PATH = ROOT / "tests" / "fixtures" / "robotic-law-enforcement-admissibility-cases.json"
DOCTRINE_PATH = ROOT / "docs" / "governance" / "robotic-law-enforcement-adoption-boundary.md"
HANDOFF_PATH = ROOT / "docs" / "ROBOTIC_LAW_ENFORCEMENT_ADOPTION_MIRROR_HANDOFF.md"

REQUIRED_RECORD_FIELDS = {
    "record_id",
    "deployment_class",
    "requested_capabilities",
    "human_authority",
    "policy_reference",
    "validity_window",
    "shutdown_path",
    "pre_consequence_refusal_point",
    "procurement_disclosure",
    "auditability",
    "decision",
    "reasons",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def expected_decision(record: dict) -> str:
    capabilities = set(record.get("requested_capabilities", []))
    procurement = record.get("procurement_disclosure") or {}
    justification = record.get("justification") or {}
    auditability = record.get("auditability") or {}
    validity = record.get("validity_window") or {}

    prohibited = {
        "autonomous_lethal_targeting",
        "autonomous_force_initiation",
    }
    if capabilities & prohibited:
        return "DENY"
    if procurement.get("compensation_tied_to_enforcement_outputs") is True:
        return "DENY"
    if justification.get("human_failure_only") is True:
        return "DENY"

    unresolved = (
        not record.get("human_authority")
        or not record.get("policy_reference")
        or not record.get("shutdown_path")
        or record.get("pre_consequence_refusal_point") is not True
        or procurement.get("complete") is not True
        or auditability.get("consequential_review_available") is not True
        or auditability.get("force_event_receipts") is not True
        or auditability.get("operator_receipts") is not True
        or validity.get("expires_at") is None
    )
    if unresolved:
        return "FAIL_CLOSED"

    return "ALLOW"


def main() -> int:
    failures: list[str] = []

    for path in (STATUS_PATH, SCHEMA_PATH, FIXTURES_PATH, DOCTRINE_PATH, HANDOFF_PATH):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}", failures)

    if failures:
        print("ROBOTIC LAW ENFORCEMENT ADMISSIBILITY: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        fixture_doc = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("ROBOTIC LAW ENFORCEMENT ADMISSIBILITY: FAIL")
        print(f"- invalid JSON artifact: {exc}")
        return 1

    if status.get("goal_id") != "robotic-law-enforcement-adoption-boundary":
        fail("unexpected goal_id", failures)
    if status.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("unexpected repository", failures)
    if set(status.get("decision_outcomes", [])) != {"ALLOW", "DENY", "FAIL_CLOSED"}:
        fail("decision outcomes must cover ALLOW, DENY, and FAIL_CLOSED", failures)
    if status.get("manual_task_required") is not False:
        fail("manual_task_required must remain false", failures)
    if status.get("downstream_mutation_authority") is not False:
        fail("downstream mutation authority must remain false", failures)

    schema_required = set(schema.get("required", []))
    if not REQUIRED_RECORD_FIELDS.issubset(schema_required):
        missing = sorted(REQUIRED_RECORD_FIELDS - schema_required)
        fail(f"schema missing required fields: {', '.join(missing)}", failures)

    cases = fixture_doc.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("fixtures must contain a non-empty cases list", failures)
        cases = []

    observed = set()
    for case in cases:
        name = case.get("name", "unnamed")
        expected = case.get("expected")
        record = case.get("record")
        if not isinstance(record, dict):
            fail(f"{name}: record must be an object", failures)
            continue
        missing = REQUIRED_RECORD_FIELDS - set(record)
        if missing:
            fail(f"{name}: missing record fields: {', '.join(sorted(missing))}", failures)
            continue
        calculated = expected_decision(record)
        observed.add(calculated)
        if expected != calculated:
            fail(f"{name}: fixture expected {expected}, calculated {calculated}", failures)
        if record.get("decision") != calculated:
            fail(f"{name}: record decision {record.get('decision')} does not match {calculated}", failures)
        if not isinstance(record.get("reasons"), list) or not record.get("reasons"):
            fail(f"{name}: reasons must be non-empty", failures)

    if observed != {"ALLOW", "DENY", "FAIL_CLOSED"}:
        fail("fixtures must exercise ALLOW, DENY, and FAIL_CLOSED", failures)

    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    for marker in (
        "autonomous lethal",
        "Human failure is not replacement authority",
        "Crisis exploitation",
        "procurement",
        "pre-consequence refusal",
    ):
        if marker.lower() not in doctrine.lower():
            fail(f"doctrine missing marker: {marker}", failures)

    if failures:
        print("ROBOTIC LAW ENFORCEMENT ADMISSIBILITY: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ROBOTIC LAW ENFORCEMENT ADMISSIBILITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
