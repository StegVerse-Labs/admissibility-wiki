#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "static" / "data" / "framework-evaluations" / "relational-mechanics.json"
DOC = ROOT / "docs" / "external-frameworks" / "relational-mechanics-binding-authority-intake.md"


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    if not DATA.exists():
        fail("missing relational-mechanics machine-readable intake")
    if not DOC.exists():
        fail("missing relational-mechanics public intake document")

    record = json.loads(DATA.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    if record.get("framework_id") != "relational-mechanics":
        fail("unexpected framework_id")
    if record.get("stegverse_determination", {}).get("public_review_standing") != "BOUNDED_INTAKE":
        fail("public review standing must remain BOUNDED_INTAKE")

    binding = record.get("binding_model", {})
    expected_terms = {
        "R": "relational_integrity",
        "S": "current_standing",
        "E": "sufficient_evidence",
        "A": "commit_time_authority_and_admissibility",
        "C": "continuation_and_independent_reconstructability",
    }
    if binding.get("terms") != expected_terms:
        fail("binding-model terms changed or are incomplete")
    if binding.get("policy_binding_required") is not True:
        fail("policy binding must be required")

    separations = set(record.get("constitutional_separations", []))
    required_separations = {
        "relational_understanding != execution_authority",
        "relational_correctness != binding_judgment",
        "actor_authorization != authorized_relationship",
        "authorized_relationship != admissible_transition",
        "accountability_record != non_bypassable_prevention",
    }
    missing = sorted(required_separations - separations)
    if missing:
        fail(f"missing constitutional separations: {missing}")

    authority = record.get("authority", {})
    prohibited_true = sorted(key for key, value in authority.items() if value is not False)
    if prohibited_true:
        fail(f"authority fields must remain false: {prohibited_true}")

    tests = set(record.get("test_vectors", []))
    required_tests = {
        "INDIVIDUALLY_CLEAN_RELATIONALLY_UNSAFE",
        "OBSERVER_AMBIGUITY",
        "SHORT_LIVED_ACTOR",
        "AUTHORITY_DRIFT_BEFORE_COMMIT",
        "RELATIONAL_INTEGRITY_FAILURE_ENFORCEMENT",
    }
    if tests != required_tests:
        fail("discriminating test-vector set changed or is incomplete")

    if record.get("answerability_survival", {}).get("authority_inheritance_from_terminated_actor") is not False:
        fail("terminated actors must not confer inherited authority")

    required_doc_markers = (
        "authorized actors",
        "authorized relationship",
        "admissible transition",
        "Relational Binding Theorem",
        "non-bypassable",
        "short-lived actor",
        "Bounded determination",
    )
    missing_doc = [marker for marker in required_doc_markers if marker.lower() not in doc.lower()]
    if missing_doc:
        fail(f"public intake is missing required markers: {missing_doc}")

    print("RELATIONAL MECHANICS BINDING INTAKE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
