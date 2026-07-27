#!/usr/bin/env python3
"""Validate the governed relationship publication-observation schema and fixtures."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static/schemas/governed-relationship-transition-publication-observation.schema.json"
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


def fail(message: str) -> int:
    print(f"GOVERNED RELATIONSHIP OBSERVATION SCHEMA: FAIL - {message}")
    return 1


def main() -> int:
    for path in (SCHEMA_PATH, OBSERVER_PATH, WRITER_PATH):
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
    for field in (
        "publication_authority_granted",
        "release_authority_granted",
        "execution_authority_granted",
        "admissibility_granted",
        "downstream_mutation_authority_granted",
        "user_action_required",
    ):
        if properties.get(field, {}).get("const") is not False:
            return fail(f"{field} must remain const false")

    if properties.get("manual_tasks_required", {}).get("maxItems") != 0:
        return fail("manual_tasks_required must remain empty")

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
        "GOVERNED RELATIONSHIP OBSERVATION SCHEMA: PASS - schema, observer, "
        "writer, fail-closed states, and authority boundaries agree"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
