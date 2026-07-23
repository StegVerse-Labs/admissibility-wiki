#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "discovery-governance-handoff-status.json"
HANDOFF = ROOT / "docs" / "DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md"

EXPECTED_STATE = "SOURCE_COMPLETE_WITH_CANONICAL_RUNTIME_VALIDATION_PENDING_WORKFLOW_OBSERVATION"
EXPECTED_CRITERIA = (
    "canonical_dependency_chain_observed",
    "proof_receipt_pass",
    "four_outcomes_preserved",
    "all_five_public_routes_verified",
    "publication_state_complete",
    "pages_deployment_observed",
    "standalone_embedded_closure_exact_match",
    "linked_publication_receipt_bound",
    "public_activation_publication_complete",
    "receipt_run_identity_match",
    "input_sha256_digests_present",
    "authority_boundary_preserved",
)
REQUIRED_HANDOFF_MARKERS = (
    f"State: {EXPECTED_STATE}",
    "scripts/check_discovery_governance_activation_evidence_runtime.py",
    "ACTIVATION_EVIDENCE_COMPLETE",
    "ACTIVATION_EVIDENCE_FAIL_CLOSED",
    "goal_completion_observed",
    "The complete thread is not ready for archiving",
    "No destination mutation is authorized by this handoff.",
)


def main() -> int:
    failures: list[str] = []
    if not STATUS.exists():
        failures.append("missing static/status/discovery-governance-handoff-status.json")
        status = {}
    else:
        status = json.loads(STATUS.read_text(encoding="utf-8"))

    if not HANDOFF.exists():
        failures.append("missing docs/DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md")
        handoff_text = ""
    else:
        handoff_text = HANDOFF.read_text(encoding="utf-8")

    if status.get("state") != EXPECTED_STATE:
        failures.append("status state does not match authoritative handoff state")
    if status.get("goal_id") != "discovery-governance-minimum-handoff":
        failures.append("status goal_id mismatch")
    if status.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("status repository mismatch")
    if status.get("activation_evidence_runtime_checker") != "scripts/check_discovery_governance_activation_evidence_runtime.py":
        failures.append("status runtime checker binding mismatch")
    if tuple(status.get("completion_criteria", [])) != EXPECTED_CRITERIA:
        failures.append("status completion criteria differ from authoritative completion contract")
    if status.get("manual_task_requirement") != "none":
        failures.append("status manual task requirement must remain none")
    if status.get("user_manual_action_required") is not False:
        failures.append("status user manual action must remain false")
    if status.get("downstream_mutation_authority") != "none granted":
        failures.append("status downstream mutation authority must remain none granted")

    for marker in REQUIRED_HANDOFF_MARKERS:
        if marker not in handoff_text:
            failures.append(f"handoff missing marker: {marker}")
    for criterion in EXPECTED_CRITERIA:
        if criterion not in handoff_text:
            failures.append(f"handoff missing completion criterion: {criterion}")

    stale_archive_claim = "The complete thread is ready for archiving without any additional part of the thread needed to move forward."
    if stale_archive_claim in handoff_text:
        failures.append("handoff contains stale archive-ready claim while run-bound evidence is pending")

    if failures:
        print("DISCOVERY GOVERNANCE HANDOFF SYNC: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE HANDOFF SYNC: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
