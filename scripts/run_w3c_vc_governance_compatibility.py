#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "w3c-vc-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "w3c-vc" / "w3c-vc-stegverse-governance-compatibility-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(case: dict) -> tuple[str, str | None]:
    result = case["verification_result"]
    transition = case["transition"]
    if result == "error":
        return "FAIL_CLOSED", "VERIFIER_OR_RESOLVER_ERROR"
    if result != "verified":
        return "DENY", "CREDENTIAL_VERIFICATION_FAILED"
    if not transition["actor_identity_correlated"]:
        return "FAIL_CLOSED", "ACTOR_SUBJECT_CORRELATION_UNRESOLVED"
    if not transition["issuer_trusted_for_claim"]:
        return "FAIL_CLOSED", "ISSUER_STANDING_UNRESOLVED"
    if not transition["credential_status_current"] or not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_OR_REVOKED_CREDENTIAL_STATUS"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["claim_matches_scope"]:
        return "DENY", "CLAIM_SCOPE_DIVERGENCE"
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
        case_match = (
            observed_result == case["expected_stegverse_result"]
            and observed_failure == case["expected_failure_class"]
        )
        all_match = all_match and case_match
        results.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "native_verification_result": case["verification_result"],
            "translation_mapping": "Credential verification enters as bounded claim evidence; issuer standing, status, actor correlation, delegation, scope, freshness, recoverability, and execution context remain independently governed.",
            "stegverse_transition_input": case["transition"],
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed_result,
            "expected_failure_class": case["expected_failure_class"],
            "observed_failure_class": observed_failure,
            "case_match": case_match,
        })

    receipt = {
        "schema": "w3c_vc_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "w3c-verifiable-credentials",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "fixture": {"path": str(FIXTURE.relative_to(ROOT)), "sha256": sha256(FIXTURE)},
        "runtime_evidence_state": "SIMULATED_NATIVE_RESULTS_NO_PINNED_VERIFIER_EXECUTION",
        "results": results,
        "summary": {
            "total_cases": len(results),
            "matching_cases": sum(1 for item in results if item["case_match"]),
            "all_expected_results_matched": all_match,
            "translation_contract_state": "VALIDATED" if all_match else "MISMATCH",
            "bounded_compatibility_state": "RUNTIME_EVIDENCE_PENDING",
        },
        "limitations": [
            "No pinned VC verifier, proof suite, resolver, credential, presentation, or status method was executed.",
            "Verification results are fixture inputs used only to validate the StegVerse governance translation boundary.",
            "The evaluator is not a production SPE deployment.",
        ],
        "authority_boundary": {
            "verified_credential_is_execution_authority": False,
            "issuer_signature_proves_claim_truth": False,
            "translation_validation_is_general_compatibility": False,
            "receipt_creates_standing": False,
            "certification_claim_allowed": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"W3C VC GOVERNANCE COMPATIBILITY: {'TRANSLATION_VALIDATED_RUNTIME_PENDING' if all_match else 'MISMATCH'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
