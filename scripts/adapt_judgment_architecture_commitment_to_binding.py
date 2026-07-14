#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def evidence_ref(value: Any, fallback: str) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        refs = [item.strip() for item in value if isinstance(item, str) and item.strip()]
        if refs:
            return refs
    return [fallback]


def derive_control(evidence: dict[str, Any], key: str) -> dict[str, Any]:
    item = evidence.get(key)
    if not isinstance(item, dict):
        return {"result": "UNRESOLVED", "evidence_refs": [f"missing:{key}"]}
    observed = item.get("observed_result")
    if observed not in {"VALID", "INVALID", "UNRESOLVED"}:
        observed = "UNRESOLVED"
    return {
        "result": observed,
        "evidence_refs": evidence_ref(item.get("evidence_refs"), f"missing:{key}.evidence_refs"),
    }


def derive_admissibility(evidence: dict[str, Any]) -> dict[str, Any]:
    item = evidence.get("admissibility")
    if not isinstance(item, dict):
        return {"result": "FAIL_CLOSED", "evidence_refs": ["missing:admissibility"]}
    observed = item.get("observed_result")
    if observed not in {"ALLOW", "DENY", "FAIL_CLOSED"}:
        observed = "FAIL_CLOSED"
    return {
        "result": observed,
        "evidence_refs": evidence_ref(item.get("evidence_refs"), "missing:admissibility.evidence_refs"),
    }


def derive_invariants(evidence: dict[str, Any]) -> dict[str, Any]:
    item = evidence.get("invariants")
    if not isinstance(item, dict):
        return {"result": "UNRESOLVED", "evidence_refs": ["missing:invariants"]}
    observed = item.get("observed_result")
    if observed not in {"PRESERVED", "VIOLATED", "UNRESOLVED"}:
        observed = "UNRESOLVED"
    return {
        "result": observed,
        "evidence_refs": evidence_ref(item.get("evidence_refs"), "missing:invariants.evidence_refs"),
    }


def derive_recoverability(evidence: dict[str, Any]) -> dict[str, Any]:
    item = evidence.get("recoverability")
    if not isinstance(item, dict):
        return {
            "result": "UNRESOLVED",
            "margin": 0.0,
            "minimum_margin": 0.0,
            "evidence_refs": ["missing:recoverability"],
        }
    observed = item.get("observed_result")
    if observed not in {"PRESERVED", "DEGRADED", "LOST", "UNRESOLVED"}:
        observed = "UNRESOLVED"
    margin = item.get("margin")
    minimum = item.get("minimum_margin")
    if not isinstance(margin, (int, float)) or margin < 0:
        margin = 0.0
        observed = "UNRESOLVED"
    if not isinstance(minimum, (int, float)) or minimum < 0:
        minimum = 0.0
        observed = "UNRESOLVED"
    return {
        "result": observed,
        "margin": float(margin),
        "minimum_margin": float(minimum),
        "evidence_refs": evidence_ref(item.get("evidence_refs"), "missing:recoverability.evidence_refs"),
    }


def derive_evidence_state(evidence: dict[str, Any]) -> dict[str, Any]:
    item = evidence.get("evidence_state")
    if not isinstance(item, dict):
        return {"result": "INCOMPLETE", "refs": ["missing:evidence_state"]}
    observed = item.get("observed_result")
    if observed not in {"COMPLETE", "INCOMPLETE", "UNRESOLVED", "STALE"}:
        observed = "UNRESOLVED"
    return {
        "result": observed,
        "refs": evidence_ref(item.get("refs"), "missing:evidence_state.refs"),
    }


