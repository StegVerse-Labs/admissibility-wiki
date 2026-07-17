#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/nist-ai-rmf-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/nist-ai-rmf/nist-ai-rmf-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case.get("native_result")
    transition = case.get("transition", {})
    if native == "mapping_error":
        return "FAIL_CLOSED", "RMF_MAPPING_ERROR"
    if not transition.get("official_source_confirmed") or not transition.get("profile_snapshot_attached") or not transition.get("evidence_fresh"):
        return "FAIL_CLOSED", "PROFILE_EVIDENCE_MISSING_OR_STALE"
    if native == "risk_treatment_incomplete":
        return "DENY", "RISK_TREATMENT_INCOMPLETE"
    if not transition.get("delegation_current"):
        return "DENY", "AUTHORITY_DRIFT"
    if not transition.get("scope_matches"):
        return "DENY", "RISK_SCOPE_DIVERGENCE"
    required = ("actor_identity_verified", "policy_reference_current", "recoverability_satisfied")
    if not all(transition.get(key) for key in required):
        return "FAIL_CLOSED", "CURRENT_STANDING_INCOMPLETE"
    return "ALLOW", None


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in fixture.get("cases", []):
        actual, failure = evaluate(case)
        results.append({
            "case_id": case.get("case_id"),
            "family": case.get("family"),
            "native_result": case.get("native_result"),
            "expected_stegverse_result": case.get("expected_stegverse_result"),
            "actual_stegverse_result": actual,
            "expected_failure_class": case.get("expected_failure_class"),
            "actual_failure_class": failure,
            "matched": actual == case.get("expected_stegverse_result") and failure == case.get("expected_failure_class"),
        })
    matched = sum(1 for result in results if result["matched"])
    receipt = {
        "schema": "external_framework_governance_compatibility_receipt.v1",
        "framework_id": "nist-ai-rmf",
        "evaluation_mode": "DETERMINISTIC_SIMULATION_ONLY",
        "official_source_confirmed": True,
        "native_execution_observed": False,
        "risk_profile_mapping_observed": False,
        "stegverse_governance_compatibility_observed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_cases": len(results),
        "matching_cases": matched,
        "result": "CONTRACT_SIMULATION_PASS" if matched == len(results) else "CONTRACT_SIMULATION_FAIL",
        "translation_boundary": "NIST AI RMF guidance, profiles, lifecycle review, and trustworthiness evidence contribute risk-management context only; they do not establish current standing, delegation, commit-time admissibility, or execution authority.",
        "manual_tasks_required": [],
        "user_action_required": False,
        "authority_granted": False,
        "execution_authority_granted": False,
        "release_authority_granted": False,
        "downstream_mutation_authority_granted": False,
        "cases": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"NIST AI RMF GOVERNANCE COMPATIBILITY: {'PASS' if matched == len(results) else 'FAIL'}")
    print(f"cases={len(results)} matched={matched}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if matched != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
