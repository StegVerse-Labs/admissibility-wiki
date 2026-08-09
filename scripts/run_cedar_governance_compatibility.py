#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "cedar-governance-compatibility-cases.v1.json"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "cedar" / "cedar-stegverse-governance-compatibility-receipt.json"


def load_capture(capture_dir: Path, name: str, expected_decision: str, expected_exit: int) -> dict[str, Any]:
    path = capture_dir / name
    if not path.exists():
        raise ValueError(f"missing native Cedar capture: {path}")
    capture = json.loads(path.read_text(encoding="utf-8"))
    runtime = capture.get("runtime", {})
    decision = runtime.get("observed_decision")
    exit_code = runtime.get("exit_code")
    semantics_validated = runtime.get("decision_semantics_validated") is True
    if decision != expected_decision or exit_code != expected_exit or not semantics_validated:
        raise ValueError(
            f"invalid native Cedar capture {path}: decision={decision!r} exit={exit_code!r} validated={semantics_validated!r}"
        )
    return {
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "case_id": capture.get("case_id"),
        "decision": decision,
        "exit_code": exit_code,
        "implementation_id": runtime.get("implementation_id"),
        "version_output": runtime.get("version_output"),
        "hashes": capture.get("hashes", {}),
    }


def evaluate(case: dict, native_responses: dict[str, dict[str, Any]] | None) -> tuple[str, list[str], str, dict[str, Any] | None]:
    declared_response = case.get("cedar_response")
    transition = case.get("transition", {})
    reasons: list[str] = []
    runtime_evidence = None
    response_origin = "declared_fixture_response"

    if native_responses is not None and declared_response in native_responses:
        runtime_evidence = native_responses[declared_response]
        response_origin = "native_observed_response_class"

    if declared_response == "error":
        return "FAIL_CLOSED", ["cedar_runtime_error"], response_origin, runtime_evidence
    if declared_response == "forbid":
        return "DENY", ["cedar_native_forbid"], response_origin, runtime_evidence
    if declared_response != "permit":
        return "FAIL_CLOSED", ["cedar_response_unrecognized"], response_origin, runtime_evidence

    if not transition.get("principal_identity_verified"):
        reasons.append("principal_identity_unverified")
    if not transition.get("delegation_current"):
        reasons.append("delegation_not_current")
    if not transition.get("policy_reference_current"):
        reasons.append("policy_reference_not_current")
    if not transition.get("entity_store_current") or not transition.get("evidence_fresh"):
        return "FAIL_CLOSED", ["entity_or_evidence_stale"], response_origin, runtime_evidence
    if not transition.get("resource_matches_scope"):
        reasons.append("resource_outside_governed_scope")
    if not transition.get("recoverability_satisfied"):
        reasons.append("recoverability_unsatisfied")
    if not transition.get("execution_context_current"):
        return "FAIL_CLOSED", ["execution_context_stale"], response_origin, runtime_evidence

    result = ("DENY", reasons) if reasons else ("ALLOW", ["cedar_permit_accepted_as_policy_evidence_only"])
    return result[0], result[1], response_origin, runtime_evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Cedar response classes against StegVerse governance conditions.")
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--capture-dir",
        help="Optional directory containing cedar-allow-capture.json and cedar-deny-capture.json from a validated native capture.",
    )
    args = parser.parse_args()

    fixture_path = Path(args.fixture).resolve()
    output_path = Path(args.output).resolve()
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    native_responses: dict[str, dict[str, Any]] | None = None
    native_capture_error = None
    if args.capture_dir:
        capture_dir = Path(args.capture_dir).resolve()
        try:
            native_responses = {
                "permit": load_capture(capture_dir, "cedar-allow-capture.json", "ALLOW", 0),
                "forbid": load_capture(capture_dir, "cedar-deny-capture.json", "DENY", 2),
            }
        except ValueError as exc:
            native_capture_error = str(exc)

    results = []
    failures = []
    if args.capture_dir and native_capture_error:
        failures.append("native_capture_binding")

    for case in fixture.get("cases", []):
        observed, reasons, response_origin, runtime_evidence = evaluate(case, native_responses)
        expected = case.get("expected_stegverse_result")
        matched = observed == expected
        results.append({
            "case_id": case.get("case_id"),
            "family": case.get("family"),
            "cedar_response": case.get("cedar_response"),
            "cedar_response_origin": response_origin,
            "runtime_evidence": runtime_evidence,
            "expected_stegverse_result": expected,
            "observed_stegverse_result": observed,
            "matched": matched,
            "reasons": reasons,
        })
        if not matched:
            failures.append(case.get("case_id"))

    native_bound = native_responses is not None and native_capture_error is None
    receipt = {
        "schema": "cedar_stegverse_governance_compatibility_receipt.v2",
        "framework_id": "cedar-policy",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "contract_state": "NATIVE_ALLOW_DENY_OBSERVED_TRANSLATION_MIXED" if native_bound else "SIMULATED_GOVERNANCE_TRANSLATION_ONLY",
        "native_runtime_execution_observed": native_bound,
        "native_response_classes_observed": ["permit", "forbid"] if native_bound else [],
        "native_runtime_error_class_observed": False,
        "native_capture_binding_error": native_capture_error,
        "binary_build_evidence_required": "reports/external-frameworks/cedar-build/cedar-binary-build-receipt.json",
        "fixture": str(fixture_path.relative_to(ROOT)) if fixture_path.is_relative_to(ROOT) else str(fixture_path),
        "cases_total": len(results),
        "cases_matched": sum(1 for item in results if item["matched"]),
        "overall_result": "PASS" if not failures else "FAIL",
        "results": results,
        "limitations": [
            "Native Cedar ALLOW and DENY response classes are bound from the validated repository fixture capture when --capture-dir is supplied.",
            "The six StegVerse governance transition conditions remain deterministic test fixtures; observing Cedar ALLOW/DENY does not independently prove each transition predicate.",
            "The runtime-error response class remains declared rather than natively reproduced by this transition.",
            "No same-environment replay, fresh-runner replay, independent provider reproduction, certification, or general compatibility is established by this receipt.",
            "A passing translation result does not grant standing or execution authority.",
        ],
        "authority_boundary": {
            "cedar_response_is_execution_authority": False,
            "native_capture_is_general_compatibility_proof": False,
            "compatibility_receipt_grants_standing": False,
            "general_compatibility_claim_allowed": False,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    mode = "native_allow_deny_bound" if native_bound else "simulated"
    print(f"CEDAR GOVERNANCE COMPATIBILITY: {receipt['overall_result']} cases={len(results)} mode={mode}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
