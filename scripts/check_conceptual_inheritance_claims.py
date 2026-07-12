#!/usr/bin/env python3
"""Deterministically validate conceptual-inheritance fixtures and decisions."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "conceptual-inheritance-cases.json"
SCHEMA = ROOT / "static" / "schemas" / "conceptual-inheritance-record.schema.json"
FORMALISM = ROOT / "docs" / "formalisms" / "conceptual-inheritance-provenance.md"

DECISIONS = {"ADMIT", "DENY", "FAIL_CLOSED", "REVIEW_REQUIRED"}
INHERITANCE_STATES = {
    "NO_KNOWN_EXPOSURE",
    "INDEPENDENT_PARALLEL_DEVELOPMENT",
    "GENERAL_DOMAIN_INFLUENCE",
    "ACKNOWLEDGED_CONCEPTUAL_INFLUENCE",
    "BOUNDED_INTEROPERABILITY",
    "STRUCTURAL_INHERITANCE",
    "DIRECT_ARTIFACT_TRANSFER",
    "TRANSFORMED_DERIVATION",
    "CO_DEVELOPED",
    "PROVENANCE_UNRESOLVED",
    "PROVENANCE_CONFLICTED",
}

REQUIRED_FIELDS = {
    "transition_id",
    "source_artifact_refs",
    "source_concept_refs",
    "exposure_event_refs",
    "received_artifact_refs",
    "transformation_record_refs",
    "inheritance_state",
    "attribution_required",
    "attribution_satisfied",
    "independence_claim_requested",
    "claim_admissibility",
    "evaluated_at",
    "policy_ref",
}


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def decide(record: Dict[str, Any]) -> str:
    """Evaluate only provenance standing, not ownership, intent, or legality."""
    independence_requested = bool(record["independence_claim_requested"])
    unresolved = bool(record.get("provenance_unresolved", False)) or record["inheritance_state"] in {
        "PROVENANCE_UNRESOLVED",
        "PROVENANCE_CONFLICTED",
    }
    direct_receipt = bool(record.get("direct_receipt_established", False))
    structural_inheritance = bool(record.get("structural_inheritance_established", False))
    contradictions = bool(record.get("contradiction_refs", []))
    attribution_required = bool(record["attribution_required"])
    attribution_satisfied = bool(record["attribution_satisfied"])

    if not independence_requested:
        if unresolved:
            return "REVIEW_REQUIRED"
        if attribution_required and not attribution_satisfied:
            return "REVIEW_REQUIRED"
        return "ADMIT"

    if unresolved:
        return "FAIL_CLOSED"

    if direct_receipt or structural_inheritance or contradictions:
        return "DENY"

    if record["inheritance_state"] in {
        "ACKNOWLEDGED_CONCEPTUAL_INFLUENCE",
        "BOUNDED_INTEROPERABILITY",
        "GENERAL_DOMAIN_INFLUENCE",
        "CO_DEVELOPED",
    }:
        return "REVIEW_REQUIRED"

    if attribution_required and not attribution_satisfied:
        return "REVIEW_REQUIRED"

    return "ADMIT"


def validate_record(record: Dict[str, Any], case_id: str) -> List[str]:
    errors: List[str] = []
    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        errors.append(f"{case_id}: missing required fields: {', '.join(missing)}")
        return errors

    if record["inheritance_state"] not in INHERITANCE_STATES:
        errors.append(f"{case_id}: invalid inheritance_state")
    if record["claim_admissibility"] not in DECISIONS:
        errors.append(f"{case_id}: invalid claim_admissibility")

    for field in (
        "source_artifact_refs",
        "source_concept_refs",
        "exposure_event_refs",
        "received_artifact_refs",
        "transformation_record_refs",
        "contradiction_refs",
    ):
        value = record.get(field, [])
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            errors.append(f"{case_id}: {field} must be an array of non-empty strings")

    for field in (
        "attribution_required",
        "attribution_satisfied",
        "independence_claim_requested",
    ):
        if not isinstance(record[field], bool):
            errors.append(f"{case_id}: {field} must be boolean")

    if not isinstance(record["transition_id"], str) or not record["transition_id"]:
        errors.append(f"{case_id}: transition_id must be non-empty")
    if not isinstance(record["policy_ref"], str) or not record["policy_ref"]:
        errors.append(f"{case_id}: policy_ref must be non-empty")

    return errors


def main() -> int:
    missing_files = [str(path.relative_to(ROOT)) for path in (FIXTURES, SCHEMA, FORMALISM) if not path.exists()]
    if missing_files:
        print("conceptual inheritance validation failed: missing " + ", ".join(missing_files), file=sys.stderr)
        return 1

    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        print("conceptual inheritance validation failed: fixtures require non-empty cases", file=sys.stderr)
        return 1

    errors: List[str] = []
    receipts: List[Dict[str, str]] = []
    seen_ids = set()

    for case in cases:
        case_id = case.get("case_id")
        record = case.get("record")
        expected = case.get("expected_decision")

        if not isinstance(case_id, str) or not case_id:
            errors.append("fixture case missing non-empty case_id")
            continue
        if case_id in seen_ids:
            errors.append(f"duplicate case_id: {case_id}")
            continue
        seen_ids.add(case_id)

        if not isinstance(record, dict):
            errors.append(f"{case_id}: record must be an object")
            continue
        if expected not in DECISIONS:
            errors.append(f"{case_id}: invalid expected_decision")
            continue

        errors.extend(validate_record(record, case_id))
        actual = decide(record)
        if actual != expected:
            errors.append(f"{case_id}: expected {expected}, got {actual}")
        if record.get("claim_admissibility") != expected:
            errors.append(
                f"{case_id}: fixture claim_admissibility {record.get('claim_admissibility')} does not match expected {expected}"
            )

        receipts.append(
            {
                "case_id": case_id,
                "transition_id": str(record.get("transition_id", "")),
                "decision": actual,
                "record_sha256": canonical_hash(record),
            }
        )

    required_outcomes = {"ADMIT", "DENY", "FAIL_CLOSED", "REVIEW_REQUIRED"}
    observed_outcomes = {receipt["decision"] for receipt in receipts}
    missing_outcomes = sorted(required_outcomes - observed_outcomes)
    if missing_outcomes:
        errors.append("fixture coverage missing decisions: " + ", ".join(missing_outcomes))

    if errors:
        print("conceptual inheritance validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "validator": "check_conceptual_inheritance_claims.py",
                "result": "PASS",
                "case_count": len(receipts),
                "decision_coverage": sorted(observed_outcomes),
                "fixture_sha256": canonical_hash(payload),
                "receipts": receipts,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
