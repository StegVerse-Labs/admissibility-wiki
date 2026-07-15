#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "static" / "translation-records" / "disciplinary-translation-records.v0.1.json"
BINDINGS = ROOT / "static" / "formalisms" / "formalism-translation-bindings.v1.json"
FORMALISM_REGISTRY = ROOT / "static" / "formalisms" / "formalism-registry.v0.1.json"

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

REQUIRED_BINDING_FIELDS = {
    "translation_id",
    "target_formalism_ids",
    "relationship",
    "proof_effect",
    "standing_effect",
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
    for path in [RECORDS, BINDINGS, FORMALISM_REGISTRY]:
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    data = json.loads(RECORDS.read_text(encoding="utf-8"))
    bindings = json.loads(BINDINGS.read_text(encoding="utf-8"))
    formalism_registry = json.loads(FORMALISM_REGISTRY.read_text(encoding="utf-8"))

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

    if bindings.get("schema") != "admissibility_wiki_formalism_translation_bindings.v1":
        fail("unexpected formalism translation binding schema")
    if bindings.get("translation_registry") != "static/translation-records/disciplinary-translation-records.v0.1.json":
        fail("translation binding registry reference mismatch")
    if bindings.get("formalism_registry") != "static/formalisms/formalism-registry.v0.1.json":
        fail("formalism binding registry reference mismatch")
    if "do not define canonical formalisms" not in bindings.get("authority_boundary", ""):
        fail("formalism translation binding must preserve canonical-authority boundary")

    formalism_ids = {
        record.get("formalism_id")
        for record in formalism_registry.get("records", [])
        if isinstance(record.get("formalism_id"), str)
    }
    binding_entries = bindings.get("entries", [])
    if not isinstance(binding_entries, list):
        fail("formalism translation bindings entries must be a list")

    bound_ids: set[str] = set()
    target_ids: set[str] = set()
    for entry in binding_entries:
        missing = REQUIRED_BINDING_FIELDS - set(entry)
        if missing:
            fail(f"binding {entry.get('translation_id')} missing fields: {sorted(missing)}")
        translation_id = entry.get("translation_id")
        if not isinstance(translation_id, str) or translation_id in bound_ids:
            fail(f"invalid or duplicate binding translation_id: {translation_id}")
        if translation_id not in seen_ids:
            fail(f"binding references unknown translation record: {translation_id}")
        bound_ids.add(translation_id)

        targets = entry.get("target_formalism_ids")
        if not isinstance(targets, list) or not targets:
            fail(f"binding {translation_id} must include target formalism IDs")
        for target in targets:
            if target not in formalism_ids:
                fail(f"binding {translation_id} references unknown formalism: {target}")
            target_ids.add(target)

        require_nonempty_string(translation_id, "relationship", entry.get("relationship"))
        if entry.get("proof_effect") != "NONE":
            fail(f"binding {translation_id} must not create proof effect")
        if entry.get("standing_effect") != "NONE":
            fail(f"binding {translation_id} must not create standing effect")

    if bound_ids != seen_ids:
        fail("translation binding coverage must exactly match translation records")

    counts = bindings.get("counts", {})
    if counts.get("translation_records") != len(seen_ids):
        fail("translation_records count is stale")
    if counts.get("bound_translation_records") != len(bound_ids):
        fail("bound_translation_records count is stale")
    if counts.get("unbound_translation_records") != 0:
        fail("unbound_translation_records must be zero")
    if counts.get("target_formalisms") != len(target_ids):
        fail("target_formalisms count is stale")

    print(f"TRANSLATION RECORDS: PASS - {len(records)} records validated")
    print(f"formalism_translation_bindings={len(bound_ids)}")
    print(f"target_formalisms={len(target_ids)}")
    print("proof_effect=NONE")
    print("standing_effect=NONE")


if __name__ == "__main__":
    main()
