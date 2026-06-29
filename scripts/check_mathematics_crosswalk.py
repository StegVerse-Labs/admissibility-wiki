#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION_RECORDS = ROOT / "static" / "translation-records" / "disciplinary-translation-records.v0.1.json"
MATH_CROSSWALK = ROOT / "static" / "translation-records" / "mathematics-crosswalk.v0.1.json"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "record_state",
    "source_authority_boundary",
    "rows",
}

REQUIRED_ROW_FIELDS = {
    "crosswalk_id",
    "equation_or_object",
    "source_framing",
    "transition_table_role",
    "translation_record_ids",
    "review_posture",
    "non_claims",
}

ALLOWED_REVIEW_POSTURES = {
    "proposed",
    "mapped",
    "disputed",
    "accepted",
    "deferred",
    "escalated",
}


def fail(message: str) -> None:
    raise SystemExit(f"MATHEMATICS CROSSWALK: FAIL - {message}")


def require_nonempty_string(row_id: str, key: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"row {row_id} field {key} must be a non-empty string")


def main() -> None:
    if not TRANSLATION_RECORDS.exists():
        fail(f"missing {TRANSLATION_RECORDS.relative_to(ROOT)}")
    if not MATH_CROSSWALK.exists():
        fail(f"missing {MATH_CROSSWALK.relative_to(ROOT)}")

    translation_data = json.loads(TRANSLATION_RECORDS.read_text(encoding="utf-8"))
    known_translation_ids = {
        record["translation_id"]
        for record in translation_data.get("records", [])
        if isinstance(record, dict) and "translation_id" in record
    }
    if not known_translation_ids:
        fail("no known translation record IDs found")

    data = json.loads(MATH_CROSSWALK.read_text(encoding="utf-8"))
    missing_top = REQUIRED_TOP_LEVEL - set(data)
    if missing_top:
        fail(f"missing top-level fields: {sorted(missing_top)}")

    boundary = data["source_authority_boundary"]
    require_nonempty_string("top-level", "source_authority_boundary", boundary)
    if "do not prove" not in boundary.lower() and "does not prove" not in boundary.lower():
        fail("source_authority_boundary must preserve a proof non-claim")

    rows = data["rows"]
    if not isinstance(rows, list) or not rows:
        fail("rows must be a non-empty list")

    seen_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            fail("each row must be an object")
        row_id = str(row.get("crosswalk_id", "<missing>"))

        missing = REQUIRED_ROW_FIELDS - set(row)
        if missing:
            fail(f"row {row_id} missing fields: {sorted(missing)}")

        if row_id in seen_ids:
            fail(f"duplicate crosswalk_id: {row_id}")
        seen_ids.add(row_id)

        for key in REQUIRED_ROW_FIELDS - {"translation_record_ids"}:
            require_nonempty_string(row_id, key, row[key])

        if row["review_posture"] not in ALLOWED_REVIEW_POSTURES:
            fail(f"row {row_id} has invalid review_posture: {row['review_posture']}")

        translation_ids = row["translation_record_ids"]
        if not isinstance(translation_ids, list) or not translation_ids:
            fail(f"row {row_id} translation_record_ids must be a non-empty list")

        for translation_id in translation_ids:
            if translation_id not in known_translation_ids:
                fail(f"row {row_id} references unknown translation record ID: {translation_id}")

        non_claims = row["non_claims"].lower()
        if "not" not in non_claims and "does not" not in non_claims:
            fail(f"row {row_id} must include an explicit non-claim")

    print(f"MATHEMATICS CROSSWALK: PASS - {len(rows)} rows validated")


if __name__ == "__main__":
    main()
