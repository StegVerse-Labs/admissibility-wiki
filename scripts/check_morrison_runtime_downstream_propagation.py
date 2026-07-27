#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "external-frameworks" / "evidence" / "morrison-runtime-downstream-propagation-review.template.json"
AUTHORITY = "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"
PROHIBITED = {
    "CERTIFIED_COMPATIBLE",
    "STEGVERSE_EXECUTION_AUTHORITY",
    "FULL_FRESH_STATE_RECONSTRUCTION_BY_DEFAULT",
    "PRODUCTION_VALIDATION",
    "ENDORSEMENT",
}
TARGETS = {
    "compatibility_report",
    "external_framework_index",
    "site_mirror",
    "release_snapshot",
}
REVIEWS = {
    "claim_scope_preserved",
    "source_and_route_receipts_bound",
    "no_execution_authority_inferred",
    "no_certification_or_endorsement_inferred",
    "runtime_re_evaluation_distinction_preserved",
    "rollback_path_defined",
}
EVIDENCE = {
    "public_route_receipt_sha256",
    "propagation_review_receipt_sha256",
    "target_diff_manifest_sha256",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load() -> dict:
    if not CONTRACT.exists():
        raise ValueError(f"missing {CONTRACT.relative_to(ROOT)}")
    try:
        value = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {CONTRACT.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("downstream propagation contract must contain a JSON object")
    return value


def main() -> int:
    failures: list[str] = []
    try:
        data = load()
    except ValueError as exc:
        print("MORRISON DOWNSTREAM PROPAGATION REVIEW: FAIL")
        print(f"- {exc}")
        return 1

    if data.get("source_state_required") != "WIKI_VALIDATED_AND_PUBLIC_ROUTE_VERIFIED":
        failures.append("source state requirement changed")
    if data.get("authority_posture") != AUTHORITY:
        failures.append("authority posture changed")
    if set(data.get("prohibited_promotions", [])) != PROHIBITED:
        failures.append("prohibited promotion set changed")
    if data.get("required_next_transition") != "BOUNDED_DOWNSTREAM_PROPAGATION_APPROVED":
        failures.append("next transition changed")
    if data.get("fail_closed") is not True:
        failures.append("contract must remain fail-closed")

    targets = data.get("eligible_targets", {})
    reviews = data.get("required_reviews", {})
    evidence = data.get("review_evidence", {})
    decision = data.get("decision", {})

    if set(targets) != TARGETS:
        failures.append("eligible target set changed")
    if set(reviews) != REVIEWS:
        failures.append("required review set changed")
    if set(evidence) != EVIDENCE:
        failures.append("review evidence set changed")

    state = data.get("review_state")
    if state == "PENDING_DOWNSTREAM_PROPAGATION_REVIEW":
        if any(value is not False for value in targets.values()):
            failures.append("pending targets must remain ineligible")
        if any(value is not False for value in reviews.values()):
            failures.append("pending reviews must remain false")
        if any(value != "PENDING" for value in evidence.values()):
            failures.append("pending review evidence must remain PENDING")
        if decision.get("approved_for_bounded_downstream_propagation") is not False:
            failures.append("pending contract cannot approve propagation")
        if decision.get("approved_targets") != []:
            failures.append("pending contract cannot name approved targets")
        if decision.get("activation_authority_granted") is not False:
            failures.append("propagation review cannot grant activation authority")
        mode = "PENDING_FAIL_CLOSED"
    elif state == "BOUNDED_DOWNSTREAM_PROPAGATION_APPROVED":
        if not all(value is True for value in reviews.values()):
            failures.append("approved propagation requires every review to pass")
        if not all(SHA256.fullmatch(str(value)) for value in evidence.values()):
            failures.append("approved propagation requires three SHA-256 evidence hashes")
        approved_targets = decision.get("approved_targets", [])
        if not approved_targets or not set(approved_targets).issubset(TARGETS):
            failures.append("approved targets must be a non-empty subset of declared targets")
        for target in TARGETS:
            if targets.get(target) is not (target in approved_targets):
                failures.append(f"target eligibility mismatch: {target}")
        if decision.get("approved_for_bounded_downstream_propagation") is not True:
            failures.append("approved state requires bounded propagation approval")
        if decision.get("activation_authority_granted") is not False:
            failures.append("bounded propagation must not grant activation authority")
        mode = "BOUNDED_PROPAGATION_APPROVED"
    else:
        failures.append(f"unsupported review_state: {state!r}")
        mode = "INVALID"

    if failures:
        print("MORRISON DOWNSTREAM PROPAGATION REVIEW: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MORRISON DOWNSTREAM PROPAGATION REVIEW: PASS")
    print(f"mode: {mode}")
    print(f"authority_posture: {AUTHORITY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
