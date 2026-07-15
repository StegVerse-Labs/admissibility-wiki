#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "cedar-governance-compatibility-cases.v1.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "cedar" / "cedar-stegverse-governance-compatibility-receipt.json"


def evaluate(case: dict) -> tuple[str, list[str]]:
    response = case.get("cedar_response")
    transition = case.get("transition", {})
    reasons: list[str] = []

    if response == "error":
        return "FAIL_CLOSED", ["cedar_runtime_error"]
    if response == "forbid":
        return "DENY", ["cedar_native_forbid"]
    if response != "permit":
        return "FAIL_CLOSED", ["cedar_response_unrecognized"]

    if not transition.get("principal_identity_verified"):
        reasons.append("principal_identity_unverified")
    if not transition.get("delegation_current"):
        reasons.append("delegation_not_current")
    if not transition.get("policy_reference_current"):
        reasons.append("policy_reference_not_current")
    if not transition.get("entity_store_current") or not transition.get("evidence_fresh"):
        return "FAIL_CLOSED", ["entity_or_evidence_stale"]
    if not transition.get("resource_matches_scope"):
        reasons.append("resource_outside_governed_scope")
    if not transition.get("recoverability_satisfied"):
        reasons.append("recoverability_unsatisfied")
    if not transition.get("execution_context_current"):
        return "FAIL_CLOSED", ["execution_context_stale"]

    return ("DENY", reasons) if reasons else ("ALLOW", ["cedar_permit_accepted_as_policy_evidence_only"])


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    results = []
    failures = []
    for case in fixture.get("cases", []):
        observed, reasons = evaluate(case)
        expected = case.get("expected_stegverse_result")
        matched = observed == expected
        results.append({
            "case_id": case.get("case_id"),
            "family": case.get("family"),
            "cedar_response": case.get("cedar_response"),
            "expected_stegverse_result": expected,
            "observed_stegverse_result": observed,
            "matched": matched,
            "reasons": reasons,
        })
        if not matched:
            failures.append(case.get("case_id"))

    receipt = {
        "schema": "cedar_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "cedar-policy",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "contract_state": "SIMULATED_GOVERNANCE_TRANSLATION_ONLY",
        "native_runtime_execution_observed": False,
        "binary_build_evidence_required": "reports/external-frameworks/cedar-build/cedar-binary-build-receipt.json",
        "cases_total": len(results),
        "cases_matched": sum(1 for item in results if item["matched"]),
        "overall_result": "PASS" if not failures else "FAIL",
        "results": results,
        "limitations": [
            "The selected Cedar binary has been built and hashed but was not executed for these cases.",
            "Cedar responses in the fixture are predeclared test inputs, not captured runtime outputs.",
            "A passing translation simulation does not establish live Cedar integration or general compatibility.",
        ],
        "authority_boundary": {
            "cedar_response_is_execution_authority": False,
            "translation_simulation_is_runtime_evidence": False,
            "compatibility_receipt_grants_standing": False,
            "general_compatibility_claim_allowed": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"CEDAR GOVERNANCE COMPATIBILITY: {receipt['overall_result']} simulated_cases={len(results)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
