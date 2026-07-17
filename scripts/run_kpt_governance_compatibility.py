#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/kpt-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/kpt/kpt-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case.get("native_result")
    transition = case.get("transition", {})
    if native == "decision_error":
        return "FAIL_CLOSED", "KPT_DECISION_ERROR"
    if not transition.get("official_source_confirmed") or not transition.get("evidence_fresh"):
        return "FAIL_CLOSED", "OFFICIAL_SOURCE_MISSING"
    if native == "decision_deny":
        return "DENY", "KPT_DECISION_DENY"
    if not transition.get("delegation_current"):
        return "DENY", "AUTHORITY_DRIFT"
    if not transition.get("scope_matches"):
        return "DENY", "DOWNSTREAM_CONSEQUENCE_DIVERGENCE"
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
        "framework_id": "kpt",
        "evaluation_mode": "DETERMINISTIC_SIMULATION_ONLY",
        "native_execution_observed": False,
        "official_source_confirmed": False,
        "stegverse_governance_compatibility_observed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_cases": len(results),
        "matching_cases": matched,
        "result": "CONTRACT_SIMULATION_PASS" if matched == len(results) else "CONTRACT_SIMULATION_FAIL",
        "translation_boundary": "KPT positioning, decision states, trace evidence, and boundary-before-consequence language contribute source-bounded evidence only; they do not establish current standing, delegation, commit-time admissibility, or execution authority.",
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
    print(f"KPT GOVERNANCE COMPATIBILITY: {'PASS' if matched == len(results) else 'FAIL'}")
    print(f"cases={len(results)} matched={matched}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if matched != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
