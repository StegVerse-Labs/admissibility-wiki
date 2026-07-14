#!/usr/bin/env python3
"""Check governed documentation routes without mutating repository state.

The canonical verify-public-pages job runs this script after GitHub Pages deploys.
It verifies the established governed-LLM route set, optimization-target artifacts,
the generated external-translation reconstruction receipt, and the public
no-manual canonical-workflow observation automation status. A PASS is
run-specific reachability evidence only; it does not establish admissibility,
proof authority, release authority, or downstream mutation authority.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PAGES = {
    "governed_llm_reconstructive_search": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-reconstructive-search",
    "governed_llm_activation_map": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-activation-map",
    "governed_llm_demo_overview": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-overview",
    "governed_llm_demo_verification": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-verification",
    "governed_llm_site_verification": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-site-verification",
    "governed_llm_deployment_status": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-deployment-status",
    "governed_llm_archive_handoff": "https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-archive-handoff",
    "optimization_target_doctrine": "https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit",
    "optimization_target_formalism_json": "https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit.v0.1.json",
    "optimization_target_publication_status": "https://stegverse-labs.github.io/admissibility-wiki/status/optimization-target-binding-publication-verification.json",
    "external_translation_reconstruction_receipt": "https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json",
    "canonical_workflow_observation_automation": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-observation-automation.json",
}

RECEIPT = Path("reports/optimization-target-publication-verification-receipt.json")


def check_url(url: str) -> tuple[bool, int | None, str]:
    request = Request(url, method="HEAD", headers={"User-Agent": "stegverse-admissibility-verifier/1.0"})
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


def write_receipt(results: dict[str, dict[str, object]], passed: bool) -> None:
    receipt = {
        "schema": "stegverse.optimization_target_publication_verification_receipt.v0.3",
        "receipt_id": f"optimization-target-publication.workflow.{os.getenv('GITHUB_RUN_ID', 'local')}.{os.getenv('GITHUB_RUN_ATTEMPT', '0')}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "verification_result": "PASS" if passed else "FAIL_CLOSED",
        "routes": results,
        "manual_tasks_required": [],
        "user_action_required": False,
        "authority_granted": False,
        "proof_authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "Route reachability does not prove admissibility or executable correctness.",
            "The external-translation receipt endpoint proves publication of a generated reconstruction artifact only.",
            "The canonical-workflow observation endpoint proves publication of the automation contract only, not future run success.",
            "A failed public check remains fail-closed and does not create a user task.",
            "This receipt does not replace canonical workflow or GitHub Pages deployment records.",
            "This receipt does not authorize Site, Publisher, Guardian, release, or custody mutation.",
        ],
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RECEIPT}")


def main() -> int:
    results: dict[str, dict[str, object]] = {}
    failures: list[str] = []
    for name, url in PAGES.items():
        ok, status, message = check_url(url)
        print(message)
        results[name] = {"url": url, "reachable": ok, "http_status": status}
        if not ok:
            failures.append(message)

    passed = not failures
    write_receipt(results, passed)
    if not passed:
        print("GOVERNED DOCUMENTATION DEPLOYMENT: PENDING - public routes not fully confirmed")
        return 1

    print("GOVERNED DOCUMENTATION DEPLOYMENT: PASS - public routes reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
