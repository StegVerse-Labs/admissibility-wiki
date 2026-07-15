#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "spiffe-spire-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "spiffe-spire" / "spiffe-spire-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    identity = case["identity_result"]
    transition = case["transition"]
    if identity == "error":
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if identity != "verified" or not transition["attestation_valid"]:
        return "DENY", "IDENTITY_VERIFICATION_FAILURE"
    if not transition["svid_current"] or not transition["trust_bundle_current"] or not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_OR_MISSING_IDENTITY_EVIDENCE"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_REFERENCE_STALE"
    if not transition["target_matches_scope"]:
        return "DENY", "IDENTITY_AUTHORITY_SCOPE_DIVERGENCE"
    if not transition["recoverability_satisfied"] or not transition["execution_context_current"]:
        return "FAIL_CLOSED", "COMMIT_TIME_CONTEXT_FAILURE"
    return "ALLOW", None


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    all_match = True
    for case in fixture["cases"]:
        observed, failure = evaluate(case)
        matches = observed == case["expected_stegverse_result"]
        all_match = all_match and matches
        results.append({
            "framework_id": "spiffe-spire",
            "case_id": case["case_id"],
            "family": case["family"],
            "native_input": {"identity_result": case["identity_result"]},
            "native_output": case["identity_result"],
            "translation_mapping": "verified workload identity -> actor identity evidence only",
            "stegverse_transition_input": case["transition"],
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed,
            "failure_class": failure,
            "matches_expected": matches,
        })
    receipt = {
        "schema": "spiffe_spire_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "spiffe-spire",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evidence_posture": "SIMULATED_IDENTITY_TRANSLATION_RUNTIME_NOT_CAPTURED",
        "case_count": len(results),
        "all_expected_results_matched": all_match,
        "results": results,
        "runtime_environment": "deterministic fixture evaluator",
        "same_environment_replay": False,
        "fresh_runner_replay": False,
        "limitations": [
            "No pinned SPIRE runtime, trust domain, registration entry, attestation payload, SVID, or bundle was executed.",
            "Identity results are predeclared fixture inputs, not observed SPIRE outputs.",
            "A matching result validates the StegVerse translation contract only.",
        ],
        "authority_boundary": fixture["authority_boundary"],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"SPIFFE SPIRE GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} cases={len(results)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
