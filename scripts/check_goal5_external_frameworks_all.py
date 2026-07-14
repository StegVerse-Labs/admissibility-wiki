#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "goal5_external_frameworks_report.json"
SYNC_SCRIPT = "scripts/sync_external_chat_activation_evidence.py"

CHECKS = [
    "scripts/check_runtime_governance_benchmark_suite.py",
    "scripts/check_morrison_runtime_benchmark_fixtures.py",
    "scripts/check_morrison_validation_table_visibility.py",
    "scripts/check_external_framework_reports.py",
    "scripts/check_external_framework_benchmark_mappings.py",
    "scripts/check_external_framework_benchmark_fixtures.py",
    "scripts/check_judgment_architecture_commitment_fixtures.py",
    "scripts/check_judgment_architecture_commit_boundary_crosswalk.py",
    "scripts/check_judgment_architecture_binding_adapter.py",
    "scripts/check_judgment_architecture_source_citation_status.py",
    "scripts/check_observed_evidence_capture_queue.py",
    "scripts/check_opa_observation_capture_harness.py",
    "scripts/check_opa_version_probe_compatibility.py",
    "scripts/check_cedar_observation_capture_harness.py",
    "scripts/check_priority_command_capture_harnesses.py",
    "scripts/check_external_framework_evidence_tooling_coverage.py",
    "scripts/check_external_framework_implementation_selection_gates.py",
    "scripts/check_cedar_implementation_selection_evidence.py",
    "scripts/check_cedar_selected_binary_build_harness.py",
    "scripts/check_cedar_binary_promotion_automation.py",
    "scripts/check_cedar_binary_registry_promotion_receipts.py",
    "scripts/check_cedar_binary_hash_registry_application.py",
    "scripts/check_cedar_binary_provenance_reconciliation.py",
    "scripts/check_external_framework_automation_readiness.py",
    "scripts/check_external_framework_execution_plans.py",
    "scripts/check_external_framework_job_materialization_candidates.py",
    "scripts/check_external_framework_job_materialization_receipt.py",
    "scripts/check_external_framework_runtime_authorization_receipt.py",
    "scripts/check_external_framework_runtime_dispatch_observation.py",
    "scripts/check_external_framework_runtime_dispatch_progression.py",
    "scripts/check_pages_build_verification_receipt.py",
    "scripts/check_pages_build_verification_candidate.py",
    "scripts/check_pages_artifact_binding_receipt.py",
    "scripts/check_pages_build_status_promotion_receipt.py",
    "scripts/check_pages_build_verification_status_application.py",
    "scripts/check_pages_deployment_observation_receipt.py",
    "scripts/check_pages_public_endpoint_verification_receipt.py",
    "scripts/check_external_chat_review_packets.py",
    "scripts/check_external_chat_activation_evidence.py",
    "scripts/check_external_chat_activation_importer.py",
    "scripts/check_external_chat_activation_sync.py",
    "scripts/check_external_chat_activation_observation_candidate.py",
    "scripts/check_external_chat_activation_status_promotion_receipt.py",
    "scripts/check_external_chat_activation_status_application.py",
    "scripts/check_expanded_external_framework_intake.py",
    "scripts/check_external_framework_candidate_directory.py",
    "scripts/check_external_framework_family_coverage.py",
    "scripts/check_tier1_source_intake_work_packets.py",
    "scripts/check_external_framework_intake_promotion.py",
    "scripts/check_decision_authority_integration_receipt.py",
    "scripts/check_goal5_external_blockers.py",
    "scripts/check_goal5_release_readiness.py",
    "scripts/check_external_frameworks_index.py",
]


def execute(path: str) -> tuple[int, str]:
    target = ROOT / path
    if not target.exists():
        return 127, f"MISSING: {path}"
    completed = subprocess.run([sys.executable, str(target)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return completed.returncode, completed.stdout.rstrip()


def main() -> int:
    results: list[dict[str, object]] = []
    print("GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE CHECK")
    print("=" * 64)
    print(f"\n--- RUN: {SYNC_SCRIPT} ---")
    sync_code, sync_output = execute(SYNC_SCRIPT)
    if sync_output:
        print(sync_output)
    acquisition_path = ROOT / "reports/external-chat-activation-evidence-acquisition.json"
    sync_state = None
    if acquisition_path.exists():
        try:
            sync_state = json.loads(acquisition_path.read_text(encoding="utf-8")).get("state")
        except Exception:
            sync_state = "UNREADABLE"
    results.append({"path": SYNC_SCRIPT, "status": "PASS" if sync_code == 0 else "FAIL", "return_code": sync_code, "output": sync_output, "external_chat_activation_sync": True, "sync_state": sync_state})
    for check in CHECKS:
        print(f"\n--- RUN: {check} ---")
        return_code, output = execute(check)
        if output:
            print(output)
        results.append({"path": check, "status": "PASS" if return_code == 0 else "FAIL", "return_code": return_code, "output": output})
    failures = [item for item in results if item["status"] == "FAIL"]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({
        "schema": "admissibility_wiki.goal5_external_frameworks_report.v1",
        "total_checks": len(results),
        "passed_checks": len(results) - len(failures),
        "failed_checks": len(failures),
        "overall_status": "FAIL" if failures else "PASS",
        "external_chat_activation_sync": {"state": sync_state, "output": sync_output, "authority_effect": "NONE"},
        "results": results,
        "authority_boundary": "This report records structural validation, bounded evidence-transfer outcomes, deployment observations, public-endpoint verification contracts, non-mutating observation candidates, canonical-status-only promotion/application boundaries, and fail-closed source-citation posture. It does not create external-framework certification, equivalence, standing, registry-promotion, dispatch, execution, deployment authority, release, downstream propagation, activation authority, repository mutation, publication, or consequence authority.",
    }, indent=2) + "\n", encoding="utf-8")
    print("\n" + "=" * 64)
    if failures:
        print(f"GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE: FAIL ({len(failures)}/{len(results)} failed)")
        for failure in failures:
            print(f"\nFAIL: {failure['path']}")
            print(failure["output"] or "(no validator output)")
        print(f"Machine-readable report: {REPORT.relative_to(ROOT)}")
        return 1
    print("GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE: PASS")
    print("release_readiness: external_chat_activation_status_promotion_boundary_installed_pending_observed_source_evidence")
    print(f"Machine-readable report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
