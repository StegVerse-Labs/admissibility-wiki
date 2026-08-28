#!/usr/bin/env python3
"""Validate bounded public external-health-guidance research projection."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "health-guidance" / "external-health-guidance-quality.v1.json"
PAGE = ROOT / "docs" / "health-guidance" / "external-health-guidance-quality.md"

ALLOWED_CLASSIFICATIONS = {
    "CONFIRMED_CURRENT",
    "CONFIRMED_DISCREPANCY",
    "OUTDATED_REFERENCE",
    "OVERSIMPLIFIED",
    "AMBIGUOUS",
    "PROGRAM_SPECIFIC_CONVENTION",
    "REQUIRES_MORE_EVIDENCE",
    "CORRECTED_BY_SOURCE",
}
PROHIBITED_KEYS = {
    "participant_name",
    "patient_name",
    "member_id",
    "account_id",
    "prescription_number",
    "rx_number",
    "medical_record_number",
    "date_of_birth",
}


def fail(message: str) -> None:
    raise SystemExit(f"PUBLIC HEALTH GUIDANCE QUALITY: FAIL — {message}")


def walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")

    if data.get("schema_version") != "public.health-guidance-quality.v1":
        fail("unexpected schema_version")
    if data.get("issue") != 109:
        fail("record must remain bound to issue #109")
    if data.get("posture") != "QUALITY_IMPROVEMENT_RECOMMENDATION_NOT_COMPLAINT":
        fail("quality-improvement posture changed")
    if data.get("source_program", {}).get("participant_identifying_information_included") is not False:
        fail("public record must explicitly exclude participant-identifying information")

    boundary = data.get("authority_boundary", {})
    if any(boundary.get(key) is not False for key in (
        "clinical_diagnosis", "regulatory_finding", "proof_of_harm",
        "certification", "complaint_disposition"
    )):
        fail("authority boundary cannot be promoted")

    found_prohibited = sorted(PROHIBITED_KEYS.intersection(set(walk_keys(data))))
    if found_prohibited:
        fail(f"prohibited private-field keys present: {found_prohibited}")

    source_ids = [source["source_id"] for source in data.get("sources", [])]
    if len(source_ids) != len(set(source_ids)):
        fail("source_id values must be unique")
    source_set = set(source_ids)

    finding_ids = []
    for finding in data.get("findings", []):
        finding_id = finding.get("finding_id")
        if not finding_id:
            fail("finding missing finding_id")
        finding_ids.append(finding_id)
        if finding.get("classification") not in ALLOWED_CLASSIFICATIONS:
            fail(f"{finding_id} has unsupported classification")
        unknown = sorted(set(finding.get("source_refs", [])) - source_set)
        if unknown:
            fail(f"{finding_id} references unknown sources: {unknown}")
        for field in ("guide", "reviewed_statement", "comparator", "recommendation"):
            if not str(finding.get(field, "")).strip():
                fail(f"{finding_id} missing {field}")
        marker = f"<!-- finding:{finding_id} -->"
        if marker not in page:
            fail(f"public page missing marker for {finding_id}")

    if len(finding_ids) != len(set(finding_ids)):
        fail("finding_id values must be unique")

    lower_page = page.lower()
    for phrase in (
        "not a complaint or allegation",
        "does not provide individualized medical advice",
        "no participant identity",
    ):
        if phrase not in lower_page:
            fail(f"public authority/privacy boundary phrase missing: {phrase}")

    print(
        "PUBLIC HEALTH GUIDANCE QUALITY: PASS "
        f"({len(finding_ids)} findings, {len(source_ids)} sources, privacy/authority boundary intact)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
