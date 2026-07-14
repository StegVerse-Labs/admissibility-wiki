#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-summary.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-frequency-change-stability-change-receipt.json"
PUBLIC_SUMMARY_URL = "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-frequency-change-stability-summary.json"


def load_previous() -> tuple[dict | None, dict]:
    override = os.getenv("CANONICAL_FREQUENCY_CHANGE_STABILITY_SOURCE")
    if override:
        path = Path(override)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), {
                "source": str(path),
                "result": "LOCAL_SOURCE_LOADED",
            }
        return None, {"source": str(path), "result": "LOCAL_SOURCE_MISSING"}

    request = Request(
        PUBLIC_SUMMARY_URL,
        headers={"User-Agent": "stegverse-frequency-stability-change-generator/1.0"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8")), {
                "source": PUBLIC_SUMMARY_URL,
                "result": "PUBLIC_SUMMARY_LOADED",
                "http_status": int(getattr(response, "status", None) or response.getcode()),
            }
    except HTTPError as exc:
        return None, {
            "source": PUBLIC_SUMMARY_URL,
            "result": "PUBLIC_SUMMARY_UNAVAILABLE",
            "http_status": exc.code,
        }
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, {
            "source": PUBLIC_SUMMARY_URL,
            "result": "PUBLIC_SUMMARY_UNAVAILABLE",
            "error": str(exc),
        }


def main() -> int:
    if not CURRENT.exists():
        raise SystemExit("current workflow frequency-change stability summary is missing")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    if current.get("manual_tasks_required") != [] or current.get("user_action_required") is not False:
        raise SystemExit("current stability summary violates no-manual boundary")
    scope = current.get("evaluation_scope", {})
    if scope.get("descriptive_only") is not True:
        raise SystemExit("current stability summary must remain descriptive")
    if scope.get("predictive_claim") is not False:
        raise SystemExit("current stability summary must remain non-predictive")
    if scope.get("causal_claim_beyond_receipt_fields") is not False:
        raise SystemExit("current stability summary exceeds causal claim boundary")

    previous, prior_observation = load_previous()
    prior_class = (previous or {}).get("stability_class") or "AWAITING_AUTOMATED_STABILITY_SUMMARY"
    resulting_class = current.get("stability_class")
    if not isinstance(resulting_class, str) or not resulting_class:
        raise SystemExit("current stability_class is missing")

    change_state = "CHANGED" if prior_class != resulting_class else "UNCHANGED"
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_frequency_change_stability_change_receipt.v0.1",
        "receipt_id": f"workflow-frequency-stability-change.{current.get('evidence', {}).get('latest_change_receipt_id') or 'awaiting'}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-frequency-change-stability-change-receipt.json",
        "change_state": change_state,
        "prior_stability_class": prior_class,
        "resulting_stability_class": resulting_class,
        "prior_summary_observation": prior_observation,
        "resulting_evidence": current.get("evidence"),
        "automation_response": current.get("automation_response"),
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
            "This receipt compares bounded descriptive stability classes only.",
            "An unchanged class is recorded to preserve continuity.",
            "A stable or changing class does not predict future workflow behavior.",
            "This receipt does not grant release, deployment, execution, or downstream mutation authority.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW FREQUENCY CHANGE STABILITY CHANGE: PASS - "
        f"change={change_state} prior={prior_class} resulting={resulting_class} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
