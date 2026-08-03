#!/usr/bin/env python3
"""Validate admissible structural invariant counterexamples and succession schema."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "static" / "research" / "examples" / "admissible-structural-invariant-cases.v0.1.json"
SCHEMA = ROOT / "static" / "research" / "admissible-invariant-succession.schema.v0.1.json"
DECISIONS = {"ALLOW", "DENY", "REVIEW_REQUIRED", "FAIL_CLOSED"}
FAILURES = {
    "PRESERVED_BUT_OBSOLETE",
    "PRESERVED_BUT_PURPOSE_INVERTING",
    "PRESERVED_BUT_UNRECOVERABLE",
    "PRESERVED_BUT_RELATIONALLY_INADMISSIBLE",
    "PRESERVED_BUT_UNRECONSTRUCTABLE",
}
REQUIRED_CASES = {
    "ASI-C01-PRESERVED-ALLOW", "ASI-C02-OBSOLETE", "ASI-C03-PURPOSE-INVERTING",
    "ASI-C04-UNRECOVERABLE", "ASI-C05-RELATIONAL-CONFLICT", "ASI-C06-UNRECONSTRUCTABLE",
    "ASI-C07-ADMISSIBLE-SUCCESSION"
}


def fail(message: str) -> None:
    raise SystemExit(f"ADMISSIBLE INVARIANT CASES: FAIL - {message}")


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.name}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.name} must contain an object")
    return value


def main() -> None:
    fixtures = load(CASES)
    schema = load(SCHEMA)
    if fixtures.get("execution_authority") is not False:
        fail("fixtures must not claim execution authority")
    cases = fixtures.get("cases", [])
    ids = {case.get("case_id") for case in cases if isinstance(case, dict)}
    if ids != REQUIRED_CASES:
        fail(f"case coverage mismatch: {sorted(ids)}")
    observed_failures = set()
    for case in cases:
        decision = case.get("expected_decision")
        failure = case.get("expected_failure_class")
        if decision not in DECISIONS:
            fail(f"invalid decision in {case.get('case_id')}")
        if failure is not None:
            if failure not in FAILURES:
                fail(f"invalid failure class in {case.get('case_id')}")
            observed_failures.add(failure)
        if case.get("preservation_result") == "SUCCESSION" and not case.get("succession_record_required"):
            fail("succession case must require a succession record")
    if observed_failures != FAILURES:
        fail(f"failure coverage mismatch: {sorted(observed_failures)}")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("succession schema must use JSON Schema 2020-12")
    required = set(schema.get("required", []))
    for name in {"predecessor_invariant", "successor_invariant", "affected_entity_dispositions", "receipt_chain_reference", "execution_authority"}:
        if name not in required:
            fail(f"succession schema missing required field {name}")
    execution = schema.get("properties", {}).get("execution_authority", {})
    if execution.get("const") is not False:
        fail("succession research schema must not grant execution authority")
    print("ADMISSIBLE INVARIANT CASES: PASS - seven cases, five failure classes, and succession schema validated")


if __name__ == "__main__":
    main()
