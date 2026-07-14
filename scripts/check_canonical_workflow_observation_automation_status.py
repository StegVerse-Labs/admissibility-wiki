#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "canonical-workflow-observation-automation.json"
REQUIRED_FILES = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "write_canonical_workflow_observation_receipt.py",
    ROOT / "scripts" / "check_canonical_workflow_observation_receipt.py",
    ROOT / "scripts" / "check_full_validation_chain.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION AUTOMATION: FAIL - {message}")


def main() -> int:
    if not STATUS.exists():
        fail("public status artifact is missing")
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"required automation file is missing: {path.relative_to(ROOT)}")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("state") != "AUTOMATED":
        fail("state must be AUTOMATED")
    if data.get("manual_tasks_required") != []:
        fail("manual_tasks_required must be empty")
    if data.get("user_action_required") is not False:
        fail("user_action_required must be false")
    if data.get("authority_granted") is not False:
        fail("authority_granted must be false")
    if data.get("release_authority_granted") is not False:
        fail("release_authority_granted must be false")
    if data.get("downstream_mutation_authority_granted") is not False:
        fail("downstream_mutation_authority_granted must be false")

    states = set(data.get("observation_states", []))
    required_states = {"PASS_OBSERVED", "FAIL_CLOSED_OBSERVED", "INCOMPLETE_OBSERVATION"}
    if states != required_states:
        fail("observation states do not match the governed set")

    triggers = data.get("trigger_ownership", {})
    for trigger in ("push", "pull_request", "workflow_dispatch", "hourly_schedule"):
        if triggers.get(trigger) != "repository automation":
            fail(f"trigger {trigger} is not automation-owned")

    if "next repository-owned trigger" not in data.get("cancelled_run_policy", ""):
        fail("cancelled-run policy must assign automatic re-evaluation")
    if "do not become user tasks" not in data.get("external_evidence_policy", ""):
        fail("external-evidence policy must prohibit user task assignment")

    non_claims = data.get("non_claims", [])
    if not any("does not grant" in claim for claim in non_claims):
        fail("authority non-claim is missing")

    print("CANONICAL WORKFLOW OBSERVATION AUTOMATION: PASS - manual_tasks=0 user_action=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
