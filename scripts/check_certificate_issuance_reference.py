#!/usr/bin/env python3
"""Validate the Governance-Chain Certification reference issuance pipeline.

This validator proves a deterministic reference-only certificate path and its
negative controls. It does not activate public certification authority.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data/certification/issuance/reference-issuance-bundle.v0.1.json"


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def reject_reason(bundle: dict) -> str | None:
    candidate = bundle.get("candidate")
    evidence = bundle.get("evidence")
    cert = bundle.get("certificate")
    if not isinstance(candidate, dict) or not isinstance(evidence, dict) or not isinstance(cert, dict):
        return "missing candidate/evidence/certificate"
    if canonical_hash(candidate) != bundle.get("candidate_hash"):
        return "candidate hash mismatch"
    if canonical_hash(evidence) != bundle.get("evidence_hash"):
        return "evidence hash mismatch"
    if canonical_hash(cert) != bundle.get("certificate_hash"):
        return "certificate hash mismatch"
    if evidence.get("candidate_hash") != bundle.get("candidate_hash"):
        return "evidence candidate binding mismatch"
    if cert.get("candidate_hash") != bundle.get("candidate_hash"):
        return "certificate candidate binding mismatch"
    if cert.get("evidence_hash") != bundle.get("evidence_hash"):
        return "certificate evidence binding mismatch"
    if evidence.get("validator", {}).get("status") != "PASS":
        return "validator not PASS"
    if evidence.get("negative_controls_complete") is not True:
        return "negative controls incomplete"
    if evidence.get("portable_verification") is not True:
        return "portable verification absent"
    if evidence.get("authority_effect") != "NONE" or cert.get("authority_effect") != "NONE":
        return "authority effect must be NONE"
    for result in evidence.get("property_results", []):
        if result.get("state") in {"INDETERMINATE", "STALE_OR_EXPIRED", "REVOKED", "NOT_CERTIFIED"}:
            return "required property is not certifiable"
    lifecycle = cert.get("lifecycle", {}).get("state")
    if lifecycle in {"EXPIRED", "SUSPENDED", "REVOKED", "SUPERSEDED"}:
        return "certificate lifecycle blocks issuance"
    if cert.get("certificate_class") == "REFERENCE_CERTIFICATE" and cert.get("public_claim_allowed") is not False:
        return "reference certificate cannot allow public claim"
    if cert.get("commercial_relationship", {}).get("outcome_purchased") is not False:
        return "outcome purchase is prohibited"
    if cert.get("external_subject") is not False:
        return "reference certificate cannot bind external subject"
    if cert.get("overall_state") != "CERTIFIED_WITH_LIMITS":
        return "reference certificate must be bounded"
    return None


def mutate_case(bundle: dict, case_id: str) -> dict:
    mutated = copy.deepcopy(bundle)
    if case_id == "NEG-MISSING-EVIDENCE":
        mutated.pop("evidence", None)
    elif case_id == "NEG-INDETERMINATE":
        mutated["evidence"]["property_results"][0]["state"] = "INDETERMINATE"
        mutated["evidence_hash"] = canonical_hash(mutated["evidence"])
        mutated["certificate"]["evidence_hash"] = mutated["evidence_hash"]
        mutated["certificate_hash"] = canonical_hash(mutated["certificate"])
    elif case_id == "NEG-HASH-MISMATCH":
        mutated["evidence"]["portable_verification"] = False
    elif case_id == "NEG-PUBLIC-REFERENCE":
        mutated["certificate"]["public_claim_allowed"] = True
        mutated["certificate_hash"] = canonical_hash(mutated["certificate"])
    elif case_id == "NEG-OUTCOME-PURCHASED":
        mutated["certificate"]["commercial_relationship"]["outcome_purchased"] = True
        mutated["certificate_hash"] = canonical_hash(mutated["certificate"])
    elif case_id == "NEG-REVOKED":
        mutated["certificate"]["lifecycle"]["state"] = "REVOKED"
        mutated["certificate_hash"] = canonical_hash(mutated["certificate"])
    else:
        raise AssertionError(f"unknown negative case {case_id}")
    return mutated


def main() -> int:
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    reason = reject_reason(bundle)
    if reason is not None:
        raise AssertionError(f"reference bundle rejected: {reason}")

    negative_cases = bundle.get("negative_issuance_cases", [])
    if len(negative_cases) < 6:
        raise AssertionError("minimum negative issuance coverage missing")

    for case in negative_cases:
        case_id = case["case_id"]
        mutated = mutate_case(bundle, case_id)
        reason = reject_reason(mutated)
        if reason is None:
            raise AssertionError(f"negative case incorrectly accepted: {case_id}")

    decision = bundle.get("activation_decision", {})
    assert decision.get("pipeline_state") == "PIPELINE_OPERATIONAL_REFERENCE_ONLY"
    assert decision.get("public_certification_authority") == "INACTIVE"
    assert decision.get("certificate_issuance_authority") == "REFERENCE_ONLY"
    assert decision.get("external_certification_issued") is False

    print("CERTIFICATE_ISSUANCE_REFERENCE: PASS")
    print(f"certificate={bundle['certificate']['certificate_id']}")
    print(f"certificate_hash={bundle['certificate_hash']}")
    print(f"negative_cases={len(negative_cases)}")
    print("pipeline=PIPELINE_OPERATIONAL_REFERENCE_ONLY")
    print("public_authority=INACTIVE")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
