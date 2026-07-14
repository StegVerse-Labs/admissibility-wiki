#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "canonical-workflow-observation-receipt.json"
FULL_REPORT = ROOT / "reports" / "full_validation_chain_report.json"
RECONSTRUCTION = ROOT / "reports" / "external-translation-reconstruction-receipt.json"


def load_optional(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"unreadable": True, "error": str(exc)}


def main() -> int:
    job_status = os.getenv("CANONICAL_JOB_STATUS", "unknown")
    full_report = load_optional(FULL_REPORT)
    reconstruction = load_optional(RECONSTRUCTION)

    full_status = full_report.get("overall_status") if isinstance(full_report, dict) else None
    reconstruction_status = (
        reconstruction.get("evaluation_result")
        if isinstance(reconstruction, dict)
        else None
    )

    receipt = {
        "schema": "admissibility_wiki.canonical_workflow_observation_receipt.v0.1",
        "receipt_id": f"canonical-workflow-observation.{os.getenv('GITHUB_RUN_ID', 'local')}.{os.getenv('GITHUB_RUN_ATTEMPT', '0')}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "workflow": "Validate chain continuation",
        "event_name": os.getenv("GITHUB_EVENT_NAME", "local"),
        "ref": os.getenv("GITHUB_REF"),
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "job_status_observed": job_status,
        "full_validation_status": full_status,
        "reconstruction_evaluation_result": reconstruction_status,
        "automation_ownership": {
            "validation": "validate-chain-continuation job",
            "receipt_generation": "scripts/write_canonical_workflow_observation_receipt.py",
            "artifact_retention": "canonical workflow artifact upload",
            "scheduled_reobservation": "hourly canonical workflow schedule"
        },
        "manual_tasks_required": [],
        "user_action_required": False,
        "observation_state": (
            "PASS_OBSERVED"
            if job_status == "success" and full_status == "PASS"
            else "FAIL_CLOSED_OBSERVED"
            if job_status in {"failure", "cancelled"} or full_status == "FAIL"
            else "INCOMPLETE_OBSERVATION"
        ),
        "non_claims": [
            "This receipt records one workflow-run observation only.",
            "It does not grant merge, release, deployment, publication, execution, or downstream mutation authority.",
            "A cancelled or failed run remains fail-closed and does not assign a manual task to the user.",
            "External evidence conditions remain owned by their declared intake and review processes."
        ]
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)}: {receipt['observation_state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
