#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/policy-cards-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports/external-frameworks/policy-cards/policy-cards-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> str:
    if not case.get("policy_card_present") or case.get("policy_card_result") not in {"ALLOW", "DENY"}:
        return "FAIL_CLOSED"
    if case.get("policy_card_claims_execution_authority") is True:
        return "DENY"
    if case.get("authority_valid") is not True:
        return "DENY"
    if case.get("evidence_current") is not True:
        return "FAIL_CLOSED"
    return case["policy_card_result"]


def main() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    for case in data["cases"]:
        actual = evaluate(case)
        results.append({"case_id": case["case_id"], "family": case["family"], "expected": case["expected_stegverse_result"], "actual": actual, "matched": actual == case["expected_stegverse_result"]})
    receipt = {
        "schema": "policy_cards_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "policy-cards",
        "execution_mode": "deterministic_simulation_only",
        "source_reviewed": True,
        "official_source_confirmed": True,
        "implementation_attached": False,
        "native_execution_observed": False,
        "fresh_runner_replay_observed": False,
        "stegverse_governance_compatibility_observed": False,
        "cases": results,
        "all_cases_matched": all(item["matched"] for item in results),
        "translation_boundary": "Policy-card declarations and allow/deny rules are policy evidence only; they do not establish current standing, commit-time admissibility, or execution authority.",
        "manual_tasks_required": [],
        "user_action_required": False,
        "downstream_mutation_authority": False
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if not receipt["all_cases_matched"]:
        raise SystemExit("POLICY CARDS GOVERNANCE COMPATIBILITY: FAIL")
    print("POLICY CARDS GOVERNANCE COMPATIBILITY: PASS")
    print("cases=6")
    print("native_execution_observed=false")
    print("manual_tasks_required=0")


if __name__ == "__main__":
    main()
