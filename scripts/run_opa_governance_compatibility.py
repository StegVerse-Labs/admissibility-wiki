#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "opa-governance-compatibility-cases.v1.json"
UPSTREAM = ROOT / "reports" / "upstream-opa"
INDEPENDENT = ROOT / "reports" / "external-frameworks" / "opa-independent"
OUTPUT = INDEPENDENT / "opa-stegverse-governance-compatibility-receipt.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_opa_decision(capture: dict) -> bool | None:
    if capture.get("runtime", {}).get("exit_code") != 0:
        return None
    output = capture.get("output")
    try:
        value = output["result"][0]["expressions"][0]["value"]
    except (KeyError, IndexError, TypeError):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, dict) and isinstance(value.get("allow"), bool):
        return value["allow"]
    return None


def evaluate(case: dict, native_decision: bool | None) -> tuple[str, str | None]:
    transition = case["transition"]
    if native_decision is None:
        return "FAIL_CLOSED", "FRAMEWORK_RUNTIME_ERROR"
    if native_decision is False:
        return "DENY", "POLICY_DENIAL"
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
    required = {
        "fixture": FIXTURE,
        "allow_capture": UPSTREAM / "opa-allow-capture.json",
        "deny_capture": UPSTREAM / "opa-deny-capture.json",
        "capture_receipt": UPSTREAM / "opa-replay-receipt.json",
        "independent_allow": INDEPENDENT / "opa-allow-independent-replay.json",
        "independent_deny": INDEPENDENT / "opa-deny-independent-replay.json",
        "independent_receipt": INDEPENDENT / "opa-independent-replay-receipt.json",
    }
    missing = [str(path.relative_to(ROOT)) for path in required.values() if not path.exists()]
    if missing:
        print("OPA GOVERNANCE COMPATIBILITY: BLOCKED — missing artifacts", file=sys.stderr)
        for path in missing:
            print(f"- {path}", file=sys.stderr)
        return 2

    fixture = load(FIXTURE)
    captures = {
        "allow": load(required["allow_capture"]),
        "deny": load(required["deny_capture"]),
    }
    independent = {
        "allow": load(required["independent_allow"]),
        "deny": load(required["independent_deny"]),
    }
    capture_receipt = load(required["capture_receipt"])
    independent_receipt = load(required["independent_receipt"])

    if capture_receipt.get("replay_state") != "replay_confirmed_same_environment":
        print("OPA GOVERNANCE COMPATIBILITY: BLOCKED — same-environment replay not confirmed", file=sys.stderr)
        return 2
    if independent_receipt.get("replay_state") != "replay_confirmed_independent_environment":
        print("OPA GOVERNANCE COMPATIBILITY: BLOCKED — fresh-runner replay not confirmed", file=sys.stderr)
        return 2

    native_decisions = {name: extract_opa_decision(payload) for name, payload in captures.items()}
    independent_decisions = {name: extract_opa_decision(payload) for name, payload in independent.items()}
    if native_decisions != independent_decisions:
        print("OPA GOVERNANCE COMPATIBILITY: FAIL — native decision differs on fresh runner", file=sys.stderr)
        return 1

    results = []
    all_match = True
    for case in fixture["cases"]:
        native_case = case["native_case"]
        observed_native = None if native_case == "error" else native_decisions[native_case]
        observed_result, observed_failure = evaluate(case, observed_native)
        expected_result = case["expected_stegverse_result"]
        expected_failure = case["expected_failure_class"]
        case_match = observed_result == expected_result and observed_failure == expected_failure
        all_match = all_match and case_match
        results.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "native_case": native_case,
            "observed_opa_decision": observed_native,
            "translation_mapping": "OPA decision enters as policy evidence; all StegVerse commit-time fields are evaluated independently.",
            "stegverse_transition_input": case["transition"],
            "expected_stegverse_result": expected_result,
            "observed_stegverse_result": observed_result,
            "expected_failure_class": expected_failure,
            "observed_failure_class": observed_failure,
            "case_match": case_match,
            "reason": case["reason"],
        })

    receipt = {
        "schema": "opa_stegverse_governance_compatibility_receipt.v1",
        "framework_id": "open-policy-agent",
        "compatibility_scope": "OPA v1.0.0 policy-decision evidence routed into a deterministic StegVerse commit-time evaluation fixture.",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/admissibility-wiki",
        "commit": os.getenv("GITHUB_SHA"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "framework_version": fixture["framework_version"],
        "query": fixture["query"],
        "framework_artifact_hashes": {
            key: sha256(path) for key, path in required.items() if key != "fixture"
        },
        "fixture": {
            "path": str(FIXTURE.relative_to(ROOT)),
            "sha256": sha256(FIXTURE),
        },
        "native_decisions": native_decisions,
        "fresh_runner_native_decisions": independent_decisions,
        "same_environment_replay": capture_receipt.get("replay_state"),
        "fresh_runner_replay": independent_receipt.get("replay_state"),
        "results": results,
        "summary": {
            "total_cases": len(results),
            "matching_cases": sum(1 for result in results if result["case_match"]),
            "all_expected_results_matched": all_match,
            "bounded_compatibility_state": "GOVERNANCE_COMPATIBILITY_OBSERVED" if all_match else "COMPATIBILITY_MISMATCH",
        },
        "replay_commands": [
            "python scripts/run_pinned_opa_ci_capture.py",
            "python scripts/run_independent_opa_ci_replay.py",
            "python scripts/run_opa_governance_compatibility.py",
        ],
        "limitations": [
            "The StegVerse evaluator is a deterministic compatibility fixture, not a production SPE deployment.",
            "The fresh runner uses the same GitHub Actions provider and the same OPA implementation.",
            "No independent organization or independent StegVerse implementation has reproduced the result.",
            "The result applies only to the pinned policy, inputs, mapping, cases, and commit-time conditions recorded here.",
        ],
        "authority_boundary": {
            "opa_allow_is_stegverse_allow": False,
            "compatibility_receipt_is_execution_authority": False,
            "compatibility_receipt_creates_standing": False,
            "general_compatibility_claim_allowed": False,
            "certification_claim_allowed": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if not all_match:
        print(f"OPA GOVERNANCE COMPATIBILITY: MISMATCH -> {OUTPUT.relative_to(ROOT)}")
        return 1
    print(f"OPA GOVERNANCE COMPATIBILITY: OBSERVED -> {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
