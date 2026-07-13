#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "full_validation_chain_report.json"

CHECKS = [
    ("Validate single workflow policy", "scripts/check_workflow_sprawl.py"),
    ("Validate chain continuation", "scripts/check_chain_status_continuation.py"),
    ("Validate continuation bundle", "scripts/check_continuation_bundle.py"),
    ("Validate chain snapshot", "scripts/check_chain_snapshot.py"),
    ("Validate chain snapshot receipt", "scripts/check_chain_snapshot_receipt.py"),
    ("Validate chain auto state", "scripts/check_chain_auto.py"),
    ("Validate blocked destination record", "scripts/check_blocked_destination_record.py"),
    ("Validate goal state", "scripts/check_goal_state.py"),
    ("Validate workflow manifest", "scripts/check_workflow_manifest.py"),
    ("Validate Pages build receipt automation", "scripts/check_pages_build_receipt_automation.py"),
    ("Validate Pages build verification candidate", "scripts/check_pages_build_verification_candidate.py"),
    ("Validate Pages artifact binding receipt", "scripts/check_pages_artifact_binding_receipt.py"),
    ("Validate Pages verification status application", "scripts/check_pages_build_verification_status_application.py"),
    ("Validate Pages deployment observation receipt", "scripts/check_pages_deployment_observation_receipt.py"),
    ("Validate Pages public endpoint verification receipt", "scripts/check_pages_public_endpoint_verification_receipt.py"),
    ("Validate inference-window governance documentation mesh", "scripts/check_inference_window_governance_docs.py"),
    ("Validate external frameworks index", "scripts/check_external_frameworks_index.py"),
    ("Validate external framework manifests", "scripts/check_external_framework_manifests.py"),
    ("Validate external framework terminology", "scripts/check_external_framework_terminology.py"),
    ("Validate external framework reports", "scripts/check_external_framework_reports.py"),
    ("Validate report coverage", "scripts/check_external_framework_report_coverage.py"),
    ("Validate external framework report generation", "scripts/check_external_framework_report_generation.py"),
    ("Validate external framework results page", "scripts/check_external_framework_results_page.py"),
    ("Validate external framework page metadata", "scripts/check_external_framework_page_metadata.py"),
    ("Validate external framework page mapping", "scripts/check_external_framework_page_mapping.py"),
    ("Validate external framework page status", "scripts/check_external_framework_page_status.py"),
    ("Validate external framework expansion policy", "scripts/check_external_framework_expansion_policy.py"),
    ("Validate external framework evidence provenance", "scripts/check_external_framework_evidence_provenance.py"),
    ("Validate Goal 5 external framework benchmark chain", "scripts/check_goal5_external_frameworks_all.py"),
    ("Validate ASRO commitment candidate", "scripts/check_asro_commitment_candidate.py"),
    ("Validate governed LLM public pages", "scripts/check_governed_llm_pages.py"),
    ("Validate governed LLM demo docs", "scripts/check_governed_llm_demo_docs.py"),
    ("Validate LLM free-tier trust chain", "scripts/check_llm_free_tier_trust_chain.py"),
    ("Validate iOS workflow mirror status", "scripts/check_ios_workflow_mirror_status.py"),
    ("Validate admissibility automation handoff", "scripts/check_admissibility_automation_handoff.py"),
    ("Validate CI evidence state", "scripts/check_ci_evidence.py"),
    ("Resolve Guardian destination", "scripts/check_guardian_destination.py"),
]


def main() -> int:
    results: list[dict[str, object]] = []
    failures: list[str] = []
    print("FULL VALIDATION CHAIN SCAN")
    print("=" * 72)
    for name, relative_path in CHECKS:
        path = ROOT / relative_path
        print(f"\n--- {name} ---")
        if not path.exists():
            output = f"missing validator: {relative_path}"
            print(output)
            return_code = 127
        else:
            completed = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            return_code = completed.returncode
            output = completed.stdout.rstrip()
            if output:
                print(output)
        status = "PASS" if return_code == 0 else "FAIL"
        results.append({"name": name, "path": relative_path, "status": status, "return_code": return_code, "output": output})
        if return_code != 0:
            failures.append(relative_path)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "admissibility_wiki.full_validation_chain_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_checks": len(results),
        "passed_checks": sum(1 for result in results if result["status"] == "PASS"),
        "failed_checks": sum(1 for result in results if result["status"] == "FAIL"),
        "overall_status": "FAIL" if failures else "PASS",
        "results": results,
        "authority_boundary": "This report records validator outcomes only. A passing scan does not grant execution, merge, deployment authority, public verification, release, certification, downstream propagation, or ecosystem authority.",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("\n" + "=" * 72)
    print(f"FULL VALIDATION CHAIN: {report['overall_status']} ({report['passed_checks']}/{report['total_checks']} passed)")
    if failures:
        print("FAILING VALIDATORS:")
        for failure in failures:
            print(f"- {failure}")
        print(f"Machine-readable report: {REPORT.relative_to(ROOT)}")
        return 1
    print(f"Machine-readable report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
