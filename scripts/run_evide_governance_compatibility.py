#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "evide-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "evide" / "evide-stegverse-governance-compatibility-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case["native_result"]
    transition = case["transition"]
    if native == "registry_error":
        return "FAIL_CLOSED", "EVIDENTIARY_REGISTRY_ERROR"
    if native == "deposit_invalid":
        return "DENY", "EVIDENTIARY_DEPOSIT_INVALID"
    if not transition["actor_identity_verified"]:
        return "FAIL_CLOSED", "IDENTITY_UNVERIFIED"
    if not transition["delegation_current"]:
        return "DENY", "AUTHORITY_DRIFT"
    if not transition["policy_reference_current"]:
        return "FAIL_CLOSED", "POLICY_DRIFT"
    if not transition["evidence_fresh"]:
        return "FAIL_CLOSED", "STALE_EVIDENTIARY_RECORD"
    if not transition["receipt_chain_complete"]:
        return "DENY", "RECEIPT_CHAIN_DIVERGENCE"
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
            "simulated_native_result": case["native_result"],
            "observed_stegverse_result": observed_result,
            "observed_failure_class": observed_failure,
            "case_match": case_match,
        })

    receipt = {
        "schema": "evide_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "evide",
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
            "reconstructability_is_commit_time_authority": False,
            "post_event_evidence_is_execution_permission": False,
            "simulation_is_runtime_observation": False,
            "receipt_is_execution_authority": False,
            "general_compatibility_claim_allowed": False,
        },
        "limitations": [
            "No EVIDE registry, API, schema package, deposited record, or independent implementation was executed.",
            "The evaluator tests only the authored translation contract.",
            "Post-event reconstructability cannot retroactively create commit-time standing or execution authority.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"EVIDE GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
