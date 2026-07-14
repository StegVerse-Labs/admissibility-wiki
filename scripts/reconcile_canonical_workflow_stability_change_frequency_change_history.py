#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-receipt.json"
HISTORY = ROOT / "static" / "status" / "canonical-workflow-stability-change-frequency-change-history.json"
ROLLUP_GENERATOR = ROOT / "scripts" / "generate_canonical_workflow_observation_rollup.py"
PUBLIC_HISTORY_URL = "https://stegverse-labs.github.io/admissibility-wiki/status/canonical-workflow-stability-change-frequency-change-history.json"
MAX_ENTRIES = 24


def load_previous() -> tuple[list[dict], dict]:
    override = os.getenv("CANONICAL_STABILITY_CHANGE_FREQUENCY_CHANGE_HISTORY_SOURCE")
    if override:
        path = Path(override)
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            return list(payload.get("changes", [])), {"source": str(path), "result": "LOCAL_SOURCE_LOADED"}
        return [], {"source": str(path), "result": "LOCAL_SOURCE_MISSING"}

    request = Request(PUBLIC_HISTORY_URL, headers={"User-Agent": "stegverse-stability-change-frequency-change-history/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return list(payload.get("changes", [])), {
                "source": PUBLIC_HISTORY_URL,
                "result": "PUBLIC_HISTORY_LOADED",
                "http_status": int(getattr(response, "status", None) or response.getcode()),
            }
    except HTTPError as exc:
        return [], {"source": PUBLIC_HISTORY_URL, "result": "PUBLIC_HISTORY_UNAVAILABLE", "http_status": exc.code}
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return [], {"source": PUBLIC_HISTORY_URL, "result": "PUBLIC_HISTORY_UNAVAILABLE", "error": str(exc)}


def main() -> int:
    if not CURRENT.exists():
        raise SystemExit("current stability-change frequency comparison receipt is missing")

    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    if current.get("manual_tasks_required") != [] or current.get("user_action_required") is not False:
        raise SystemExit("current comparison receipt violates no-manual boundary")
    if current.get("descriptive_only") is not True:
        raise SystemExit("current comparison receipt must remain descriptive")
    if current.get("predictive_claim") is not False:
        raise SystemExit("current comparison receipt must remain non-predictive")
    if current.get("causal_claim_beyond_receipt_fields") is not False:
        raise SystemExit("current comparison receipt exceeds causal claim boundary")

    previous, prior_history = load_previous()
    by_id: dict[str, dict] = {}
    for item in previous:
        receipt_id = item.get("receipt_id")
        if isinstance(receipt_id, str) and receipt_id:
            by_id[receipt_id] = item

    receipt_id = current.get("receipt_id")
    if not isinstance(receipt_id, str) or not receipt_id:
        raise SystemExit("current comparison receipt_id is missing")
    by_id[receipt_id] = current

    ordered = sorted(by_id.values(), key=lambda item: str(item.get("generated_at", "")))[-MAX_ENTRIES:]
    latest = ordered[-1] if ordered else current
    counts = {state: sum(1 for item in ordered if item.get("change_state") == state) for state in ("CHANGED", "UNCHANGED")}
    field_counts = {
        field: sum(1 for item in ordered if field in item.get("changed_fields", []))
        for field in ("frequency_class", "recency_class")
    }
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_stability_change_frequency_change_history.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-stability-change-frequency-change-history.json",
        "retention_policy": {
            "maximum_entries": MAX_ENTRIES,
            "deduplication_key": "receipt_id",
            "ordering": "generated_at ascending",
            "supersession": "new comparison receipts append; duplicate receipt identifiers replace prior copies; bounded retention removes the oldest entry",
        },
        "prior_history_observation": prior_history,
        "latest_change": {
            "receipt_id": latest.get("receipt_id"),
            "generated_at": latest.get("generated_at"),
            "change_state": latest.get("change_state"),
            "changed_fields": latest.get("changed_fields", []),
            "prior_frequency_class": latest.get("prior_frequency_class"),
            "resulting_frequency_class": latest.get("resulting_frequency_class"),
            "prior_recency_class": latest.get("prior_recency_class"),
            "resulting_recency_class": latest.get("resulting_recency_class"),
        },
        "change_state_counts": counts,
        "changed_field_counts": field_counts,
        "changes": ordered,
        "manual_tasks_required": [],
        "user_action_required": False,
        "reconciliation_owner": "canonical build-pages job",
        "next_reconciliation": "next repository-owned canonical workflow trigger",
        "descriptive_only": True,
        "predictive_claim": False,
        "causal_claim_beyond_receipt_fields": False,
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "Comparison history records bounded descriptive workflow evidence only.",
            "Unavailable prior public history initializes a new bounded sequence without creating a manual task.",
            "History counts do not predict future class changes or establish an independent cause.",
            "History retention grants no release, deployment, execution, or downstream mutation authority.",
        ],
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW STABILITY CHANGE FREQUENCY CHANGE HISTORY: PASS - "
        f"entries={len(ordered)} latest={latest.get('change_state')} prior={prior_history.get('result')} manual_tasks=0"
    )

    if not ROLLUP_GENERATOR.exists():
        raise SystemExit("terminal workflow observation rollup generator is missing")
    completed = subprocess.run(
        [sys.executable, str(ROLLUP_GENERATOR)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit("terminal workflow observation rollup generation failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
