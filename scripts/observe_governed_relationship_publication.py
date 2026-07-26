#!/usr/bin/env python3
"""Observe governed relationship-transition public routes and write a bounded receipt."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROUTES = {
    "doctrine": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-relationship-transitions",
    "schema": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-relationship-transition.schema.v0.1.json",
    "example": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-relationship-transition.example.v0.1.json",
}
RECEIPT = Path("reports/governed-relationship-transition-publication-observation.json")


def observe(url: str) -> dict[str, object]:
    request = Request(url, method="HEAD", headers={"User-Agent": "stegverse-admissibility-verifier/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            status = int(getattr(response, "status", None) or response.getcode())
        return {"url": url, "reachable": 200 <= status < 400, "http_status": status}
    except HTTPError as exc:
        return {"url": url, "reachable": False, "http_status": exc.code}
    except (URLError, TimeoutError) as exc:
        return {"url": url, "reachable": False, "http_status": None, "error": str(exc)}


def main() -> int:
    observations = {name: observe(url) for name, url in ROUTES.items()}
    passed = all(bool(item["reachable"]) for item in observations.values())
    receipt = {
        "schema": "stegverse.governed_relationship_transition_publication_observation.v1",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "state": "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE" if passed else "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
        "routes": observations,
        "all_required_public_routes_verified": passed,
        "pages_deployment_observed": passed,
        "publication_authority_granted": False,
        "release_authority_granted": False,
        "execution_authority_granted": False,
        "admissibility_granted": False,
        "downstream_mutation_authority_granted": False,
        "manual_tasks_required": [],
        "user_action_required": False,
        "non_claims": [
            "Route reachability is bounded publication evidence only.",
            "Publication does not establish execution authority or admissibility.",
            "A passing observation does not independently authorize release or downstream mutation."
        ],
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RECEIPT}")
    print("GOVERNED RELATIONSHIP PUBLICATION: PASS" if passed else "GOVERNED RELATIONSHIP PUBLICATION: FAIL_CLOSED")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
