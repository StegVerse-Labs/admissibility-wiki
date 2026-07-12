#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "static" / "status" / "conceptual-inheritance-provenance-status.json"
DOCTRINE_PATH = ROOT / "docs" / "formalisms" / "conceptual-inheritance-provenance.md"
INDEX_PATH = ROOT / "docs" / "formalisms" / "index.md"
SIDEBAR_PATH = ROOT / "sidebars.js"
SCHEMA_PATH = ROOT / "static" / "schemas" / "conceptual-inheritance-record.schema.json"
FIXTURES_PATH = ROOT / "tests" / "fixtures" / "conceptual-inheritance-cases.json"
VALIDATOR_PATH = ROOT / "scripts" / "check_conceptual_inheritance_claims.py"

EXPECTED_OUTCOMES = {"ADMIT", "DENY", "FAIL_CLOSED", "REVIEW_REQUIRED"}
EXPECTED_STATUS = {
    "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_VERIFICATION",
    "CANONICAL_VALIDATION_PASSED_PENDING_PUBLIC_DEPLOYMENT",
    "PUBLICLY_DEPLOYED_PENDING_DOWNSTREAM_PROPAGATION",
    "ACTIVATED",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []

    required_files = (
        STATUS_PATH,
        DOCTRINE_PATH,
        INDEX_PATH,
        SIDEBAR_PATH,
        SCHEMA_PATH,
        FIXTURES_PATH,
        VALIDATOR_PATH,
    )
    for path in required_files:
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}", failures)

    if failures:
        print("CONCEPTUAL INHERITANCE STATUS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("CONCEPTUAL INHERITANCE STATUS: FAIL")
        print(f"- invalid status artifact: {exc}")
        return 1

    required_fields = {
        "schema_version",
        "goal_id",
        "repository",
        "status",
        "doctrine",
        "schema",
        "fixtures",
        "validator",
        "canonical_integration",
        "navigation",
        "formalism_index",
        "decision_outcomes",
        "governance_boundaries",
        "remaining_checks",
        "manual_task_required",
        "recorded_at",
    }
    missing_fields = sorted(required_fields - set(status))
    if missing_fields:
        fail(f"missing status fields: {', '.join(missing_fields)}", failures)

    if status.get("goal_id") != "conceptual-inheritance-provenance-standing":
        fail("unexpected goal_id", failures)
    if status.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("unexpected repository", failures)
    if status.get("status") not in EXPECTED_STATUS:
        fail("unsupported status value", failures)
    if set(status.get("decision_outcomes", [])) != EXPECTED_OUTCOMES:
        fail("decision outcomes must cover ADMIT, DENY, FAIL_CLOSED, and REVIEW_REQUIRED", failures)
    if status.get("manual_task_required") is not False:
        fail("manual_task_required must remain false", failures)

    expected_paths = {
        "doctrine": "docs/formalisms/conceptual-inheritance-provenance.md",
        "schema": "static/schemas/conceptual-inheritance-record.schema.json",
        "fixtures": "tests/fixtures/conceptual-inheritance-cases.json",
        "validator": "scripts/check_conceptual_inheritance_claims.py",
        "canonical_integration": "scripts/check_admissibility_automation_handoff.py",
        "navigation": "sidebars.js",
        "formalism_index": "docs/formalisms/index.md",
    }
    for field, expected in expected_paths.items():
        if status.get(field) != expected:
            fail(f"{field} must reference {expected}", failures)

    doctrine = DOCTRINE_PATH.read_text(encoding="utf-8")
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    sidebar = SIDEBAR_PATH.read_text(encoding="utf-8")

    doctrine_markers = (
        "architectural integrity",
        "provenance continuity",
        "origin-claim standing",
        "PROVENANCE_UNRESOLVED",
        "Accusation overclaim",
    )
    for marker in doctrine_markers:
        if marker not in doctrine:
            fail(f"doctrine missing marker: {marker}", failures)

    if "conceptual-inheritance-provenance" not in sidebar:
        fail("sidebar does not publish conceptual inheritance formalism", failures)
    if "Conceptual Inheritance and Provenance Standing" not in index_text:
        fail("formalism index does not include conceptual inheritance entry", failures)

    if failures:
        print("CONCEPTUAL INHERITANCE STATUS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONCEPTUAL INHERITANCE STATUS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
