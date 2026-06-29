#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "static" / "translation-records" / "disciplinary-translation-records.v0.1.json"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "record_state",
    "source_authority_boundary",
    "records",
}

REQUIRED_RECORD_FIELDS = {
    "translation_id",
    "source_discipline",
    "source_reference",
    "native_term",
    "native_meaning",
    "transition_role",
    "boundary_condition",
    "constraint_reference",
    "admissibility_question",
    "evidence_posture",
    "review_posture",
    "non_claims",
    "receipt_reference",
}

ALLOWED_REVIEW_POSTURES = {
    "proposed",
    "mapped",
    "disputed",
    "accepted",
    "deferred",
    "escalated",
}

ALLOWED_EVIDENCE_POSTURES = {
    "none",
    "partial",
    "present",
    "sufficient",
    "conflicting",
    "stale",
    "unknown",
}


def fail(message: str) -> None:
    raise SystemExit(f"TRANSLATION RECORDS: FAIL - {message}")


def require_nonempty_string(record_id: str, key: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"record {record_id} field {key} must be a non-empty string")


def main() -> None:
    if not RECORDS.exists():
        fail(f"missing {RECORDS.relative_to(ROOT)}")

    data = json.loads(RECORDS.read_text(encoding="utf-8"))

    missing_top = REQUIRED_TOP_LEVEL - set(data)
    if missing_top:
        fail(f"missing top-level fields: {sorted(missing_top)}")

    boundary = data["source_authority_boundary"]
    require_nonempty_string("top-level", "source_authority_boundary", boundary)
    if "do not prove" not in boundary.lower() and "does not prove" not in boundary.lower():
        fail("source_authority_boundary must preserve a proof non-claim")

    records = data["records"]
    if not isinstance(records, list) or not records:
        fail("records must be a non-empty list")

    seen_ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            fail("each record must be an object")
        record_id = str(record.get("translation_id", "<missing>"))

        missing = REQUIRED_RECORD_FIELDS - set(record)
        if missing:
            fail(f"record {record_id} missing fields: {sorted(missing)}")

        if record_id in seen_ids:
            fail(f"duplicate translation_id: {record_id}")
        seen_ids.add(record_id)

        for key in REQUIRED_RECORD_FIELDS - {"receipt_reference"}:
            require_nonempty_string(record_id, key, record[key])

        if record["review_posture"] not in ALLOWED_REVIEW_POSTURES:
            fail(f"record {record_id} has invalid review_posture: {record['review_posture']}")

        if record["evidence_posture"] not in ALLOWED_EVIDENCE_POSTURES:
            fail(f"record {record_id} has invalid evidence_posture: {record['evidence_posture']}")

        non_claims = record["non_claims"].lower()
        if "not" not in non_claims and "does not" not in non_claims:
            fail(f"record {record_id} must include an explicit non-claim")

    print(f"TRANSLATION RECORDS: PASS - {len(records)} records validated")


if __name__ == "__main__":
    main()