def evaluate_binding(record: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if record["decision_validity"] != "VALID":
        reasons.append("DECISION_INVALID_OR_UNRESOLVED")
    if record["origin"]["result"] == "INVALID":
        reasons.append("ORIGIN_INVALID")
    elif record["origin"]["result"] != "VALID":
        reasons.append("ORIGIN_UNRESOLVED")
    if record["authority"]["result"] == "INVALID":
        reasons.append("AUTHORITY_INVALID")
    elif record["authority"]["result"] != "VALID":
        reasons.append("AUTHORITY_UNRESOLVED")
    if record["admissibility"]["result"] == "DENY":
        reasons.append("ADMISSIBILITY_DENY")
    elif record["admissibility"]["result"] != "ALLOW":
        reasons.append("ADMISSIBILITY_UNRESOLVED")
    if record["invariants"]["result"] == "VIOLATED":
        reasons.append("INVARIANTS_VIOLATED")
    elif record["invariants"]["result"] != "PRESERVED":
        reasons.append("INVARIANTS_UNRESOLVED")
    recovery = record["recoverability"]
    if recovery["result"] in {"DEGRADED", "LOST"} or recovery["margin"] < recovery["minimum_margin"]:
        reasons.append("RECOVERABILITY_INSUFFICIENT")
    elif recovery["result"] != "PRESERVED":
        reasons.append("RECOVERABILITY_UNRESOLVED")
    evidence_state = record["evidence"]["result"]
    if evidence_state in {"INCOMPLETE", "STALE"}:
        reasons.append(f"EVIDENCE_{evidence_state}")
    elif evidence_state != "COMPLETE":
        reasons.append("EVIDENCE_UNRESOLVED")

    hard_denials = {
        "ORIGIN_INVALID", "AUTHORITY_INVALID", "ADMISSIBILITY_DENY",
        "INVARIANTS_VIOLATED", "RECOVERABILITY_INSUFFICIENT",
    }
    if any(reason in hard_denials for reason in reasons):
        return "DENY", reasons
    if reasons:
        return "FAIL_CLOSED", reasons
    return "BIND", []


def adapt(payload: dict[str, Any]) -> dict[str, Any]:
    commitment = payload.get("commitment_record")
    evidence = payload.get("live_evidence")
    if not isinstance(commitment, dict):
        commitment = {}
    if not isinstance(evidence, dict):
        evidence = {}

    decision_validity = evidence.get("decision_validity")
    if decision_validity not in {"VALID", "INVALID", "UNRESOLVED", "NOT_EVALUATED"}:
        decision_validity = "UNRESOLVED"

    transition_id = evidence.get("transition_id")
    if not isinstance(transition_id, str) or not transition_id.strip():
        transition_id = f"unresolved:{commitment.get('record_id', 'unknown')}"

    record: dict[str, Any] = {
        "schema_version": "commit_boundary_binding_record.v1",
        "transition_id": transition_id,
        "candidate_hash": canonical_hash(commitment),
        "state_before_hash": canonical_hash(evidence.get("state_before", {"missing": True})),
        "state_after_hash": canonical_hash(evidence.get("state_after", {"missing": True})),
        "decision_validity": decision_validity,
        "origin": derive_control(evidence, "origin"),
        "authority": derive_control(evidence, "authority"),
        "admissibility": derive_admissibility(evidence),
        "invariants": derive_invariants(evidence),
        "recoverability": derive_recoverability(evidence),
        "evidence": derive_evidence_state(evidence),
        "binding_result": "FAIL_CLOSED",
        "reason_codes": [],
        "evaluated_at": evidence.get("evaluated_at") or datetime.now(timezone.utc).isoformat(),
        "committed_at": None,
        "previous_receipt_hash": evidence.get("previous_receipt_hash"),
        "receipt_hash": None,
    }
    result, reasons = evaluate_binding(record)
    record["binding_result"] = result
    record["reason_codes"] = reasons
    record["committed_at"] = record["evaluated_at"] if result == "BIND" else None
    receipt_material = {key: value for key, value in record.items() if key != "receipt_hash"}
    record["receipt_hash"] = canonical_hash(receipt_material)
    return record


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: adapt_judgment_architecture_commitment_to_binding.py <input.json>")
        return 2
    path = Path(sys.argv[1])
    payload = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(adapt(payload), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
