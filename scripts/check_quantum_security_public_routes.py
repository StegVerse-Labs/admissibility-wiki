#!/usr/bin/env python3
"""Observe the merged StegVerse quantum-security publication routes.

This script records bounded publication evidence only. It does not establish
certification, production cryptographic deployment, execution authority, or
permission to mutate downstream repositories.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://stegverse-labs.github.io/admissibility-wiki"
ROUTES = {
    "governance_page": f"{BASE_URL}/governance/quantum-resilient-execution-security",
    "research_paper": f"{BASE_URL}/research/stegverse-complete-security-paper",
    "carousel_source": f"{BASE_URL}/social/stegverse-quantum-security-carousel",
}
OUTPUT = Path("reports/quantum-security-public-route-observation.json")
ATTEMPTS = 6
TIMEOUT_SECONDS = 20


def observe(name: str, url: str) -> dict[str, object]:
    last_error: str | None = None
    for attempt in range(1, ATTEMPTS + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "StegVerse-Quantum-Route-Observer/1.0"},
            )
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                body = response.read()
                status = int(response.status)
                if status != 200:
                    raise RuntimeError(f"HTTP {status}")
                if not body.strip():
                    raise RuntimeError("empty response body")
                return {
                    "result": "PASS",
                    "url": url,
                    "http_status": status,
                    "response_bytes": len(body),
                    "attempt": attempt,
                    "verifier": "scripts/check_quantum_security_public_routes.py",
                }
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            last_error = str(exc)
            if attempt < ATTEMPTS:
                time.sleep(attempt * 2)

    return {
        "result": "SOURCE_BLOCKED_FAIL_CLOSED",
        "url": url,
        "attempts": ATTEMPTS,
        "error": last_error or "unknown observation failure",
        "verifier": "scripts/check_quantum_security_public_routes.py",
    }


def main() -> int:
    observations = {name: observe(name, url) for name, url in ROUTES.items()}
    all_verified = all(item["result"] == "PASS" for item in observations.values())

    receipt = {
        "schema": "quantum_security_public_route_observation.v1",
        "goal_id": "stegverse-quantum-resilient-complete-security",
        "state": (
            "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE"
            if all_verified
            else "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED"
        ),
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "routes": observations,
        "all_required_public_routes_verified": all_verified,
        "pages_deployment_observed": all_verified,
        "manual_task_requirement": "NONE",
        "user_manual_action_required": False,
        "certification_granted": False,
        "universal_quantum_proof_claim": False,
        "production_cryptographic_deployment_established": False,
        "execution_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "continuation_source": "docs/STEGVERSE_QUANTUM_SECURITY_MIRROR_HANDOFF.md",
        "issues": [20, 23],
        "non_claims": [
            "Route reachability is bounded publication evidence only.",
            "Publication is not certification.",
            "Post-quantum cryptography does not independently grant execution authority.",
            "This receipt grants no downstream mutation authority.",
        ],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    print(
        "QUANTUM SECURITY PUBLIC ROUTES: " + ("PASS" if all_verified else "FAIL_CLOSED")
    )
    for name, observation in observations.items():
        print(f"- {name}: {observation['result']} {observation['url']}")

    return 0 if all_verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
