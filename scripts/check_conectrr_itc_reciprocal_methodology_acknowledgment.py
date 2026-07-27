#!/usr/bin/env python3
"""Validate the bounded Conectrr reciprocal-methodology acknowledgment record."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "static/data/framework-evaluations/examples/conectrr-itc.reciprocal-methodology-acknowledgment.v1.json"
DOC = ROOT / "docs/external-frameworks/conectrr-itc-reciprocal-methodology-acknowledgment-2026-07-27.md"

REQUIRED_ACKNOWLEDGMENTS = {
    "responsibility_separation",
    "discovery_remains_non_authorizing",
    "downstream_reconstruction_responsibility",
    "downstream_governance_responsibility",
    "downstream_authorization_responsibility",
    "downstream_execution_responsibility",
    "divergent_findings_remain_visible",
    "methodology_is_material_outcome",
    "v1_1_evidence_constrained_after_v1_0_closure",
    "reciprocal_non_subsuming_review_model",
}

REQUIRED_EXTERNAL_ARTIFACTS = {
    "ITC Specification v1.0 Draft",
    "canonical ITC generated from an actual Conectrr recommendation",
    "Conectrr internal validation report",
}

REQUIRED_NON_EQUIVALENCE_RULES = {
    "methodology acknowledgment != implementation proof",
    "methodology acknowledgment != schema conformance",
    "methodology acknowledgment != semantic correctness",
    "methodology acknowledgment != independent reconstruction",
    "methodology acknowledgment != replay PASS",
    "methodology acknowledgment != execution authority",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(RECORD.is_file(), f"missing acknowledgment record: {RECORD}")
    require(DOC.is_file(), f"missing acknowledgment documentation: {DOC}")

    data = json.loads(RECORD.read_text(encoding="utf-8"))

    require(data.get("schema_version") == "1.0.0", "unexpected schema_version")
    require(data.get("record_id") == "conectrr-itc-reciprocal-methodology-acknowledgment-2026-07-27", "unexpected record_id")
    require(data.get("framework_id") == "conectrr-itc", "unexpected framework_id")
    require(data.get("record_type") == "founder_correspondence_acknowledgment", "unexpected record_type")
    require(data.get("source_artifact_posture") == "captured_not_canonically_custodied", "source posture must remain non-custodial")

    acknowledgments = data.get("acknowledgments", {})
    require(set(acknowledgments) == REQUIRED_ACKNOWLEDGMENTS, "acknowledgment inventory drifted")
    require(all(acknowledgments.values()), "all preserved methodology acknowledgments must remain true")

    disposition = data.get("disposition", {})
    expected_disposition = {
        "reciprocal_review_model": "MUTUALLY_ACKNOWLEDGED",
        "technical_validation_result": "UNCHANGED",
        "source_package": "OFFERED_NOT_RECEIVED",
        "bounded_v1_0_evaluation": "OPEN",
        "v1_1_development_posture": "DEFERRED_PENDING_V1_0_EVIDENCE",
        "live_interoperability_test": "NOT_RUN",
        "independent_reconstruction": "NOT_RUN_EXTERNALLY",
    }
    require(disposition == expected_disposition, "technical disposition or evidence posture drifted")

    authority = data.get("authority", {})
    require(authority, "authority boundary missing")
    require(all(value is False for value in authority.values()), "acknowledgment must grant no authority")

    require(set(data.get("required_external_artifacts", [])) == REQUIRED_EXTERNAL_ARTIFACTS, "external artifact gate drifted")
    require(set(data.get("non_equivalence_rules", [])) == REQUIRED_NON_EQUIVALENCE_RULES, "non-equivalence boundary drifted")

    doc = DOC.read_text(encoding="utf-8")
    for marker in (
        "RECIPROCAL REVIEW MODEL: MUTUALLY ACKNOWLEDGED",
        "TECHNICAL VALIDATION RESULT: UNCHANGED",
        "SOURCE PACKAGE: OFFERED_NOT_RECEIVED",
        "AUTHORITY GRANTED: NONE",
        "methodology acknowledgment != execution authority",
    ):
        require(marker in doc, f"documentation missing boundary marker: {marker}")

    print("PASS: Conectrr reciprocal methodology acknowledgment remains bounded and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
