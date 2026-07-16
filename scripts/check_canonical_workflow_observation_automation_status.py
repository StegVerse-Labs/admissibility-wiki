#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_DIR = ROOT / "static" / "status"
STATUS = STATUS_DIR / "canonical-workflow-observation-automation.json"
VALIDATORS = [
    ROOT / "scripts" / "check_canonical_workflow_observation_publication.py",
    ROOT / "scripts" / "check_canonical_workflow_observation_history.py",
    ROOT / "scripts" / "check_canonical_workflow_health_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_receipt.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_history.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_trend.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_trend_change.py",
    ROOT / "scripts" / "check_canonical_workflow_health_transition_trend_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_trend_change_frequency_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_trend_change_frequency_change.py",
    ROOT / "scripts" / "check_canonical_workflow_trend_change_frequency_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_frequency_change_stability_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_frequency_change_stability_change.py",
    ROOT / "scripts" / "check_canonical_workflow_frequency_change_stability_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_stability_change_frequency_summary.py",
    ROOT / "scripts" / "check_canonical_workflow_stability_change_frequency_change.py",
    ROOT / "scripts" / "check_canonical_workflow_stability_change_frequency_change_history.py",
    ROOT / "scripts" / "check_canonical_workflow_observation_rollup.py",
]
REQUIRED = [
    ROOT / ".github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml",
    ROOT / "scripts" / "reconcile_canonical_workflow_stability_change_frequency_change_history.py",
    ROOT / "scripts" / "generate_canonical_workflow_observation_rollup.py",
    ROOT / "scripts" / "check_full_validation_chain.py",
] + VALIDATORS


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL WORKFLOW OBSERVATION AUTOMATION: FAIL - {message}")


def snapshot_status_directory(snapshot_root: Path) -> None:
    if STATUS_DIR.exists():
        shutil.copytree(STATUS_DIR, snapshot_root / "status")


def restore_status_directory(snapshot_root: Path) -> None:
    prior = snapshot_root / "status"
    if STATUS_DIR.exists():
        shutil.rmtree(STATUS_DIR)
    if prior.exists():
        shutil.copytree(prior, STATUS_DIR)
    else:
        STATUS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    if not STATUS.exists():
        fail("status artifact missing")
    for path in REQUIRED:
        if not path.exists():
            fail(f"required file missing: {path.relative_to(ROOT)}")

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("state") != "AUTOMATED_TERMINAL_OBSERVATION_ROLLUP_BOUND":
        fail("state mismatch")
    if data.get("manual_tasks_required") != [] or data.get("user_action_required") is not False:
        fail("no-manual boundary violated")
    for key in ("authority_granted", "release_authority_granted", "downstream_mutation_authority_granted"):
        if data.get(key) is not False:
            fail(f"{key} must be false")

    if data.get("terminal_rollup_endpoint") != "/status/canonical-workflow-observation-rollup.json":
        fail("terminal rollup endpoint mismatch")
    policy = data.get("terminal_rollup_policy", {})
    if policy.get("terminal_envelope") is not True:
        fail("terminal_envelope must be true")
    if policy.get("recursive_derivative_expansion_allowed") is not False:
        fail("recursive derivative expansion must be disabled")
    if policy.get("artifact_count") != 17:
        fail("terminal rollup artifact_count must be 17")
    if set(policy.get("local_presence_states", [])) != {"PRESENT", "MISSING"}:
        fail("local presence states mismatch")
    if set(policy.get("completeness_states", [])) != {
        "COMPLETE_LOCAL_CHAIN",
        "FAIL_CLOSED_INCOMPLETE_LOCAL_CHAIN",
    }:
        fail("completeness states mismatch")
    if policy.get("public_reachability_before_deploy") != "NOT_OBSERVED_UNTIL_POST_DEPLOY_VERIFICATION":
        fail("pre-deploy reachability boundary mismatch")
    if policy.get("semantic_reclassification_performed") is not False:
        fail("terminal rollup must not reclassify semantic meaning")
    if policy.get("owner") != "canonical build-pages job":
        fail("terminal rollup owner mismatch")
    if policy.get("next_evaluation") != "next repository-owned canonical workflow trigger":
        fail("terminal rollup evaluation must remain automation-owned")

    chain = data.get("publication_chain", [])
    for phrase in (
        "build-pages generates one terminal rollup envelope pointing to the latest governed artifacts",
        "the terminal rollup records local presence, generation ownership, public endpoints, and fail-closed completeness without semantic reclassification",
        "verify-public-pages checks the terminal rollup endpoint and the referenced public endpoint set",
    ):
        if phrase not in chain:
            fail(f"publication chain missing: {phrase}")

    for trigger in ("push", "pull_request", "workflow_dispatch", "hourly_schedule"):
        if data.get("trigger_ownership", {}).get(trigger) != "repository automation":
            fail(f"trigger {trigger} is not automation-owned")

    for validator in VALIDATORS:
        with tempfile.TemporaryDirectory(prefix="canonical-observation-validator-") as tmp:
            snapshot_root = Path(tmp)
            snapshot_status_directory(snapshot_root)
            try:
                completed = subprocess.run(
                    [sys.executable, str(validator)], cwd=ROOT, text=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
                )
            finally:
                restore_status_directory(snapshot_root)
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.returncode != 0:
            fail(f"validator failed: {validator.name}")

    print(
        "CANONICAL WORKFLOW OBSERVATION AUTOMATION: PASS - "
        "manual_tasks=0 terminal_rollup=bound recursive_expansion=false validators_isolated=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
