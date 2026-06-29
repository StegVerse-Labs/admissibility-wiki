#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_RECORDS = ROOT / "static" / "translation-records" / "external-physics-translation-records.v0.1.json"
BIBLIOGRAPHIC_INTAKE = ROOT / "static" / "translation-records" / "external-bibliographic-intake.v0.1.json"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "record_state",
    "authority_boundary",
    "required_fields",
    "records",
}

REQUIRED_RECORD_FIELDS = {
    "bibliographic_id",
    "source_id",
    "source_title",
    "creator_or_author_posture",
    "publication_or_source_posture",
    "source_locator",
    "access_posture",
    "evidence_posture",
    "review_posture",
    "linked_external_record_ids",
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
    raise SystemExit(f"EXTERNAL BIBLIOGRAPHIC INTAKE: FAIL - {message}")


def require_nonempty_string(record_id: str, key: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{record_id} field {key} must be a non-empty string")


def require_nonclaim(record_id: str, value: object) -> None:
    require_nonempty_string(record_id, "non_claims", value)
    text = str(value).lower()
    if "not" not in text and "does not" not in text:
        fail(f"{record_id} must include an explicit non-claim")


def main() -> None:
    for path in (EXTERNAL_RECORDS, BIBLIOGRAPHIC_INTAKE):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    external_data = json.loads(EXTERNAL_RECORDS.read_text(encoding="utf-8"))
    known_source_ids = {
        source["source_id"]
        for source in external_data.get("sources", [])
        if isinstance(source, dict) and "source_id" in source
    }
    known_external_record_ids = {
        record["external_record_id"]
        for record in external_data.get("records", [])
        if isinstance(record, dict) and "external_record_id" in record
    }
    if not known_source_ids:
        fail("no known external source IDs found")
    if not known_external_record_ids:
        fail("no known external record IDs found")

    data = json.loads(BIBLIOGRAPHIC_INTAKE.read_text(encoding="utf-8"))
    missing_top = REQUIRED_TOP_LEVEL - set(data)
    if missing_top:
        fail(f"missing top-level fields: {sorted(missing_top)}")

    boundary = data["authority_boundary"]
    require_nonempty_string("top-level", "authority_boundary", boundary)
    if "do not" not in boundary.lower() and "does not" not in boundary.lower():
        fail("authority_boundary must preserve an explicit non-claim")

    declared_required = set(data["required_fields"])
    missing_declared = REQUIRED_RECORD_FIELDS - declared_required
    if missing_declared:
        fail(f"required_fields does not declare: {sorted(missing_declared)}")

    records = data["records"]
    if not isinstance(records, list) or not records:
        fail("records must be a non-empty list")

    seen_ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            fail("each record must be an object")
        record_id = str(record.get("bibliographic_id", "<missing>"))
        missing = REQUIRED_RECORD_FIELDS - set(record)
        if missing:
            fail(f"record {record_id} missing fields: {sorted(missing)}")
        if record_id in seen_ids:
            fail(f"duplicate bibliographic_id: {record_id}")
        seen_ids.add(record_id)

        for key in REQUIRED_RECORD_FIELDS - {"linked_external_record_ids", "non_claims"}:
            require_nonempty_string(record_id, key, record[key])

        if record["source_id"] not in known_source_ids:
            fail(f"record {record_id} references unknown source_id: {record['source_id']}")
        if record["review_posture"] not in ALLOWED_REVIEW_POSTURES:
            fail(f"record {record_id} has invalid review_posture: {record['review_posture']}")
        if record["evidence_posture"] not in ALLOWED_EVIDENCE_POSTURES:
            fail(f"record {record_id} has invalid evidence_posture: {record['evidence_posture']}")

        linked_ids = record["linked_external_record_ids"]
        if not isinstance(linked_ids, list) or not linked_ids:
            fail(f"record {record_id} linked_external_record_ids must be a non-empty list")
        for linked_id in linked_ids:
            if linked_id not in known_external_record_ids:
                fail(f"record {record_id} references unknown external record ID: {linked_id}")

        require_nonclaim(record_id, record["non_claims"])

    print(f"EXTERNAL BIBLIOGRAPHIC INTAKE: PASS - {len(records)} records validated")


if __name__ == "__main__":
    main()
