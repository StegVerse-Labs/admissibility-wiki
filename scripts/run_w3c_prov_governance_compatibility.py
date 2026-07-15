#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/w3c-prov-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports/external-frameworks/w3c-prov/w3c-prov-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    result = case["validation_result"]
    transition = case["transition"]
    if result == "ERROR":
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if result == "FAIL":
        return "DENY", "PROVENANCE_VALIDATION_DENIAL"
    if not transition["source_evidence_present"] or not transition["custody_valid"]:
        return "FAIL_CLOSED", "PROVENANCE_SOURCE_OR_CUSTODY_GAP"
    if not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_PROVENANCE_EVIDENCE"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["requested_action_in_scope"]:
        return "DENY", "REPRESENTED_RELATION_SCOPE_DIVERGENCE"
    if not transition["recoverability_satisfied"]:
        return "ESCALATE", "RECOVERABILITY_UNRESOLVED"
    return "ALLOW", None


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    all_match = True
    for case in fixture["cases"]:
        observed_result, observed_failure = evaluate(case)
        matched = observed_result == case["expected_stegverse_result"] and observed_failure == case["expected_failure_class"]
        all_match = all_match and matched
        results.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "native_output": case["validation_result"],
            "translation_mapping": "W3C PROV relations enter as represented provenance evidence; truth, legitimacy, current delegation, scope, and consequence authority remain independently evaluated.",
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed_result,
            "expected_failure_class": case["expected_failure_class"],
            "observed_failure_class": observed_failure,
            "case_match": matched,
        })
    receipt = {
        "schema": "w3c_prov_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "w3c-prov",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evidence_posture": "SIMULATED_TRANSLATION_CONTRACT_RUNTIME_PENDING",
        "results": results,
        "summary": {"total_cases": len(results), "matching_cases": sum(1 for item in results if item["case_match"]), "all_expected_results_matched": all_match, "bounded_compatibility_state": "TRANSLATION_CONTRACT_VALIDATED" if all_match else "COMPATIBILITY_MISMATCH"},
        "limitations": ["No pinned W3C PROV implementation was executed.", "No source-to-PROV generation, validation, or query transcript was captured.", "This receipt validates only the declared translation and StegVerse governance decision contract."],
        "authority_boundary": {"provenance_representation_is_truth": False, "represented_delegation_is_current_authority": False, "compatibility_receipt_is_execution_authority": False, "general_compatibility_claim_allowed": False, "certification_claim_allowed": False}
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"W3C PROV GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
