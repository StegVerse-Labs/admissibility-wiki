#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "mindforge-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "mindforge" / "mindforge-stegverse-governance-compatibility-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case["native_result"]
    transition = case["transition"]
    if native == "packet_parse_error":
        return "FAIL_CLOSED", "REVIEW_PACKET_PARSE_ERROR"
    if native == "review_packet_rejected":
        return "DENY", "HISTORICAL_REVIEW_REJECTED"
    if not transition["actor_identity_verified"]:
        return "FAIL_CLOSED", "IDENTITY_UNVERIFIED"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_REVIEW_EVIDENCE"
    if not transition["scope_matches_review"]:
        return "DENY", "REVIEW_SCOPE_DIVERGENCE"
    if not transition["recoverability_satisfied"]:
        return "FAIL_CLOSED", "RECOVERABILITY_UNRESOLVED"
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
            "simulated_native_result": case["native_result"],
            "observed_stegverse_result": observed_result,
            "observed_failure_class": observed_failure,
            "case_match": case_match,
        })

    receipt = {
        "schema": "mindforge_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "mindforge",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "simulation_only": True,
        "native_runtime_execution_observed": False,
        "fixture": {"path": str(FIXTURE.relative_to(ROOT)), "sha256": sha256(FIXTURE)},
        "results": results,
        "summary": {
            "total_cases": len(results),
            "matching_cases": sum(1 for item in results if item["case_match"]),
            "all_expected_results_matched": all_match,
            "bounded_compatibility_state": "CONTRACT_SIMULATION_MATCHED" if all_match else "CONTRACT_SIMULATION_MISMATCH",
        },
        "authority_boundary": {
            "historical_review_is_current_authority": False,
            "review_packet_is_execution_authority": False,
            "commitment_candidate_is_authorization": False,
            "simulation_is_runtime_observation": False,
            "general_compatibility_claim_allowed": False,
        },
        "limitations": [
            "No MindForge implementation, review engine, packet schema, or verifier was executed.",
            "The evaluator tests only the authored translation contract.",
            "Current standing must be reconstructed independently at the commit boundary.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"MINDFORGE GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
