#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "status" / "canonical-workflow-observation-rollup.json"

ARTIFACTS = [
    ("observation_receipt", "canonical-workflow-observation-receipt.json", "canonical validation and publication chain"),
    ("observation_history", "canonical-workflow-observation-history.json", "canonical build-pages job"),
    ("health_summary", "canonical-workflow-health-summary.json", "canonical build-pages job"),
    ("health_transition_receipt", "canonical-workflow-health-transition-receipt.json", "canonical build-pages job"),
    ("health_transition_history", "canonical-workflow-health-transition-history.json", "canonical build-pages job"),
    ("health_transition_trend", "canonical-workflow-health-transition-trend.json", "canonical build-pages job"),
    ("health_transition_trend_change_receipt", "canonical-workflow-health-transition-trend-change-receipt.json", "canonical build-pages job"),
    ("health_transition_trend_change_history", "canonical-workflow-health-transition-trend-change-history.json", "canonical build-pages job"),
    ("trend_change_frequency_summary", "canonical-workflow-trend-change-frequency-summary.json", "canonical build-pages job"),
    ("trend_change_frequency_change_receipt", "canonical-workflow-trend-change-frequency-change-receipt.json", "canonical build-pages job"),
    ("trend_change_frequency_change_history", "canonical-workflow-trend-change-frequency-change-history.json", "canonical build-pages job"),
    ("frequency_change_stability_summary", "canonical-workflow-frequency-change-stability-summary.json", "canonical build-pages job"),
    ("frequency_change_stability_change_receipt", "canonical-workflow-frequency-change-stability-change-receipt.json", "canonical build-pages job"),
    ("frequency_change_stability_change_history", "canonical-workflow-frequency-change-stability-change-history.json", "canonical build-pages job"),
    ("stability_change_frequency_summary", "canonical-workflow-stability-change-frequency-summary.json", "canonical build-pages job"),
    ("stability_change_frequency_change_receipt", "canonical-workflow-stability-change-frequency-change-receipt.json", "canonical build-pages job"),
    ("stability_change_frequency_change_history", "canonical-workflow-stability-change-frequency-change-history.json", "canonical build-pages job"),
]


def main() -> int:
    records = []
    missing = []
    for artifact_id, filename, owner in ARTIFACTS:
        path = ROOT / "static" / "status" / filename
        present = path.exists()
        if not present:
            missing.append(artifact_id)
        records.append(
            {
                "artifact_id": artifact_id,
                "repository_path": f"static/status/{filename}",
                "public_endpoint": f"/status/{filename}",
                "generation_owner": owner,
                "local_presence": "PRESENT" if present else "MISSING",
                "public_reachability": "NOT_OBSERVED_UNTIL_POST_DEPLOY_VERIFICATION",
                "semantic_reclassification_performed": False,
            }
        )

    completeness_state = "COMPLETE_LOCAL_CHAIN" if not missing else "FAIL_CLOSED_INCOMPLETE_LOCAL_CHAIN"
    payload = {
        "schema": "admissibility_wiki.canonical_workflow_observation_rollup.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "public_endpoint": "/status/canonical-workflow-observation-rollup.json",
        "terminal_envelope": True,
        "recursive_derivative_expansion_allowed": False,
        "completeness_state": completeness_state,
        "artifact_count": len(records),
        "present_count": len(records) - len(missing),
        "missing_count": len(missing),
        "missing_artifact_ids": missing,
        "artifacts": records,
        "generation_owner": "canonical build-pages job",
        "next_evaluation": "next repository-owned canonical workflow trigger",
        "manual_tasks_required": [],
        "user_action_required": False,
        "authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "non_claims": [
            "This terminal envelope reports artifact pointers, presence, ownership, and bounded completeness only.",
            "It does not reinterpret scientific, governance, authority, or admissibility meaning from referenced artifacts.",
            "Public reachability remains unobserved until the post-deployment verifier checks the endpoint set.",
            "Incomplete local presence fails closed and does not create a manual task for the user.",
            "This envelope grants no release, deployment, execution, or downstream mutation authority.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        "CANONICAL WORKFLOW OBSERVATION ROLLUP: PASS - "
        f"state={completeness_state} present={payload['present_count']} missing={payload['missing_count']} manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
