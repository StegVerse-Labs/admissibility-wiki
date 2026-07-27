#!/usr/bin/env python3
"""Validate the governed relationship publication-observation schema and fixtures."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static/schemas/governed-relationship-transition-publication-observation.schema.json"
FIXTURE_PATH = ROOT / "static/governance/fixtures/governed-relationship-publication-observation-cases.v0.1.json"
OBSERVER_PATH = ROOT / "scripts/observe_governed_relationship_publication.py"
WRITER_PATH = ROOT / "scripts/write-public-activation-receipt.mjs"

REQUIRED_SCHEMA_KEYS = {
    "schema",
    "repository",
    "observed_at",
    "state",
    "routes",
    "all_required_public_routes_verified",
    "pages_deployment_observed",
    "publication_authority_granted",
    "release_authority_granted",
    "execution_authority_granted",
    "admissibility_granted",
    "downstream_mutation_authority_granted",
    "manual_tasks_required",
    "user_action_required",
    "non_claims",
}
FALSE_AUTHORITY_FIELDS = (
    "publication_authority_granted",
    "release_authority_granted",
    "execution_authority_granted",
    "admissibility_granted",
    "downstream_mutation_authority_granted",
    "user_action_required",
)
REQUIRED_ROUTES = {"doctrine", "schema", "example"}


def fail(message: str) -> int:
    print(f"GOVERNED RELATIONSHIP OBSERVATION SCHEMA: FAIL - {message}")
    return 1


def receipt_is_admissible(receipt: dict[str, object]) -> bool:
    required = REQUIRED_SCHEMA_KEYS
    if not required.issubset(receipt):
        return False
    if receipt.get("schema") != "stegverse.governed_relationship_transition_publication_observation.v1":
        return False
    if receipt.get("repository") != "StegVerse-Labs/admissibility-wiki":
        return False
    if any(receipt.get(field) is not False for field in FALSE_AUTHORITY_FIELDS):
        return False
    if receipt.get("manual_tasks_required") != []:
        return False
    non_claims = receipt.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        return False

    state = receipt.get("state")
    routes = receipt.get("routes")
    if not isinstance(routes, dict):
        return False
    verified = receipt.get("all_required_public_routes_verified")
    deployed = receipt.get("pages_deployment_observed")

    if state == "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE":
        if verified is not True or deployed is not True or set(routes) != REQUIRED_ROUTES:
            return False
        for route in routes.values():
            if not isinstance(route, dict) or route.get("reachable") is not True:
                return False
    elif state == "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED":
        if verified is not False:
            return False
    elif state == "SIMULATED_VALIDATOR_PASS":
        if deployed is not False:
            return False
    else:
        return False
    return True


def main() -> int:
    for path in (SCHEMA_PATH, FIXTURE_PATH, OBSERVER_PATH, WRITER_PATH):
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        return fail("unexpected JSON Schema dialect")
    if schema.get("title") != "Governed Relationship Transition Publication Observation":
        return fail("title mismatch")
    if set(schema.get("required", [])) != REQUIRED_SCHEMA_KEYS:
        return fail("required-field set mismatch")

    properties = schema.get("properties", {})
    for field in FALSE_AUTHORITY_FIELDS:
        if properties.get(field, {}).get("const") is not False:
            return fail(f"{field} must remain const false")
    if properties.get("manual_tasks_required", {}).get("maxItems") != 0:
        return fail("manual_tasks_required must remain empty")

    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if fixture.get("schema") != "stegverse.governed_relationship_transition_publication_observation_cases.v0.1":
        return fail("fixture schema mismatch")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or len(cases) < 5:
        return fail("fixture coverage is incomplete")
    seen: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        expected = case.get("expected")
        receipt = case.get("receipt")
        if not isinstance(case_id, str) or case_id in seen:
            return fail("fixture case identifiers must be unique strings")
        seen.add(case_id)
        if expected not in {"PASS", "FAIL"} or not isinstance(receipt, dict):
            return fail(f"malformed fixture case: {case_id}")
        actual = "PASS" if receipt_is_admissible(receipt) else "FAIL"
        if actual != expected:
            return fail(f"fixture outcome mismatch: {case_id} expected {expected}, got {actual}")

    observer_text = OBSERVER_PATH.read_text(encoding="utf-8")
    writer_text = WRITER_PATH.read_text(encoding="utf-8")
    required_markers = (
        "stegverse.governed_relationship_transition_publication_observation.v1",
        "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE",
        "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
        "publication_authority_granted",
        "admissibility_granted",
    )
    for marker in required_markers:
        if marker not in observer_text:
            return fail(f"observer missing marker: {marker}")
        if marker not in writer_text:
            return fail(f"writer missing marker: {marker}")

    print(
        "GOVERNED RELATIONSHIP OBSERVATION SCHEMA: PASS - schema, observer, writer, "
        "positive and negative fixtures, fail-closed states, and authority boundaries agree"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
