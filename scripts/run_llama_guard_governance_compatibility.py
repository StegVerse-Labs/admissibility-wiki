#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "llama-guard-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "llama-guard" / "llama-guard-stegverse-governance-compatibility-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case["native_result"]
    transition = case["transition"]
    if native == "error":
        return "FAIL_CLOSED", "CLASSIFIER_RUNTIME_ERROR"
    if native == "unsafe":
        return "DENY", "SAFETY_CLASSIFICATION_NEGATIVE"
    if not transition["actor_identity_verified"]:
        return "FAIL_CLOSED", "IDENTITY_UNVERIFIED"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_EVIDENCE"
    if not transition["target_matches_scope"]:
        return "DENY", "SCOPE_DIVERGENCE"
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
            "simulated_native_result": case["native_result"],
            "observed_stegverse_result": observed_result,
            "observed_failure_class": observed_failure,
            "case_match": case_match,
        })

    receipt = {
        "schema": "llama_guard_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "llama-guard",
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
            "classifier_safe_is_stegverse_allow": False,
            "classifier_unsafe_is_universal_policy_denial": False,
            "simulation_is_runtime_observation": False,
            "receipt_is_execution_authority": False,
            "general_compatibility_claim_allowed": False,
        },
        "limitations": [
            "No Llama Guard model package, weights, tokenizer, taxonomy, prompt, or inference runtime was executed.",
            "The evaluator tests only the authored translation contract.",
            "A classifier result remains bounded safety evidence and does not create standing or execution authority.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"LLAMA GUARD GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
