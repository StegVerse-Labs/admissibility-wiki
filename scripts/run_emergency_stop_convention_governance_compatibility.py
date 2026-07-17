#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/external-frameworks/emergency-stop-convention-governance-compatibility-cases.v1.json"
OUT = ROOT / "reports/external-frameworks/emergency-stop-convention/emergency-stop-convention-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, str | None]:
    native = case.get("native_result")
    transition = case.get("transition", {})
    if native == "protocol_error":
        return "FAIL_CLOSED", "STOP_PROTOCOL_ERROR"
    if not transition.get("evidence_fresh"):
        return "FAIL_CLOSED", "STOP_EVIDENCE_STALE"
    if not transition.get("signal_authentic"):
        return "FAIL_CLOSED", "STOP_SIGNAL_AUTHENTICITY_UNRESOLVED"
    if not transition.get("scope_matches"):
        return "ESCALATE", "STOP_SCOPE_DIVERGENCE"
    if native == "stop_signal_valid" and transition.get("stop_condition_current"):
        return "DENY", "EMERGENCY_STOP_ACTIVE"
    if native == "stop_signal_absent":
        return "ESCALATE", "NO_STOP_SIGNAL_AUTHORITY_INCOMPLETE"
    return "FAIL_CLOSED", "STOP_STATE_UNRESOLVED"


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
        "framework_id": "emergency-stop-convention",
        "evaluation_mode": "DETERMINISTIC_SIMULATION_ONLY",
        "native_execution_observed": False,
        "stegverse_governance_compatibility_observed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_cases": len(results),
        "matching_cases": matched,
        "result": "CONTRACT_SIMULATION_PASS" if matched == len(results) else "CONTRACT_SIMULATION_FAIL",
        "translation_boundary": "Emergency-stop convention files, stop conditions, and signals contribute bounded control evidence only; a stop signal can block or escalate but does not establish positive execution authority, current standing, or universal scope.",
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
    print(f"EMERGENCY STOP CONVENTION GOVERNANCE COMPATIBILITY: {'PASS' if matched == len(results) else 'FAIL'}")
    print(f"cases={len(results)} matched={matched}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if matched != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
