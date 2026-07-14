#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-summary.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-receipt.json"
PUBLIC_URL = "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-stability-change-frequency-summary.json"


def load_previous() -> tuple[dict | None, dict]:
    override = os.getenv("CANONICAL_STABILITY_CHANGE_FREQUENCY_SOURCE")
    if override:
        path = Path(override)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), {
                "source": str(path),
                "result": "LOCAL_SOURCE_LOADED",
            }
        return None, {"source": str(path), "result": "LOCAL_SOURCE_MISSING"}

    request = Request(
        PUBLIC_URL,
        headers={"User-Agent": "stegverse-stability-change-frequency-change-generator/1.0"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8")), {
                "source": PUBLIC_URL,
                "result": "PUBLIC_SUMMARY_LOADED",
                "http_status": int(getattr(response, "status", None) or response.getcode()),
            }
    except HTTPError as exc:
        return None, {
            "source": PUBLIC_URL,
            "result": "PUBLIC_SUMMARY_UNAVAILABLE",
            "http_status": exc.code,
        }
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, {
            "source": PUBLIC_URL,
            "result": "PUBLIC_SUMMARY_UNAVAILABLE",
            "error": str(exc),
        }


def main() -> int:
    if not CURRENT.exists():
        raise SystemExit("current stability-change frequency summary is missing")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    if current.get("manual_tasks_required") != [] or current.get("user_action_required") is not False:
        raise SystemExit("current stability-change frequency summary violates no-manual boundary")
    scope = current.get("evaluation_scope", {})
    if scope.get("descriptive_only") is not True:
        raise SystemExit("current stability-change frequency summary must remain descriptive")
    if scope.get("predictive_claim") is not False:
        raise SystemExit("current stability-change frequency summary must remain non-predictive")
    if scope.get("causal_claim_beyond_receipt_fields") is not False:
        raise SystemExit("current stability-change frequency summary exceeds causal claim boundary")

    previous, prior_observation = load_previous()
    prior_frequency = (previous or {}).get("frequency_class") or "AWAITING_AUTOMATED_STABILITY_CHANGE_FREQUENCY_SUMMARY"
    prior_recency = (previous or {}).get("recency_class") or "AWAITING_AUTOMATED_STABILITY_CHANGE_FREQUENCY_SUMMARY"
    resulting_frequency = current.get("frequency_class")
    resulting_recency = current.get("recency_class")
    if not isinstance(resulting_frequency, str) or not isinstance(resulting_recency, str):
        raise SystemExit("current stability-change frequency or recency class is missing")

    changed_fields: list[str] = []
    if prior_frequency != resulting_frequency:
        changed_fields.append("frequency_class")
    if prior_recency != resulting_recency:
        changed_fields.append("recency_class")
    change_state = "CHANGED" if changed_fields else "UNCHANGED"
    latest_receipt = current.get("evidence", {}).get("latest_change_receipt_id") or "awaiting"

    payload = {
        "schema": "admissibility_wiki.canonical_workflow_stability_change_frequency_change_receipt.v0.1",
        "receipt_id": f"workflow-stability-change-frequency-change.{latest_receipt}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-stability-change-frequency-change-receipt.json",
        "change_state": change_state,
        "changed_fields": changed_fields,
        "prior_frequency_class": prior_frequency,
        "resulting_frequency_class": resulting_frequency,
        "prior_recency_class": prior_recency,
        "resulting_recency_class": resulting_recency,
        "prior_summary_observation": prior_observation,
        "resulting_evidence": current.get("evidence"),
        "manual_tasks_required": [],
        "user_action_required": False,
        "change_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "descriptive_only": True,
        "predictive_claim": False,
        "causal_claim_beyond_receipt_fields": False,
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This receipt compares bounded descriptive stability-change frequency and recency classes only.",
            "A class change does not predict persistence or identify an independent cause.",
            "An unchanged result is recorded to preserve continuity.",
            "This receipt grants no release, deployment, execution, or downstream mutation authority.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY CHANGE: PASS - "
        f"change={change_state} fields={len(changed_fields)} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
