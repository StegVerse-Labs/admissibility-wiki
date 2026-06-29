#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION_RECORDS = ROOT / "static" / "translation-records" / "disciplinary-translation-records.v0.1.json"
MATH_CROSSWALK = ROOT / "static" / "translation-records" / "mathematics-crosswalk.v0.1.json"
EXTERNAL_RECORDS = ROOT / "static" / "translation-records" / "external-physics-translation-records.v0.1.json"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "record_state",
    "source_authority_boundary",
    "sources",
    "records",
}

REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "source_name",
    "source_title_status",
    "source_type",
    "evidence_posture",
    "review_posture",
    "non_claims",
}

REQUIRED_RECORD_FIELDS = {
    "external_record_id",
    "source_id",
    "native_term",
    "native_meaning",
    "transition_table_role",
    "related_translation_record_ids",
    "related_math_crosswalk_ids",
    "evidence_posture",
    "review_posture",
    "source_boundary",
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
    raise SystemExit(f"EXTERNAL PHYSICS TRANSLATION RECORDS: FAIL - {message}")


def require_nonempty_string(record_id: str, key: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{record_id} field {key} must be a non-empty string")


def require_nonclaim(record_id: str, value: object) -> None:
    require_nonempty_string(record_id, "non_claims", value)
    text = str(value).lower()
    if "not" not in text and "does not" not in text:
        fail(f"{record_id} must include an explicit non-claim")


def main() -> None:
    for path in (TRANSLATION_RECORDS, MATH_CROSSWALK, EXTERNAL_RECORDS):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    translation_data = json.loads(TRANSLATION_RECORDS.read_text(encoding="utf-8"))
    known_translation_ids = {
        record["translation_id"]
        for record in translation_data.get("records", [])
        if isinstance(record, dict) and "translation_id" in record
    }

    math_data = json.loads(MATH_CROSSWALK.read_text(encoding="utf-8"))
    known_math_ids = {
        row["crosswalk_id"]
        for row in math_data.get("rows", [])
        if isinstance(row, dict) and "crosswalk_id" in row
    }

    if not known_translation_ids:
        fail("no known translation record IDs found")
    if not known_math_ids:
        fail("no known mathematics crosswalk IDs found")

    data = json.loads(EXTERNAL_RECORDS.read_text(encoding="utf-8"))
    missing_top = REQUIRED_TOP_LEVEL - set(data)
    if missing_top:
        fail(f"missing top-level fields: {sorted(missing_top)}")

    boundary = data["source_authority_boundary"]
    require_nonempty_string("top-level", "source_authority_boundary", boundary)
    if "do not prove" not in boundary.lower() and "does not prove" not in boundary.lower():
        fail("source_authority_boundary must preserve a proof non-claim")

    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        fail("sources must be a non-empty list")

    seen_source_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            fail("each source must be an object")
        source_id = str(source.get("source_id", "<missing>"))
        missing = REQUIRED_SOURCE_FIELDS - set(source)
        if missing:
            fail(f"source {source_id} missing fields: {sorted(missing)}")
        if source_id in seen_source_ids:
            fail(f"duplicate source_id: {source_id}")
        seen_source_ids.add(source_id)
        for key in REQUIRED_SOURCE_FIELDS - {"non_claims"}:
            require_nonempty_string(source_id, key, source[key])
        if source["review_posture"] not in ALLOWED_REVIEW_POSTURES:
            fail(f"source {source_id} has invalid review_posture: {source['review_posture']}")
        if source["evidence_posture"] not in ALLOWED_EVIDENCE_POSTURES:
            fail(f"source {source_id} has invalid evidence_posture: {source['evidence_posture']}")
        require_nonclaim(source_id, source["non_claims"])

    records = data["records"]
    if not isinstance(records, list) or not records:
        fail("records must be a non-empty list")

    seen_record_ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            fail("each record must be an object")
        record_id = str(record.get("external_record_id", "<missing>"))
        missing = REQUIRED_RECORD_FIELDS - set(record)
        if missing:
            fail(f"record {record_id} missing fields: {sorted(missing)}")
        if record_id in seen_record_ids:
            fail(f"duplicate external_record_id: {record_id}")
        seen_record_ids.add(record_id)

        for key in REQUIRED_RECORD_FIELDS - {"related_translation_record_ids", "related_math_crosswalk_ids", "non_claims"}:
            require_nonempty_string(record_id, key, record[key])

        if record["source_id"] not in seen_source_ids:
            fail(f"record {record_id} references unknown source_id: {record['source_id']}")
        if record["review_posture"] not in ALLOWED_REVIEW_POSTURES:
            fail(f"record {record_id} has invalid review_posture: {record['review_posture']}")
        if record["evidence_posture"] not in ALLOWED_EVIDENCE_POSTURES:
            fail(f"record {record_id} has invalid evidence_posture: {record['evidence_posture']}")

        translation_ids = record["related_translation_record_ids"]
        if not isinstance(translation_ids, list) or not translation_ids:
            fail(f"record {record_id} related_translation_record_ids must be a non-empty list")
        for translation_id in translation_ids:
            if translation_id not in known_translation_ids:
                fail(f"record {record_id} references unknown translation record ID: {translation_id}")

        math_ids = record["related_math_crosswalk_ids"]
        if not isinstance(math_ids, list) or not math_ids:
            fail(f"record {record_id} related_math_crosswalk_ids must be a non-empty list")
        for math_id in math_ids:
            if math_id not in known_math_ids:
                fail(f"record {record_id} references unknown mathematics crosswalk ID: {math_id}")

        require_nonclaim(record_id, record["non_claims"])

    print(f"EXTERNAL PHYSICS TRANSLATION RECORDS: PASS - {len(sources)} sources and {len(records)} records validated")


if __name__ == "__main__":
    main()
