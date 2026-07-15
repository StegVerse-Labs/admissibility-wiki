#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "openid-connect-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "openid-connect" / "openid-connect-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    result = case["validation_result"]
    transition = case["transition"]
    if result == "ERROR":
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if result == "FAIL":
        return "DENY", "IDENTITY_ASSERTION_DENIAL"
    if not all(transition[key] for key in ("issuer_accepted", "audience_matches", "nonce_valid", "signature_valid")):
        return "FAIL_CLOSED", "IDENTITY_ASSERTION_INVALID"
    if not transition["token_fresh"]:
        return "FAIL_CLOSED", "STALE_IDENTITY_EVIDENCE"
    if not transition["actor_correlation_valid"]:
        return "FAIL_CLOSED", "ACTOR_CORRELATION_UNRESOLVED"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["requested_action_in_scope"]:
        return "DENY", "ACTION_SCOPE_DIVERGENCE"
    if not transition["execution_context_current"]:
        return "FAIL_CLOSED", "EXECUTION_CONTEXT_DRIFT"
    return "ALLOW", None


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    all_match = True
    for case in fixture["cases"]:
        observed_result, observed_failure = evaluate(case)
        match = observed_result == case["expected_stegverse_result"] and observed_failure == case["expected_failure_class"]
        all_match = all_match and match
        results.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "native_output": case["validation_result"],
            "translation_mapping": "OpenID Connect validation contributes provider-asserted identity evidence; authentication does not create delegation, action authority, or admissibility.",
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed_result,
            "expected_failure_class": case["expected_failure_class"],
            "observed_failure_class": observed_failure,
            "case_match": match,
        })
    receipt = {
        "schema": "openid_connect_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "openid-connect",
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
            "No pinned OpenID Provider or relying party was executed.",
            "No discovery document, key set, ID Token, or validation transcript was captured.",
            "This receipt validates only the declared translation and StegVerse governance decision contract.",
        ],
        "authority_boundary": {
            "authentication_is_action_authority": False,
            "identity_assertion_is_current_delegation": False,
            "compatibility_receipt_is_execution_authority": False,
            "general_compatibility_claim_allowed": False,
            "certification_claim_allowed": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"OPENID CONNECT GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
