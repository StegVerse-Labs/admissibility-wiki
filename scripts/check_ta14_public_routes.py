#!/usr/bin/env python3
"""Observe TA-14 public documentation routes and write a bounded receipt."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://stegverse-labs.github.io/admissibility-wiki"
ROUTES = {
    "ta14_doctrine": f"{BASE}/external-frameworks/ta-14",
    "ta14_registry_assessment": f"{BASE}/external-frameworks/ta-14-registry-public-record-assessment",
    "ta14_status": f"{BASE}/status/ta-14-standing-reconstruction-status.json",
    "ta14_fixture": f"{BASE}/data/framework-evaluations/test-cases/ta14-continuous-standing-revalidation-v1.json",
    "ta14_output_template": f"{BASE}/data/framework-evaluations/test-cases/ta14-continuous-standing-revalidation-output-template-v1.json",
}
RECEIPT = Path("reports/ta14-public-route-observation.json")


def check_url(url: str) -> tuple[bool, int | None, str]:
    request = Request(url, method="HEAD", headers={"User-Agent": "stegverse-ta14-public-route-verifier/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            status = int(getattr(response, "status", None) or response.getcode())
    except HTTPError as exc:
        return False, exc.code, f"{url} -> HTTP {exc.code}"
    except URLError as exc:
        return False, None, f"{url} -> {exc.reason}"
    except TimeoutError:
        return False, None, f"{url} -> timeout"
    return 200 <= status < 400, status, f"{url} -> HTTP {status}"


def main() -> int:
    results: dict[str, dict[str, object]] = {}
    failures: list[str] = []
    for name, url in ROUTES.items():
        ok, status, message = check_url(url)
        print(message)
        results[name] = {"url": url, "reachable": ok, "http_status": status}
        if not ok:
            failures.append(message)

    passed = not failures
    receipt = {
        "schema": "ta14_public_route_observation.v1",
        "goal_id": "ta14-continuous-actor-standing-reconstruction",
        "state": "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE" if passed else "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "routes": results,
        "all_required_public_routes_verified": passed,
        "pages_deployment_observed": passed,
        "continuous_actor_standing_reconstruction": "PUBLICLY_UNRESOLVED",
        "standing_revocation_fixture": "FROZEN_PROPOSED_NOT_RUN",
        "manual_task_requirement": "NONE",
        "user_manual_action_required": False,
        "certification_granted": False,
        "execution_authority_granted": False,
        "activation_authority_granted": False,
        "adverse_capability_conclusion": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "Public route reachability is bounded publication evidence only.",
            "Publication does not establish that TA-14 independently reconstructs current actor standing.",
            "The frozen fixture has not been executed against TA-14.",
            "A reachable output template is not a test result.",
            "This receipt grants no certification, execution authority, activation authority, or downstream mutation authority."
        ],
        "failures": failures,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RECEIPT}")
    if failures:
        print("TA-14 PUBLIC ROUTES: FAIL_CLOSED - one or more routes were not reachable")
        return 1
    print("TA-14 PUBLIC ROUTES: PASS - all bounded publication routes reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
