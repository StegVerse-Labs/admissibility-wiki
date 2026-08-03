#!/usr/bin/env python3
"""Validate the admissible structural invariants research note and candidate record."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "research" / "admissible-structural-invariants.md"
RECORD = ROOT / "static" / "research" / "admissible-structural-invariants.v0.1.json"
SIDEBAR = ROOT / "sidebars.js"

REQUIRED_DECISIONS = {"ALLOW", "DENY", "REVIEW_REQUIRED", "FAIL_CLOSED"}
REQUIRED_PROPOSITIONS = {"ASI-P1", "ASI-P2", "ASI-P3", "ASI-P4", "ASI-P5"}
REQUIRED_FAILURES = {
    "PRESERVED_BUT_OBSOLETE",
    "PRESERVED_BUT_PURPOSE_INVERTING",
    "PRESERVED_BUT_UNRECOVERABLE",
    "PRESERVED_BUT_RELATIONALLY_INADMISSIBLE",
    "PRESERVED_BUT_UNRECONSTRUCTABLE",
}
REQUIRED_NOTE_PHRASES = {
    "preservation != legitimacy",
    "Structural invariant preservation: NOT SUFFICIENT FOR GOVERNED CONTINUITY",
    "Novelty: NOT DETERMINED",
    "Admissible Structural Invariant",
    "Invariant Succession",
    "Multi-Entity Extension",
}


def fail(message: str) -> None:
    raise SystemExit(f"ADMISSIBLE STRUCTURAL INVARIANTS: FAIL - {message}")


def main() -> None:
    if not NOTE.is_file():
        fail(f"missing note: {NOTE.relative_to(ROOT)}")
    if not RECORD.is_file():
        fail(f"missing record: {RECORD.relative_to(ROOT)}")
    if not SIDEBAR.is_file():
        fail("missing sidebars.js")

    note_text = NOTE.read_text(encoding="utf-8")
    sidebar_text = SIDEBAR.read_text(encoding="utf-8")
    missing_phrases = sorted(phrase for phrase in REQUIRED_NOTE_PHRASES if phrase not in note_text)
    if missing_phrases:
        fail(f"note missing required phrases: {missing_phrases}")

    if "research/admissible-structural-invariants" not in sidebar_text:
        fail("research note is not present in the Research sidebar")

    try:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"record is invalid JSON: {exc}")

    if record.get("schema_version") != "0.1.0":
        fail("schema_version must be 0.1.0")
    if record.get("status") != "FORMALIZATION_CANDIDATE":
        fail("status must remain FORMALIZATION_CANDIDATE")
    if record.get("novelty_status") != "NOT_DETERMINED":
        fail("novelty_status must remain NOT_DETERMINED until reviewed")
    if record.get("execution_authority") is not False:
        fail("research record must not claim execution authority")

    decisions = set(record.get("decision_enum", []))
    if decisions != REQUIRED_DECISIONS:
        fail(f"decision enum mismatch: {sorted(decisions)}")

    proposition_ids = {
        item.get("id") for item in record.get("testable_propositions", []) if isinstance(item, dict)
    }
    if proposition_ids != REQUIRED_PROPOSITIONS:
        fail(f"testable proposition mismatch: {sorted(proposition_ids)}")

    failure_classes = set(record.get("failure_classes", []))
    if failure_classes != REQUIRED_FAILURES:
        fail(f"failure class mismatch: {sorted(failure_classes)}")

    required_fields = record.get("required_decision_record_fields", [])
    if len(required_fields) != len(set(required_fields)):
        fail("required decision-record fields contain duplicates")
    if len(required_fields) < 20:
        fail("decision record is missing required governance dimensions")

    print(
        "ADMISSIBLE STRUCTURAL INVARIANTS: PASS - "
        "research note, candidate record, sidebar binding, decisions, failures, and propositions validated"
    )


if __name__ == "__main__":
    main()
