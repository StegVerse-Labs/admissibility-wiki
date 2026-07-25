#!/usr/bin/env python3
"""Deterministically verify the bounded revised Rigel DecisionAssure pilot package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
TRACE = ROOT / "trace_rigel_revised.json"
POLICIES = ROOT / "canonical_policies.json"
DELEGATIONS = ROOT / "canonical_delegations.json"
RECEIPT = ROOT / "verification_receipt.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"top_level_not_object:{path.name}")
    return value


def canonical_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    trace = load(TRACE)
    policies_doc = load(POLICIES)
    delegations_doc = load(DELEGATIONS)

    require(trace.get("schema") == "stegverse.decisionassure.pilot_trace.v1", "trace_schema_mismatch")
    require(policies_doc.get("schema") == "stegverse.canonical_policies.v1", "policy_schema_mismatch")
    require(delegations_doc.get("schema") == "stegverse.canonical_delegations.v1", "delegation_schema_mismatch")

    policies = {item["policy_id"]: item for item in policies_doc.get("policies", [])}
    delegations = {item["delegation_id"]: item for item in delegations_doc.get("delegations", [])}

    delegation = delegations.get(trace.get("delegation_ref"))
    require(delegation is not None, "delegation_missing")
    require(delegation.get("actor_id") == trace.get("actor_id"), "delegation_actor_mismatch")
    require(delegation.get("status") == "CURRENT", "delegation_not_current")
    require(trace.get("action") in delegation.get("actions", []), "delegation_action_missing")

    referenced_policy = policies.get(trace.get("policy_ref"))
    require(referenced_policy is not None, "referenced_policy_missing")
    current = next((item for item in policies.values() if item.get("status") == "CURRENT"), None)
    require(current is not None, "current_policy_missing")

    mutation = trace.get("mutation") or {}
    policy_drift = (
        mutation.get("type") == "policy_version_change"
        and mutation.get("occurred_before_commit") is True
        and referenced_policy.get("version") != current.get("version")
    )
    current_denies = trace.get("action") in current.get("denies", [])

    derived_decision = "DENY" if policy_drift and current_denies else "ALLOW"
    derived_failure = "POLICY_DRIFT" if derived_decision == "DENY" else None

    expected = trace.get("stegverse_expected_result") or {}
    require(expected.get("decision") == derived_decision, "expected_decision_mismatch")
    require(expected.get("failure_class") == derived_failure, "expected_failure_class_mismatch")
    require(expected.get("authority_effect") == "NONE", "authority_effect_must_be_none")

    native = trace.get("decisionassure_result") or {}
    require(native.get("decision") == "DENY", "decisionassure_result_mismatch")
    require(native.get("trace_integrity") == "CORRUPT", "decisionassure_integrity_mismatch")
    require(native.get("causal_continuity_persisted") is False, "decisionassure_continuity_mismatch")

    receipt = {
        "schema": "stegverse.decisionassure.pilot_verification_receipt.v1",
        "trace_id": trace.get("trace_id"),
        "result": "PASS",
        "derived_decision": derived_decision,
        "derived_failure_class": derived_failure,
        "policy_drift_detected": policy_drift,
        "current_policy_denies_action": current_denies,
        "trace_sha256": digest(trace),
        "canonical_policies_sha256": digest(policies_doc),
        "canonical_delegations_sha256": digest(delegations_doc),
        "authority_effect": "NONE",
        "native_execution_observed": False,
        "general_compatibility_claimed": False,
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("DECISIONASSURE_RIGEL_REVISED_VERIFICATION: PASS")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
