#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "guardrails-ai-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "guardrails-ai" / "guardrails-ai-stegverse-governance-compatibility-receipt.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case["native_guard_result"]
    transition = case["transition"]
    if native == "ERROR":
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if native == "BLOCK":
        return "DENY", "GUARDRAIL_BLOCK"
    if native != "PASS":
        return "FAIL_CLOSED", "UNDEFINED_FRAMEWORK_RESULT"
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
    fixture = load(FIXTURE)
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
            "native_guard_result": case["native_guard_result"],
            "translation_mapping": "Guardrails AI output enters as bounded content-safety evidence; authority, delegation, scope, freshness, recoverability, and execution context remain independent.",
            "expected_stegverse_result": case["expected_stegverse_result"],
            "observed_stegverse_result": observed_result,
            "expected_failure_class": case["expected_failure_class"],
            "observed_failure_class": observed_failure,
            "case_match": case_match,
            "reason": case["reason"],
        })

    receipt = {
        "schema": "guardrails_ai_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "guardrails-ai",
        "execution_class": "SIMULATION_ONLY_RUNTIME_EVIDENCE_NOT_ATTACHED",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "fixture": {"path": str(FIXTURE.relative_to(ROOT)), "sha256": sha256(FIXTURE)},
        "results": results,
        "summary": {
            "total_cases": len(results),
            "matching_cases": sum(1 for result in results if result["case_match"]),
            "all_expected_results_matched": all_match,
            "bounded_compatibility_state": "CONTRACT_SIMULATION_MATCHED" if all_match else "CONTRACT_SIMULATION_MISMATCH",
            "governance_compatibility_observed": False,
        },
        "limitations": [
            "No pinned Guardrails AI package, validator suite, model, prompt, threshold, or runtime trace is attached.",
            "The evaluator validates the translation contract only and is not native framework execution.",
            "No independent implementation, organization, or authority has reproduced the result.",
        ],
        "authority_boundary": fixture["authority_boundary"],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"GUARDRAILS AI GOVERNANCE COMPATIBILITY: {'PASS' if all_match else 'FAIL'} -> {OUTPUT.relative_to(ROOT)}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
