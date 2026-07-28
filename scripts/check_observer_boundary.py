#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "static/data/observer-boundary/observer-boundary-profile.v1.json"
FIXTURES = ROOT / "static/data/observer-boundary/examples/observer-boundary-fixtures.v1.json"

EXPECTED_SEQUENCE = ["PROPOSED", "AUTHORIZED", "COMMITTED", "RECONSTRUCTED"]
PROHIBITED_TRUE = {
    "certification",
    "government_recognition",
    "reviewer_standing",
    "custody",
    "endorsement",
    "execution_authority",
    "independent_verification",
    "production_runtime_control",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def classify(evidence: dict) -> str:
    if not evidence.get("proposal"):
        return "INDETERMINATE"
    if not evidence.get("authorization"):
        return "INDETERMINATE"
    if not evidence.get("commitment"):
        return "AUTHORIZED"
    if not evidence.get("reconstruction_report"):
        return "COMMITTED"
    if not evidence.get("evidence_omissions_disclosed"):
        return "INDETERMINATE"
    if evidence.get("retrospective_inference_only"):
        return "INDETERMINATE"
    return "RECONSTRUCTED"


def main() -> int:
    failures: list[str] = []
    try:
        profile = load_json(PROFILE)
        fixture_doc = load_json(FIXTURES)
    except ValueError as exc:
        print(f"OBSERVER BOUNDARY: FAIL\n- {exc}")
        return 1

    if profile.get("state_sequence") != EXPECTED_SEQUENCE:
        failures.append("state sequence must be PROPOSED -> AUTHORIZED -> COMMITTED -> RECONSTRUCTED")

    authority_effect = profile.get("authority_effect", {})
    for field in PROHIBITED_TRUE:
        if authority_effect.get(field) is not False:
            failures.append(f"profile authority_effect.{field} must be false")

    fixtures = fixture_doc.get("fixtures")
    if not isinstance(fixtures, list) or len(fixtures) < 5:
        failures.append("fixture set must contain at least five deterministic cases")
        fixtures = []

    seen_ids: set[str] = set()
    required_cases = {
        "STAGE_ROLE_COLLAPSE",
        "OBSERVER_BECAME_PARTICIPANT",
        "EVIDENCE_OMISSION",
        "RETROSPECTIVE_AUTHORIZATION_INFERENCE",
        "BOUNDED_RECONSTRUCTION_COMPLETE",
    }
    observed_cases: set[str] = set()

    for fixture in fixtures:
        fixture_id = fixture.get("id")
        if not fixture_id or fixture_id in seen_ids:
            failures.append(f"missing or duplicate fixture id: {fixture_id!r}")
            continue
        seen_ids.add(fixture_id)

        evidence = fixture.get("evidence", {})
        actual = classify(evidence)
        expected = fixture.get("expected_class")
        if actual != expected:
            failures.append(f"{fixture_id}: expected {expected}, validator derived {actual}")

        if fixture.get("independent_observer_standing") is not False:
            failures.append(f"{fixture_id}: fixtures must not create independent observer standing")

        findings = fixture.get("required_findings", [])
        if not findings:
            failures.append(f"{fixture_id}: required_findings must not be empty")
        observed_cases.update(findings)

        if "STAGE_ROLE_COLLAPSE" in findings and evidence.get("role_separation_recorded") is not False:
            failures.append(f"{fixture_id}: collapse case must record role separation as false")
        if "OBSERVER_BECAME_PARTICIPANT" in findings and evidence.get("intervention_recorded") is not True:
            failures.append(f"{fixture_id}: intervention case must preserve the intervention")
        if "EVIDENCE_OMISSION" in findings and evidence.get("evidence_omissions_disclosed") is not False:
            failures.append(f"{fixture_id}: omission case must leave omissions undisclosed")
        if "RETROSPECTIVE_AUTHORIZATION_INFERENCE" in findings and evidence.get("retrospective_inference_only") is not True:
            failures.append(f"{fixture_id}: retrospective case must be inference-only")

    missing_cases = required_cases - observed_cases
    if missing_cases:
        failures.append("missing required fixture coverage: " + ", ".join(sorted(missing_cases)))

    fixture_authority = fixture_doc.get("authority_effect", {})
    for field in ("certification", "reviewer_standing", "execution_authority", "custody", "endorsement"):
        if fixture_authority.get(field) is not False:
            failures.append(f"fixture authority_effect.{field} must be false")

    if failures:
        print("OBSERVER BOUNDARY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OBSERVER BOUNDARY: PASS")
    print(f"- profile: {PROFILE.relative_to(ROOT)}")
    print(f"- fixtures: {len(fixtures)}")
    print("- independent observer standing created: false")
    print("- execution authority created: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
