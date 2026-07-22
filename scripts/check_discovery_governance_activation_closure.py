#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "reports" / "public-activation-receipt.json"
DISCOVERY = ROOT / "reports" / "discovery-governance-publication-receipt.json"
REQUIRED_ROUTES = {
    "discovery_governance_doctrine",
    "discovery_governance_schema",
    "discovery_governance_status",
    "discovery_governance_example",
    "discovery_governance_publication_receipt_schema",
}
FALSE_FIELDS = (
    "implementation_equivalence_established",
    "interoperability_verified",
    "consent_granted",
    "standing_granted",
    "authority_granted",
    "admissibility_granted",
    "commitment_granted",
    "execution_permission_granted",
    "certification_granted",
    "endorsement_granted",
    "downstream_mutation_authority_granted",
)


def main() -> int:
    failures: list[str] = []
    for path in (PUBLIC, DISCOVERY):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("DISCOVERY GOVERNANCE ACTIVATION CLOSURE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    public = json.loads(PUBLIC.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY.read_text(encoding="utf-8"))
    embedded = public.get("activation_closures", {}).get("discovery_governance")

    if discovery.get("schema") != "discovery_governance_publication_receipt.v1":
        failures.append("standalone discovery receipt schema mismatch")
    if embedded != discovery:
        failures.append("embedded discovery closure does not exactly match standalone receipt")
    if public.get("linked_receipts", {}).get("discovery_governance_publication_receipt") != "reports/discovery-governance-publication-receipt.json":
        failures.append("public receipt linked discovery path mismatch")

    routes = discovery.get("routes", {})
    missing_routes = REQUIRED_ROUTES - set(routes)
    if missing_routes:
        failures.append(f"discovery receipt missing routes: {sorted(missing_routes)}")

    verified = discovery.get("all_required_public_routes_verified") is True
    route_pass = all(
        isinstance(routes.get(name), dict)
        and routes[name].get("reachable") is True
        and isinstance(routes[name].get("http_status"), int)
        and 200 <= routes[name]["http_status"] < 400
        for name in REQUIRED_ROUTES
    )
    if verified != route_pass:
        failures.append("bounded route verification state does not match individual route evidence")

    expected_state = "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE" if route_pass else "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED"
    if discovery.get("state") != expected_state:
        failures.append(f"discovery closure state must be {expected_state}")
    if discovery.get("pages_deployment_observed") is not route_pass:
        failures.append("pages deployment observation must match bounded route evidence")

    for field in FALSE_FIELDS:
        if discovery.get(field) is not False:
            failures.append(f"discovery closure must preserve {field}=false")

    for field in ("repository", "commit", "run_id", "run_attempt"):
        if public.get(field) != discovery.get(field):
            failures.append(f"public and discovery receipt {field} mismatch")

    if public.get("publication_complete") is True and not route_pass:
        failures.append("public publication_complete cannot be true when discovery routes fail")

    if failures:
        print("DISCOVERY GOVERNANCE ACTIVATION CLOSURE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("DISCOVERY GOVERNANCE ACTIVATION CLOSURE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
