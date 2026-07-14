#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = [
    ROOT / "reports" / "upstream-full-validation" / "full_validation_chain_report.json",
    ROOT / "reports" / "full_validation_chain_report.json",
]
PUBLIC = ROOT / "static" / "status" / "canonical-workflow-observation-receipt.json"


def fail(message: str) -> None:
    raise SystemExit(f"PUBLISH CANONICAL WORKFLOW OBSERVATION RECEIPT: FAIL - {message}")


def main() -> int:
    source = next((path for path in CANDIDATES if path.exists()), None)
    if source is None:
        fail("full validation report is missing")

    report = json.loads(source.read_text(encoding="utf-8"))
    observation = report.get("canonical_workflow_observation")
    if not isinstance(observation, dict):
        fail("embedded canonical workflow observation receipt is missing")

    if observation.get("manual_tasks_required") != []:
        fail("embedded observation assigns manual tasks")
    if observation.get("user_action_required") is not False:
        fail("embedded observation requires user action")
    if observation.get("observation_state") not in {
        "PASS_OBSERVED",
        "FAIL_CLOSED_OBSERVED",
        "INCOMPLETE_OBSERVATION",
    }:
        fail("embedded observation state is invalid")

    published = dict(observation)
    published["publication"] = {
        "repository": "StegVerse-Labs/admissibility-wiki",
        "source_report": str(source.relative_to(ROOT)),
        "published_path": "static/status/canonical-workflow-observation-receipt.json",
        "public_endpoint": "/status/canonical-workflow-observation-receipt.json",
        "publisher": "scripts/publish_canonical_workflow_observation_receipt.py",
        "build_run_id": os.getenv("GITHUB_RUN_ID"),
        "build_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "manual_tasks_required": [],
        "user_action_required": False,
    }
    published.setdefault("non_claims", []).append(
        "Public reachability of this receipt does not grant merge, release, deployment, execution, or downstream mutation authority."
    )

    PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC.write_text(json.dumps(published, indent=2) + "\n", encoding="utf-8")
    print(
        "PUBLISH CANONICAL WORKFLOW OBSERVATION RECEIPT: PASS - "
        f"state={published['observation_state']} source={source.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
