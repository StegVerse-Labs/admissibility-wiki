#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/eu-ai-act-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/eu-ai-act/eu-ai-act-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case.get("native_result")
    transition = case.get("transition", {})
    if native == "legal_mapping_error":
        return "FAIL_CLOSED", "LEGAL_MAPPING_ERROR"
    if not transition.get("official_source_confirmed") or not transition.get("article_reference_current") or not transition.get("evidence_fresh"):
        return "FAIL_CLOSED", "LEGAL_REFERENCE_STALE"
    if native == "prohibited_practice":
        return "DENY", "PROHIBITED_PRACTICE"
    if not transition.get("delegation_current"):
        return "DENY", "AUTHORITY_DRIFT"
    if not transition.get("scope_matches"):
        return "DENY", "REGULATORY_SCOPE_DIVERGENCE"
    if not transition.get("actor_identity_verified") or not transition.get("policy_reference_current"):
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
        "framework_id": "eu-ai-act",
        "evaluation_mode": "DETERMINISTIC_SIMULATION_ONLY",
        "native_execution_observed": False,
        "legal_effect_determined": False,
        "stegverse_governance_compatibility_observed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_cases": len(results),
        "matching_cases": matched,
        "result": "CONTRACT_SIMULATION_PASS" if matched == len(results) else "CONTRACT_SIMULATION_FAIL",
        "translation_boundary": "EU AI Act text, risk classification, prohibited-practice analysis, conformity, and regulatory obligations contribute legal-context evidence only; they do not establish current standing, commit-time admissibility, execution authority, or legal advice.",
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
    print(f"EU AI ACT GOVERNANCE COMPATIBILITY: {'PASS' if matched == len(results) else 'FAIL'}")
    print(f"cases={len(results)} matched={matched}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if matched != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
