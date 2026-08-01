#!/usr/bin/env python3
"""Validate TA-14 non-halting observation fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "static/reviews/ta14/fixtures/observation-cases.v0.1.json"

REQUIRED_CATEGORIES = {
    "authority",
    "receipt_trust",
    "object_binding",
    "atomic_commit",
    "execution_boundary",
    "refusal",
    "outcome",
    "neutral_review",
}
ALLOWED_STATES = {
    "BUILD_INTERNAL",
    "OBSERVE",
    "EVIDENCE_ABSENT_FAIL_CLOSED",
    "SIMULATED_ONLY",
    "VERIFIED_BOUNDED",
    "DISPUTED_REVIEWER_BURDEN",
    "COMPLETE",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not FIXTURES.is_file():
        fail(f"missing fixture file: {FIXTURES.relative_to(ROOT)}")

    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    if data.get("schema_version") != "0.1.0":
        fail("unexpected schema_version")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        fail("cases must be a non-empty list")

    ids: set[str] = set()
    categories: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail("every case requires a non-empty id")
        if case_id in ids:
            fail(f"duplicate case id: {case_id}")
        ids.add(case_id)

        category = case.get("category")
        if category not in REQUIRED_CATEGORIES:
            fail(f"unknown category for {case_id}: {category}")
        categories.add(category)

        state = case.get("expected_task_state")
        if state not in ALLOWED_STATES:
            fail(f"invalid expected_task_state for {case_id}: {state}")
        if state == "BLOCKED":
            fail(f"generic BLOCKED state prohibited: {case_id}")

        if case.get("development_halt") is not False:
            fail(f"fixture must not halt development: {case_id}")

        claim_effect = case.get("expected_claim_effect")
        if not isinstance(claim_effect, str) or not claim_effect:
            fail(f"missing expected_claim_effect: {case_id}")

    missing = REQUIRED_CATEGORIES - categories
    if missing:
        fail(f"missing required fixture categories: {sorted(missing)}")

    print(f"PASS: {len(cases)} TA-14 observation fixtures; development_halt=false for all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
