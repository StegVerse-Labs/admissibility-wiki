#!/usr/bin/env python3
"""Validate the governed relationship-transition publication candidate without claiming deployment."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "static/status/governed-relationship-transition-publication-candidate.json"
EXPECTED_ROUTES = {
    "doctrine_route": "/admissibility-wiki/governance/governed-relationship-transitions",
    "schema_route": "/admissibility-wiki/governance/governed-relationship-transition.schema.v0.1.json",
    "example_route": "/admissibility-wiki/governance/governed-relationship-transition.example.v0.1.json",
}
FALSE_CLAIM_FIELDS = (
    "public_reachability_observed",
    "pages_deployment_observed",
    "publication_authority_granted",
    "release_authority_granted",
    "execution_authority_granted",
    "admissibility_granted",
    "downstream_mutation_authority_granted",
    "user_action_required",
)


def fail(message: str) -> int:
    print(f"GOVERNED RELATIONSHIP PUBLICATION CANDIDATE: FAIL - {message}")
    return 1


def main() -> int:
    if not CANDIDATE.exists():
        return fail(f"missing file: {CANDIDATE.relative_to(ROOT)}")

    try:
        payload = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    if payload.get("schema") != "stegverse.governed_relationship_transition_publication_candidate.v1":
        return fail("unexpected schema")
    if payload.get("repository") != "StegVerse-Labs/admissibility-wiki":
        return fail("unexpected repository")
    if payload.get("verification_state") != "CANDIDATE_AWAITING_POST_DEPLOY_OBSERVATION":
        return fail("candidate must remain awaiting post-deploy observation")
    if payload.get("canonical_validation_bound") is not True:
        return fail("canonical validation binding must be declared")

    for field, expected_path in EXPECTED_ROUTES.items():
        value = payload.get(field)
        if not isinstance(value, str):
            return fail(f"missing route: {field}")
        parsed = urlparse(value)
        if parsed.scheme != "https" or parsed.netloc != "stegverse-labs.github.io":
            return fail(f"route must use canonical GitHub Pages host: {field}")
        if parsed.path != expected_path:
            return fail(f"unexpected route path for {field}: {parsed.path}")

    for field in FALSE_CLAIM_FIELDS:
        if payload.get(field) is not False:
            return fail(f"{field} must remain false before repository-owned observation")

    if payload.get("manual_tasks_required") != []:
        return fail("manual_tasks_required must remain empty")

    non_claims = payload.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        return fail("non_claims must preserve bounded publication posture")

    print(
        "GOVERNED RELATIONSHIP PUBLICATION CANDIDATE: PASS - "
        "routes declared, canonical binding recorded, deployment claims remain fail-closed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
