#!/usr/bin/env python3
"""Validate the public micronutrients successor projection."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "health-guidance" / "external-health-guidance-micronutrients-successor.v1.json"
PAGE = ROOT / "docs" / "health-guidance" / "external-health-guidance-micronutrients-successor.md"
SIDEBARS = ROOT / "sidebars.js"

REQUIRED = {
    "MICRO-NA-001",
    "MICRO-CA-001",
    "MICRO-K-SYMBOL-001",
    "MICRO-WATER-STORAGE-001",
    "MICRO-VITA-UNIT-001",
    "MICRO-FOLATE-UNIT-001",
    "MICRO-NIACIN-UNIT-001",
    "MICRO-VITD-UNIT-001",
}
PROHIBITED = {
    "participant_name","patient_name","member_id","account_id",
    "prescription_number","rx_number","medical_record_number","date_of_birth",
}

def walk_keys(v):
    if isinstance(v, dict):
        for k, child in v.items():
            yield k
            yield from walk_keys(child)
    elif isinstance(v, list):
        for child in v:
            yield from walk_keys(child)

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    sidebars = SIDEBARS.read_text(encoding="utf-8")

    assert data["schema_version"] == "public.health-guidance-micronutrients-successor.v1"
    assert data["issue"] == 113
    assert data["predecessor_issue"] == 109
    assert data["predecessor_state"] == "COMPLETED_IMMUTABLE"
    assert data["source_program"]["participant_identifying_information_included"] is False
    assert not (PROHIBITED & set(walk_keys(data)))
    assert all(v is False for v in data["authority_boundary"].values())
    assert all(v is False for v in data["h2h_boundary"].values())

    sources = {x["source_id"] for x in data["sources"]}
    ids = [x["finding_id"] for x in data["findings"]]
    assert set(ids) == REQUIRED and len(ids) == len(REQUIRED)
    assert "MICRO-B6-001" not in ids and "MICRO-K-001" not in ids

    for finding in data["findings"]:
        assert finding["source_refs"]
        assert set(finding["source_refs"]) <= sources
        assert finding["classification"]
        assert finding["reviewed_statement"]
        assert finding["comparator"]
        assert finding["recommendation"]
        assert f"<!-- finding:{finding['finding_id']} -->" in page

    assert "health-guidance/external-health-guidance-micronutrients-successor" in sidebars
    low = page.lower()
    for phrase in (
        "not a complaint or allegation",
        "does not provide individualized medical advice",
        "predecessor docket",
        "does not approve the h2h participant curriculum",
    ):
        assert phrase in low

    print(
        "PUBLIC MICRONUTRIENTS SUCCESSOR: PASS "
        f"({len(ids)} findings; predecessor #109 preserved; issue #113; privacy/authority/H2H boundaries intact)"
    )

if __name__ == "__main__":
    main()
