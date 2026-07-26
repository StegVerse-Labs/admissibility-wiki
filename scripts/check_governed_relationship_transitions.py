#!/usr/bin/env python3
"""Validate governed relationship transition doctrine, navigation, schema, and example."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/governance/governed-relationship-transitions.md"
SIDEBAR = ROOT / "sidebars.js"
README = ROOT / "README.md"
SCHEMA = ROOT / "static/governance/governed-relationship-transition.schema.v0.1.json"
EXAMPLE = ROOT / "static/governance/governed-relationship-transition.example.v0.1.json"

REQUIRED_DOC_TERMS = (
    "Persistence is not continuity. Continuity is not legitimacy.",
    "commit-time boundary",
    "purpose-inverting",
    "A governed architecture must be able to refuse its own continuation.",
)

ENUMS = {
    "reality_correspondence": {"SUPPORTED", "DIVERGED", "UNRESOLVED"},
    "recoverability": {"RECOVERABLE", "DEGRADED", "UNRECOVERABLE"},
    "commit_time_validity": {"VALID", "INVALID", "UNRESOLVED"},
    "admissibility_result": {"ALLOW", "DENY", "FAIL_CLOSED"},
}

REQUIRED_FIELDS = {
    "schema_version",
    "relationship_id",
    "transition_id",
    "prior_state_ref",
    "proposed_state_ref",
    "purpose_ref",
    "authority_refs",
    "delegation_refs",
    "evidence_refs",
    "invariant_results",
    "reality_correspondence",
    "recoverability",
    "commit_time_validity",
    "admissibility_result",
    "decision_receipt_ref",
}


def fail(message: str) -> int:
    print(f"GOVERNED RELATIONSHIP TRANSITIONS: FAIL - {message}")
    return 1


def main() -> int:
    for path in (DOC, SIDEBAR, README, SCHEMA, EXAMPLE):
        if not path.exists():
            return fail(f"missing file: {path.relative_to(ROOT)}")

    doc_text = DOC.read_text(encoding="utf-8")
    for term in REQUIRED_DOC_TERMS:
        if term not in doc_text:
            return fail(f"missing doctrine term: {term}")

    if "governance/governed-relationship-transitions" not in SIDEBAR.read_text(encoding="utf-8"):
        return fail("sidebar reference missing")

    readme_text = README.read_text(encoding="utf-8")
    if "docs/governance/governed-relationship-transitions.md" not in readme_text:
        return fail("README reference missing")

    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    schema_required = set(schema.get("required", []))
    if schema_required != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - schema_required)
        extra = sorted(schema_required - REQUIRED_FIELDS)
        return fail(f"schema required-field mismatch; missing={missing}, extra={extra}")

    if set(example) != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - set(example))
        extra = sorted(set(example) - REQUIRED_FIELDS)
        return fail(f"example field mismatch; missing={missing}, extra={extra}")

    if example.get("schema_version") != "0.1.0":
        return fail("example schema_version must be 0.1.0")

    for field, allowed in ENUMS.items():
        if example.get(field) not in allowed:
            return fail(f"invalid {field}: {example.get(field)!r}")

    if example["commit_time_validity"] == "UNRESOLVED" and example["admissibility_result"] != "FAIL_CLOSED":
        return fail("unresolved commit-time validity must fail closed")

    for result in example["invariant_results"]:
        if not isinstance(result, dict):
            return fail("invariant result must be an object")
        if result.get("result") not in {"PASS", "FAIL", "UNRESOLVED"}:
            return fail(f"invalid invariant result: {result.get('result')!r}")

    print("GOVERNED RELATIONSHIP TRANSITIONS: PASS - doctrine, navigation, schema, and example validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
