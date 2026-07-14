#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "full_validation_chain_report.json"
SANDBOX_RUNNER = "scripts/run_sandbox_validation.py"
SANDBOX_REPORT = ROOT / "reports" / "sandbox-first-validation.report.json"
RECONSTRUCTION_GENERATOR = "scripts/generate_external_translation_reconstruction_receipt.py"
RECONSTRUCTION_REPORT = ROOT / "reports" / "external-translation" / "reconstruction-receipt.json"

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
    ("Validate disciplinary translation records", "scripts/check_translation_records.py"),
    ("Validate mathematics crosswalk", "scripts/check_mathematics_crosswalk.py"),
    ("Validate external physics translation records", "scripts/check_external_physics_translation_records.py"),
    ("Validate external bibliographic intake", "scripts/check_external_bibliographic_intake.py"),
    ("Validate external record promotion governance", "scripts/check_external_record_promotion_governance.py"),
    ("Validate source locator and specialist routing", "scripts/check_source_locator_and_specialist_routing.py"),
    ("Validate review receipts and supersession", "scripts/check_review_receipts_and_supersession.py"),
    ("Validate external translation reconstruction receipt", "scripts/check_external_translation_reconstruction_receipt.py"),
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
    ("Validate KPT external framework intake", "scripts/check_kpt_external_framework_intake.py"),
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


def execute(relative_path: str) -> tuple[int, str]:
    path = ROOT / relative_path
    if not path.exists():
        return 127, f"missing validator: {relative_path}"
    completed = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout.rstrip()


def read_json_if_present(path: Path) -> object | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "UNREADABLE", "error": str(exc)}


def main() -> int:
    results: list[dict[str, object]] = []
    failures: list[str] = []
    print("FULL VALIDATION CHAIN SCAN")
    print("=" * 72)

    print("\n--- Execute ST-017 isolated sandbox ---")
    sandbox_code, sandbox_output = execute(SANDBOX_RUNNER)
    if sandbox_output:
        print(sandbox_output)
    sandbox_payload = read_json_if_present(SANDBOX_REPORT)
    sandbox_status = "PASS" if sandbox_code == 0 and isinstance(sandbox_payload, dict) and sandbox_payload.get("sandbox_status") == "PASS" else "FAIL"
    results.append({
        "name": "Execute ST-017 isolated sandbox",
        "path": SANDBOX_RUNNER,
        "status": sandbox_status,
        "return_code": sandbox_code,
        "output": sandbox_output,
    })
    if sandbox_status != "PASS":
        failures.append(SANDBOX_RUNNER)

    reconstruction_payload: object | None = None
    if sandbox_status == "PASS":
        print("\n--- Generate external translation reconstruction receipt ---")
        generation_code, generation_output = execute(RECONSTRUCTION_GENERATOR)
        if generation_output:
            print(generation_output)
        reconstruction_payload = read_json_if_present(RECONSTRUCTION_REPORT)
        generation_status = (
            "PASS"
            if generation_code == 0
            and isinstance(reconstruction_payload, dict)
            and reconstruction_payload.get("overall_status") == "PASS"
            else "FAIL"
        )
        results.append({
            "name": "Generate external translation reconstruction receipt",
            "path": RECONSTRUCTION_GENERATOR,
            "status": generation_status,
            "return_code": generation_code,
            "output": generation_output,
        })
        if generation_status != "PASS":
            failures.append(RECONSTRUCTION_GENERATOR)

    if sandbox_status == "PASS" and not failures:
        for name, relative_path in CHECKS:
            print(f"\n--- {name} ---")
            return_code, output = execute(relative_path)
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
        "st017_sandbox": sandbox_payload,
        "external_translation_reconstruction": reconstruction_payload,
        "results": results,
        "authority_boundary": "This report records isolated sandbox, generated reconstruction, and validator outcomes only. A passing scan does not grant runtime execution, artifact promotion, canonical status mutation, merge, deployment authority, public verification, release, certification, downstream propagation, standing, admissibility, or ecosystem authority.",
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
