#!/usr/bin/env python3
"""Check governed documentation routes without mutating repository state."""
from __future__ import annotations
import json, os
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
    "verification_execution_authority_doctrine": "https://stegverse-labs.github.io/admissibility-wiki/governance/verification-vs-execution-authority",
    "verification_execution_authority_status": "https://stegverse-labs.github.io/admissibility-wiki/status/verification-execution-authority-status.json",
    "optimization_target_doctrine": "https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit",
    "optimization_target_formalism_json": "https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit.v0.1.json",
    "optimization_target_publication_status": "https://stegverse-labs.github.io/admissibility-wiki/status/optimization-target-binding-publication-verification.json",
    "external_translation_reconstruction_receipt": "https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json",
    "canonical_workflow_observation_automation": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-observation-automation.json",
    "canonical_workflow_observation_receipt": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-observation-receipt.json",
    "canonical_workflow_observation_history": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-observation-history.json",
    "canonical_workflow_health_summary": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-summary.json",
    "canonical_workflow_health_transition_receipt": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-transition-receipt.json",
    "canonical_workflow_health_transition_history": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-transition-history.json",
    "canonical_workflow_health_transition_trend": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-transition-trend.json",
    "canonical_workflow_health_transition_trend_change_receipt": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-transition-trend-change-receipt.json",
    "canonical_workflow_health_transition_trend_change_history": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-transition-trend-change-history.json",
    "canonical_workflow_trend_change_frequency_summary": "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-trend-change-frequency-summary.json",
    "kpt_external_framework_page": "https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/kpt",
    "kpt_external_framework_status": "https://stegverse-labs.github.io/admissibility-wiki/status/kpt-external-framework-intake-status.json",
}
RECEIPT = Path("reports/optimization-target-publication-verification-receipt.json")

def check_url(url: str):
    request = Request(url, method="HEAD", headers={"User-Agent": "stegverse-admissibility-verifier/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            status = int(getattr(response, "status", None) or response.getcode())
    except HTTPError as exc: return False, exc.code, f"{url} -> HTTP {exc.code}"
    except URLError as exc: return False, None, f"{url} -> {exc.reason}"
    except TimeoutError: return False, None, f"{url} -> timeout"
    return 200 <= status < 400, status, f"{url} -> HTTP {status}"

def main() -> int:
    results, failures = {}, []
    for name, url in PAGES.items():
        ok, status, message = check_url(url); print(message)
        results[name] = {"url": url, "reachable": ok, "http_status": status}
        if not ok: failures.append(message)
    receipt = {
        "schema": "stegverse.optimization_target_publication_verification_receipt.v0.11",
        "receipt_id": f"optimization-target-publication.workflow.{os.getenv('GITHUB_RUN_ID','local')}.{os.getenv('GITHUB_RUN_ATTEMPT','0')}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"), "run_id": os.getenv("GITHUB_RUN_ID"), "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "verification_result": "PASS" if not failures else "FAIL_CLOSED", "routes": results,
        "manual_tasks_required": [], "user_action_required": False,
        "authority_granted": False, "proof_authority_granted": False, "release_authority_granted": False,
        "source_sufficiency_granted": False, "interoperability_standing_granted": False,
        "execution_authority_granted": False, "downstream_mutation_authority_granted": False,
        "non_claims": [
            "Route reachability is bounded publication evidence only.",
            "Published verification doctrine does not grant execution authority.",
            "Trend frequency and recency reachability do not make predictive or independent causal claims.",
            "Failed checks remain fail-closed and create no user task."
        ]
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True); RECEIPT.write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    print(f"wrote {RECEIPT}")
    if failures:
        print("GOVERNED DOCUMENTATION DEPLOYMENT: PENDING - public routes not fully confirmed"); return 1
    print("GOVERNED DOCUMENTATION DEPLOYMENT: PASS - public routes reachable"); return 0

if __name__ == "__main__": raise SystemExit(main())
