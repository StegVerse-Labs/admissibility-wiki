#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "oauth2-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "oauth2" / "oauth2-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    result = case["enforcement_result"]
    transition = case["transition"]
    if result == "ERROR":
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if result == "DENY":
        return "DENY", "OAUTH_ENFORCEMENT_DENIAL"
    if not transition["token_active"] or not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_OR_REVOKED_TOKEN_EVIDENCE"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["audience_matches"] or not transition["target_matches_scope"]:
        return "DENY", "TARGET_OR_AUDIENCE_DIVERGENCE"
    if not transition["scope_covers_action"]:
        return "DENY", "OAUTH_ENFORCEMENT_DENIAL"
    if not transition["execution_context_current"]:
        return "FAIL_CLOSED", "EXECUTION_CONTEXT_DRIFT"
    if not transition["recoverability_satisfied"]:
        return "ESCALATE", "RECOVERABILITY_UNRESOLVED"
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
            "native_output": case["enforcement_result"],
            "translation_mapping": "OAuth grant, token, audience, and scope enter as bounded delegation evidence; StegVerse evaluates current actor, target, policy, evidence, recoverability, and consequence authority independently.",
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed_result,
            "expected_failure_class": case["expected_failure_class"],
            "observed_failure_class": observed_failure,
            "case_match": case_match,
        })
    receipt = {
        "schema": "oauth2_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "oauth2",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evidence_posture": "SIMULATED_TRANSLATION_CONTRACT_RUNTIME_PENDING",
        "results": results,
        "summary": {
            "total_cases": len(results),
            "matching_cases": sum(1 for item in results if item["case_match"]),
            "all_expected_results_matched": all_match,
            "bounded_compatibility_state": "TRANSLATION_CONTRACT_VALIDATED" if all_match else "COMPATIBILITY_MISMATCH",
        },
        "limitations": [
            "No pinned authorization server, resource server, token issuer, or enforcement flow was executed.",
            "This receipt validates only the declared OAuth-to-StegVerse translation and governance decision contract.",
        ],
        "authority_boundary": {
            "token_acceptance_is_universal_authority": False,
            "scope_is_independently_reconstructed_delegation": False,
            "compatibility_receipt_is_execution_authority": False,
            "general_compatibility_claim_allowed": False,
            "certification_claim_allowed": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"OAUTH2 GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
