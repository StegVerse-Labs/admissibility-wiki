#!/usr/bin/env python3
"""Validate external Governance-Chain Certification intake records.

Intake readiness is not certification. This validator fails closed when the
selected profile lacks required observable/executable evidence routes.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARQUIVONULO = ROOT / "data/certification/intake/arquivonulo-intake.v0.1.json"

INT_REQUIRED = {
    "positive_fixture_route",
    "negative_control_route",
    "effect_observation_point",
    "request_receipt_route",
    "return_receipt_route",
    "replay_material",
    "reconstruction_material",
    "evidence_destination",
}

VALID_STATES = {
    "READY_FOR_CERTIFICATION_TEST",
    "READY_WITH_DECLARED_LIMITS",
    "EVIDENCE_REQUESTED",
    "SOURCE_ONLY_NOT_TESTABLE",
    "INDETERMINATE",
    "REJECTED_SCOPE",
}


def missing_int_requirements(record: dict) -> list[str]:
    missing: list[str] = []
    subject = record.get("subject", {})
    if not subject.get("subject_id"):
        missing.append("subject_id")
    if not subject.get("version"):
        missing.append("subject_version")
    if not subject.get("immutable_locator"):
        missing.append("immutable_locator")
    interface = record.get("interface", {})
    if interface.get("observable_or_executable") is not True:
        missing.append("observable_or_executable_interface")
    routes = record.get("evidence_routes", {})
    for key in sorted(INT_REQUIRED):
        if not routes.get(key):
            missing.append(key)
    return missing


def validate(record: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if record.get("schema_version") != "0.1.0":
        errors.append("unsupported schema_version")
    if record.get("surface") not in {"PRE", "GOV", "POST", "INT"}:
        errors.append("invalid surface")
    if record.get("intake_state") not in VALID_STATES:
        errors.append("invalid intake_state")
    if record.get("certificate_issued") is not False:
        errors.append("intake cannot issue certificate")
    if record.get("authority_effect") != "NONE":
        errors.append("intake authority_effect must be NONE")
    if not record.get("claimed_properties"):
        errors.append("claimed_properties required")

    missing = missing_int_requirements(record) if record.get("surface") == "INT" else []
    state = record.get("intake_state")

    if state == "READY_FOR_CERTIFICATION_TEST" and missing:
        errors.append("ready state with missing mandatory requirements")
    if state == "EVIDENCE_REQUESTED" and not missing:
        errors.append("evidence requested but no mandatory requirement is missing")
    if state == "SOURCE_ONLY_NOT_TESTABLE" and record.get("interface", {}).get("observable_or_executable") is True:
        errors.append("source-only state conflicts with executable interface")

    declared_missing = set(record.get("missing_requirements", []))
    if state == "EVIDENCE_REQUESTED" and not declared_missing:
        errors.append("evidence-requested state must enumerate missing requirements")

    request = record.get("evidence_request")
    if state == "EVIDENCE_REQUESTED":
        if not isinstance(request, dict):
            errors.append("evidence request packet missing")
        else:
            if not request.get("minimum_requested_artifacts"):
                errors.append("minimum_requested_artifacts missing")
            if request.get("commercial_requirement") != "NONE":
                errors.append("commercial requirement cannot be intake prerequisite")
            if request.get("submission_does_not_guarantee_certification") is not True:
                errors.append("non-guarantee must be explicit")

    return not errors, errors


def main() -> int:
    record = json.loads(ARQUIVONULO.read_text(encoding="utf-8"))
    ok, errors = validate(record)
    if not ok:
        raise AssertionError("Arquivonulo intake invalid: " + "; ".join(errors))

    missing = missing_int_requirements(record)
    assert record["intake_state"] == "EVIDENCE_REQUESTED"
    assert missing, "Arquivonulo intake must remain fail-closed while live INT evidence is absent"
    assert record["certificate_issued"] is False
    assert record["authority_effect"] == "NONE"

    # Negative control: READY must fail when the same missing evidence remains.
    promoted = json.loads(json.dumps(record))
    promoted["intake_state"] = "READY_FOR_CERTIFICATION_TEST"
    promoted_ok, _ = validate(promoted)
    if promoted_ok:
        raise AssertionError("false-positive readiness accepted")

    # Negative control: commercial prerequisite cannot create readiness.
    commercial = json.loads(json.dumps(record))
    commercial["evidence_request"]["commercial_requirement"] = "PAID_REVIEW"
    commercial_ok, _ = validate(commercial)
    if commercial_ok:
        raise AssertionError("commercial prerequisite incorrectly accepted")

    print("EXTERNAL_CERTIFICATION_INTAKE: PASS")
    print("candidate=arquivonulo-public-protocol-family")
    print("state=EVIDENCE_REQUESTED")
    print(f"mandatory_missing={len(missing)}")
    print("false_positive_ready=REJECTED")
    print("commercial_prerequisite=REJECTED")
    print("certificate_issued=false")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
