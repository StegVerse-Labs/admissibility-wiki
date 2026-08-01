#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "full_validation_chain_report.json"
PRESCAN_REPORT = ROOT / "reports" / "canonical-prescan-report.json"
SANDBOX_RUNNER = "scripts/run_sandbox_validation.py"
SANDBOX_REPORT = ROOT / "reports" / "sandbox-first-validation.report.json"
RECONSTRUCTION_GENERATOR = "scripts/generate_external_translation_reconstruction_receipt.py"
RECONSTRUCTION_REPORT = ROOT / "reports" / "external-translation" / "reconstruction-receipt.json"
OBSERVATION_WRITER = ROOT / "scripts" / "write_canonical_workflow_observation_receipt.py"
OBSERVATION_REPORT = ROOT / "reports" / "canonical-workflow-observation-receipt.json"

CHECKS = [
    ("Validate canonical orchestration contract", "scripts/check_canonical_orchestration_contract.py"),
    ("Validate canonical pre-scan contract", "scripts/check_canonical_prescan_contract.py"),
    ("Validate custody-bound activation projection", "scripts/check_activation_projection_orchestration_contract.py"),
    ("Validate revised DecisionAssure pilot package", "docs/external-frameworks/decisionassure-pilot/verifier_rigel_revised.py"),
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
    ("Validate Pages build verification status application", "scripts/check_pages_build_verification_status_application.py"),
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
    ("Validate canonical workflow observation receipt", "scripts/check_canonical_workflow_observation_receipt.py"),
    ("Validate canonical workflow observation automation status", "scripts/check_canonical_workflow_observation_automation_status.py"),
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
    ("Validate KPT source intake queue", "scripts/check_kpt_source_intake_queue.py"),
    ("Validate Goal 5 external framework benchmark chain", "scripts/check_goal5_external_frameworks_all.py"),
    ("Validate ASRO commitment candidate", "scripts/check_asro_commitment_candidate.py"),
    ("Validate governed LLM public pages", "scripts/check_governed_llm_pages.py"),
    ("Validate governed LLM demo docs", "scripts/check_governed_llm_demo_docs.py"),
    ("Validate LLM free-tier trust chain", "scripts/check_llm_free_tier_trust_chain.py"),
    ("Validate TA-14 task observation registry", "scripts/check_ta14_task_observation_registry.py"),
    ("Validate TA-14 observation fixtures", "scripts/check_ta14_observation_fixtures.py"),
    ("Validate iOS workflow mirror status", "scripts/check_ios_workflow_mirror_status.py"),
    ("Validate admissibility automation handoff", "scripts/check_admissibility_automation_handoff.py"),
    ("Validate CI evidence state", "scripts/check_ci_evidence.py"),
    ("Resolve Guardian destination", "scripts/check_guardian_destination.py"),
]


def execute(relative_path: str) -> tuple[int, str]:
    path = ROOT / relative_path
    if not path.exists():
        return 127, f"missing validator: {relative_path}"
    completed = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return completed.returncode, completed.stdout.rstrip()


def read_json_if_present(path: Path) -> object | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "UNREADABLE", "error": str(exc)}


