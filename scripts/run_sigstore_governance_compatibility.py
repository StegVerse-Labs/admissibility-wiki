#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "sigstore-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "sigstore" / "sigstore-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    result = case["verification_result"]
    transition = case["transition"]
    if result == "ERROR":
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if result == "FAIL" or not transition["signature_valid"]:
        return "DENY", "SIGNATURE_VERIFICATION_DENIAL"
    if not transition["artifact_digest_matches"]:
        return "FAIL_CLOSED", "ARTIFACT_DIGEST_MISMATCH"
    if not transition["certificate_identity_verified"] or not transition["transparency_inclusion_verified"]:
        return "FAIL_CLOSED", "IDENTITY_OR_TRANSPARENCY_UNVERIFIED"
    if not transition["trust_root_current"] or not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_TRUST_OR_EVIDENCE"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["target_action_in_scope"]:
        return "DENY", "TARGET_ACTION_SCOPE_DIVERGENCE"
    if not transition["recoverability_satisfied"]:
        return "ESCALATE", "RECOVERABILITY_UNRESOLVED"
    if not transition["execution_context_current"]:
        return "FAIL_CLOSED", "EXECUTION_CONTEXT_DRIFT"
    return "ALLOW", None


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    all_match = True
    for case in fixture["cases"]:
        observed_result, observed_failure = evaluate(case)
        case_match = observed_result == case["expected_stegverse_result"] and observed_failure == case["expected_failure_class"]
        all_match = all_match and case_match
        results.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "native_output": case["verification_result"],
            "translation_mapping": "Sigstore verification enters as artifact-origin, identity, integrity, and transparency evidence; action authority is evaluated independently.",
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed_result,
            "expected_failure_class": case["expected_failure_class"],
            "observed_failure_class": observed_failure,
            "case_match": case_match,
        })

    receipt = {
        "schema": "sigstore_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "sigstore",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evidence_posture": "SIMULATED_TRANSLATION_CONTRACT_RUNTIME_PENDING",
        "results": results,
        "summary": {
            "total_cases": len(results),
            "matching_cases": sum(1 for item in results if item["case_match"]),
            "all_expected_results_matched": all_match,
            "bounded_compatibility_state": "TRANSLATION_CONTRACT_VALIDATED" if all_match else "COMPATIBILITY_MISMATCH"
        },
        "limitations": [
            "No pinned Sigstore client or trust configuration was executed.",
            "No signed artifact, certificate, or transparency proof was verified.",
            "This receipt validates only the declared translation and StegVerse governance decision contract."
        ],
        "authority_boundary": {
            "valid_signature_is_action_authority": False,
            "transparency_inclusion_is_admissibility": False,
            "compatibility_receipt_is_execution_authority": False,
            "general_compatibility_claim_allowed": False,
            "certification_claim_allowed": False
        }
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"SIGSTORE GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
