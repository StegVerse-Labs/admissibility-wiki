#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend.json"
OUT = ROOT / "static" / "status" / "canonical-workflow-health-transition-trend-change-receipt.json"
PUBLIC_TREND_URL = "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-health-transition-trend.json"


def load_previous() -> tuple[dict | None, dict]:
    override = os.getenv("CANONICAL_HEALTH_TRANSITION_TREND_SOURCE")
    if override:
        path = Path(override)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")), {
                "source": str(path),
                "result": "LOCAL_SOURCE_LOADED",
            }
        return None, {"source": str(path), "result": "LOCAL_SOURCE_MISSING"}

    request = Request(PUBLIC_TREND_URL, headers={"User-Agent": "stegverse-trend-change-generator/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8")), {
                "source": PUBLIC_TREND_URL,
                "result": "PUBLIC_TREND_LOADED",
                "http_status": int(getattr(response, "status", None) or response.getcode()),
            }
    except HTTPError as exc:
        return None, {"source": PUBLIC_TREND_URL, "result": "PUBLIC_TREND_UNAVAILABLE", "http_status": exc.code}
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, {"source": PUBLIC_TREND_URL, "result": "PUBLIC_TREND_UNAVAILABLE", "error": str(exc)}


def main() -> int:
    if not CURRENT.exists():
        raise SystemExit("current workflow health-transition trend is missing")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    if current.get("manual_tasks_required") != [] or current.get("user_action_required") is not False:
        raise SystemExit("current trend violates no-manual boundary")
    if current.get("evaluation_scope", {}).get("predictive_claim") is not False:
        raise SystemExit("current trend must remain non-predictive")

    previous, prior_observation = load_previous()
    prior_class = (previous or {}).get("trend_class") or "AWAITING_AUTOMATED_TREND"
    resulting_class = current.get("trend_class")
    if not isinstance(resulting_class, str) or not resulting_class:
        raise SystemExit("current trend_class is missing")

    change_state = "CHANGED" if prior_class != resulting_class else "UNCHANGED"
    generated_at = datetime.now(timezone.utc).isoformat()
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_health_transition_trend_change_receipt.v0.1",
        "receipt_id": f"workflow-trend-change.{current.get('history_binding', {}).get('latest_transition_receipt_id') or 'awaiting'}",
        "generated_at": generated_at,
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-health-transition-trend-change-receipt.json",
        "change_state": change_state,
        "prior_trend_class": prior_class,
        "resulting_trend_class": resulting_class,
        "prior_trend_observation": prior_observation,
        "resulting_evidence": current.get("evidence"),
        "automation_response": current.get("automation_response"),
        "manual_tasks_required": [],
        "user_action_required": False,
        "change_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "predictive_claim": False,
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This receipt records a change between bounded descriptive trend classes only.",
            "An unchanged trend is recorded to preserve continuity.",
            "A recovery or stable trend class does not predict persistence.",
            "This receipt does not grant release, deployment, execution, or downstream mutation authority."
        ]
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW HEALTH TRANSITION TREND CHANGE: PASS - "
        f"change={change_state} prior={prior_class} resulting={resulting_class} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())