def append_actions_summary(report: dict[str, object]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    results = report.get("results", [])
    lines = [
        "## Complete validation chain",
        "",
        f"**Result:** `{report.get('overall_status')}`  ",
        f"**Checks:** {report.get('passed_checks')}/{report.get('total_checks')} passed; "
        f"{report.get('failed_checks')} failed; {report.get('skipped_checks')} skipped",
        "",
        "| Validator | Status | Exit | Path |",
        "|---|---:|---:|---|",
    ]

    if isinstance(results, list):
        for result in results:
            if not isinstance(result, dict):
                continue
            lines.append(
                f"| {result.get('name')} | `{result.get('status')}` | "
                f"`{result.get('return_code')}` | `{result.get('path')}` |"
            )

        failures = [result for result in results if isinstance(result, dict) and result.get("status") == "FAIL"]
        if failures:
            lines.extend(["", "### Validator failure details", ""])
            for failure in failures:
                output = str(failure.get("output") or "(no validator output)")[-4000:]
                lines.extend([
                    f"#### `{failure.get('path')}`",
                    "",
                    "```text",
                    output,
                    "```",
                    "",
                ])

    with Path(summary_path).open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def emit_actions_annotations(results: list[dict[str, object]]) -> None:
    if not os.environ.get("GITHUB_ACTIONS"):
        return
    for result in results:
        if result.get("status") != "FAIL":
            continue
        path = str(result.get("path") or "unknown-validator")
        output = str(result.get("output") or "no validator output").replace("\r", " ").replace("\n", "%0A")[-2000:]
        print(f"::error title=Validation failure ({path})::{output}")


def main() -> int:
    results: list[dict[str, object]] = []
    failures: list[str] = []
    print("FULL VALIDATION CHAIN SCAN")
    print("=" * 72)

    print("\n--- Bind canonical pre-scan evidence ---")
    prescan_payload = read_json_if_present(PRESCAN_REPORT)
    prescan_status = (
        "PASS"
        if isinstance(prescan_payload, dict)
        and prescan_payload.get("schema") == "admissibility_wiki.canonical_prescan_report.v1"
        and prescan_payload.get("overall_status") == "PASS"
        else "FAIL"
    )
    prescan_output = (
        f"{prescan_payload.get('passed_commands')}/{prescan_payload.get('total_commands')} commands passed; "
        f"{prescan_payload.get('failed_commands')} failed"
        if isinstance(prescan_payload, dict)
        else "canonical pre-scan report missing or unreadable"
    )
    results.append({
        "name": "Bind canonical pre-scan evidence",
        "path": str(PRESCAN_REPORT.relative_to(ROOT)),
        "status": prescan_status,
        "return_code": 0 if prescan_status == "PASS" else 1,
        "output": prescan_output,
    })
    print(prescan_output)
    if prescan_status != "PASS":
        failures.append(str(PRESCAN_REPORT.relative_to(ROOT)))

    print("\n--- Execute ST-017 isolated sandbox ---")
    sandbox_code, sandbox_output = execute(SANDBOX_RUNNER)
    if sandbox_output:
        print(sandbox_output)
    sandbox_payload = read_json_if_present(SANDBOX_REPORT)
    sandbox_status = "PASS" if sandbox_code == 0 and isinstance(sandbox_payload, dict) and sandbox_payload.get("sandbox_status") == "PASS" else "FAIL"
    results.append({"name": "Execute ST-017 isolated sandbox", "path": SANDBOX_RUNNER, "status": sandbox_status, "return_code": sandbox_code, "output": sandbox_output})
    if sandbox_status != "PASS":
        failures.append(SANDBOX_RUNNER)

    reconstruction_payload: object | None = None
    if sandbox_status == "PASS":
        print("\n--- Generate external translation reconstruction receipt ---")
        generation_code, generation_output = execute(RECONSTRUCTION_GENERATOR)
        if generation_output:
            print(generation_output)
        reconstruction_payload = read_json_if_present(RECONSTRUCTION_REPORT)
        generation_status = "PASS" if generation_code == 0 and isinstance(reconstruction_payload, dict) and reconstruction_payload.get("overall_status") == "PASS" else "FAIL"
        results.append({"name": "Generate external translation reconstruction receipt", "path": RECONSTRUCTION_GENERATOR, "status": generation_status, "return_code": generation_code, "output": generation_output})
        if generation_status != "PASS":
            failures.append(RECONSTRUCTION_GENERATOR)
    else:
        print("\n--- Reconstruction generation skipped: sandbox failed ---")
        results.append({
            "name": "Generate external translation reconstruction receipt",
            "path": RECONSTRUCTION_GENERATOR,
            "status": "SKIPPED_DEPENDENCY_FAILED",
            "return_code": None,
            "output": "ST-017 sandbox failed; reconstruction generation was not executed.",
        })

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
        "skipped_checks": sum(1 for result in results if str(result["status"]).startswith("SKIPPED_")),
        "overall_status": "FAIL" if failures else "PASS",
        "canonical_prescan": prescan_payload,
        "st017_sandbox": sandbox_payload,
        "external_translation_reconstruction": reconstruction_payload,
        "results": results,
        "authority_boundary": "This report records canonical pre-scan evidence, isolated sandbox, generated reconstruction, and validator outcomes only. Diagnostic continuation after failure does not weaken fail-closed enforcement. A passing scan does not grant runtime execution, artifact promotion, canonical status mutation, merge, deployment authority, public verification, release, certification, downstream propagation, standing, admissibility, or ecosystem authority.",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    observation_payload: object | None = None
    if OBSERVATION_WRITER.exists():
        observation_env = os.environ.copy()
        observation_env["CANONICAL_JOB_STATUS"] = "failure" if failures else "success"
        observation_run = subprocess.run([sys.executable, str(OBSERVATION_WRITER)], cwd=ROOT, env=observation_env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        if observation_run.stdout:
            print(observation_run.stdout.rstrip())
        observation_payload = read_json_if_present(OBSERVATION_REPORT)
        if observation_run.returncode != 0 or not isinstance(observation_payload, dict):
            failures.append(str(OBSERVATION_WRITER.relative_to(ROOT)))
        report["canonical_workflow_observation"] = observation_payload
        report["overall_status"] = "FAIL" if failures else "PASS"
        report["failed_checks"] = sum(1 for result in results if result["status"] == "FAIL") + (1 if observation_run.returncode != 0 else 0)
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    append_actions_summary(report)
    emit_actions_annotations(results)

    print("\n" + "=" * 72)
    print(
        f"FULL VALIDATION CHAIN: {report['overall_status']} "
        f"({report['passed_checks']}/{report['total_checks']} passed; "
        f"{report['failed_checks']} failed; {report['skipped_checks']} skipped)"
    )
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