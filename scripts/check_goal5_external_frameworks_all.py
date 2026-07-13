#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "goal5_external_frameworks_report.json"

CHECKS = [
    "scripts/check_runtime_governance_benchmark_suite.py",
    "scripts/check_morrison_runtime_benchmark_fixtures.py",
    "scripts/check_morrison_validation_table_visibility.py",
    "scripts/check_external_framework_reports.py",
    "scripts/check_external_framework_benchmark_mappings.py",
    "scripts/check_external_framework_benchmark_fixtures.py",
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
    "scripts/check_external_chat_review_packets.py",
    "scripts/check_external_chat_activation_evidence.py",
    "scripts/check_external_chat_activation_importer.py",
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


def main() -> int:
    results: list[dict[str, object]] = []
    print("GOAL 5 EXTERNAL FRAMEWORKS AGGREGATE CHECK")
    print("=" * 64)
    for check in CHECKS:
        path = ROOT / check
        print(f"\n--- RUN: {check} ---")
        if not path.exists():
            output = f"MISSING: {check}"
            return_code = 127
        else:
            completed = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            return_code = completed.returncode
            output = completed.stdout.rstrip()
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
        "results": results,
        "authority_boundary": "This report records structural validation outcomes only and does not create external-framework certification, equivalence, standing, registry-promotion, dispatch, execution, deployment, public-verification, activation, mutation, publication, or consequence authority.",
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
    print("release_readiness: pages_build_candidate_and_external_chat_activation_evidence_import_contracts_installed_pending_observed_canonical_evidence")
    print(f"Machine-readable report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
