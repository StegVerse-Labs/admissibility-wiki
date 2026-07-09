#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CRITERIA_DOC = ROOT / "docs" / "external-frameworks" / "intake-promotion-criteria.md"
CRITERIA = ROOT / "docs" / "external-frameworks" / "intake-promotion-criteria.json"
RECORDS = ROOT / "docs" / "external-frameworks" / "promoted-intake-records.v0.1.json"
EXPANDED = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.json"

REQUIRED_GATES = {
    "canonical_source",
    "source_version",
    "published_scope",
    "published_non_claims",
    "artifact_type",
    "relationship_class",
    "benchmark_relevance",
    "authority_boundary",
    "evidence_posture",
}

ALLOWED_STATES = {
    "source_required",
    "sourced_intake",
    "page_candidate",
    "mapping_candidate",
    "fixture_candidate",
    "deferred",
}

ALLOWED_RELATIONSHIPS = {"synonymous", "adjacent", "new", "unresolved"}
ALLOWED_EVIDENCE = {"source_only", "implementation_evidence", "observed_behavior", "interoperability_evidence"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [CRITERIA_DOC, CRITERIA, RECORDS, EXPANDED]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")
    if failures:
        print("EXTERNAL FRAMEWORK INTAKE PROMOTION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = CRITERIA_DOC.read_text(encoding="utf-8")
    criteria = load_json(CRITERIA)
    records = load_json(RECORDS)
    expanded = load_json(EXPANDED)

    if criteria.get("artifact_type") != "external_framework_intake_promotion_criteria":
        failures.append("criteria artifact type mismatch")
    if records.get("artifact_type") != "external_framework_promoted_intake_records":
        failures.append("records artifact type mismatch")
    if criteria.get("schema_version") != "0.1" or records.get("schema_version") != "0.1":
        failures.append("schema version mismatch")

    posture = criteria.get("posture", {})
    for key, value in posture.items():
        if value is not False:
            failures.append(f"criteria posture must be false: {key}")

    for gate in sorted(REQUIRED_GATES):
        if gate not in criteria.get("required_gates", []):
            failures.append(f"missing required gate: {gate}")
    for state in criteria.get("allowed_promotion_states", []):
        if state not in ALLOWED_STATES:
            failures.append(f"unexpected promotion state: {state}")
    for rel in criteria.get("allowed_relationship_classes", []):
        if rel not in ALLOWED_RELATIONSHIPS:
            failures.append(f"unexpected relationship class: {rel}")
    for evidence in criteria.get("allowed_evidence_postures", []):
        if evidence not in ALLOWED_EVIDENCE:
            failures.append(f"unexpected evidence posture: {evidence}")

    candidate_ids = {c.get("candidate_id") for c in expanded.get("candidates", []) if isinstance(c, dict)}
    required_fields = set(criteria.get("required_promotion_record_fields", []))
    for record in records.get("records", []):
        if not isinstance(record, dict):
            failures.append("promotion record must be object")
            continue
        candidate_id = record.get("candidate_id")
        if candidate_id not in candidate_ids:
            failures.append(f"promoted record candidate missing from expanded intake: {candidate_id}")
        for field in required_fields:
            if not record.get(field):
                failures.append(f"promoted record missing {field}: {candidate_id}")
        if record.get("relationship_class") not in ALLOWED_RELATIONSHIPS:
            failures.append(f"invalid relationship class: {candidate_id}")
        if record.get("promotion_state") not in ALLOWED_STATES:
            failures.append(f"invalid promotion state: {candidate_id}")
        if record.get("evidence_posture") not in ALLOWED_EVIDENCE:
            failures.append(f"invalid evidence posture: {candidate_id}")
        authority = record.get("authority_boundary", {})
        if not isinstance(authority, dict) or not authority:
            failures.append(f"missing authority boundary object: {candidate_id}")
        for key, value in authority.items():
            if value is not False:
                failures.append(f"authority boundary must be false: {candidate_id}:{key}")

    non_claims = records.get("non_claims", {})
    for key, value in non_claims.items():
        if value is not False:
            failures.append(f"records non-claim must be false: {key}")

    for phrase in ["promotion != certification", "promotion != execution authority", "Promotion means the candidate has enough source material"]:
        if phrase not in doc:
            failures.append(f"criteria doc missing phrase: {phrase}")

    print("EXTERNAL FRAMEWORK INTAKE PROMOTION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
