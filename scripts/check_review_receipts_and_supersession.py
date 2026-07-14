#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "static" / "translation-records" / "specialist-review-output-receipts.v0.1.json"
SUPERSESSION = ROOT / "static" / "translation-records" / "external-record-supersession-state.v0.1.json"

REQUIRED_CLASSES = {
    "physics_foundations",
    "mathematical_formalism",
    "admissibility_governance",
}
ALLOWED_RESULTS = {
    "SUPPORT",
    "OBJECT",
    "DEFER",
    "INSUFFICIENT_EVIDENCE",
    "OUT_OF_SCOPE",
}


def fail(message: str) -> None:
    raise SystemExit(f"REVIEW RECEIPTS AND SUPERSESSION: FAIL - {message}")


def main() -> None:
    if not RECEIPTS.exists() or not SUPERSESSION.exists():
        fail("required record file is missing")

    receipts_data = json.loads(RECEIPTS.read_text(encoding="utf-8"))
    supersession = json.loads(SUPERSESSION.read_text(encoding="utf-8"))

    if set(receipts_data.get("required_review_classes", [])) != REQUIRED_CLASSES:
        fail("required review classes do not match the governed review set")

    receipts = receipts_data.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != len(REQUIRED_CLASSES):
        fail("exactly one receipt per required review class is required")

    seen_classes: set[str] = set()
    issued_count = 0
    placeholder_count = 0
    for receipt in receipts:
        review_class = receipt.get("review_class")
        if review_class not in REQUIRED_CLASSES:
            fail(f"unknown review class: {review_class}")
        if review_class in seen_classes:
            fail(f"duplicate review class: {review_class}")
        seen_classes.add(review_class)
        if receipt.get("review_result") not in ALLOWED_RESULTS:
            fail(f"invalid review result for {review_class}")
        posture = receipt.get("receipt_posture")
        if posture == "issued":
            issued_count += 1
            if not receipt.get("issued_at"):
                fail(f"issued receipt for {review_class} requires issued_at")
        elif posture == "placeholder_fail_closed":
            placeholder_count += 1
            if receipt.get("issued_at") is not None:
                fail(f"placeholder receipt for {review_class} must not have issued_at")
        else:
            fail(f"invalid receipt posture for {review_class}: {posture}")
        non_claims = str(receipt.get("non_claims", "")).lower()
        if "not" not in non_claims and "does not" not in non_claims:
            fail(f"receipt for {review_class} lacks an explicit non-claim")

    observed = supersession.get("observed_conditions", {})
    if observed.get("issued_receipt_count") != issued_count:
        fail("issued receipt count does not match supersession state")
    if observed.get("placeholder_receipt_count") != placeholder_count:
        fail("placeholder receipt count does not match supersession state")
    if observed.get("required_receipt_count") != len(REQUIRED_CLASSES):
        fail("required receipt count does not match review classes")

    locator = observed.get("locator_verification")
    eligible_locator = locator in {"CONFIRMED", "PARTIAL_WITH_STABLE_RETRIEVABLE_SOURCE"}
    eligible_receipts = issued_count == len(REQUIRED_CLASSES)
    result = supersession.get("evaluation_result")

    if eligible_locator and eligible_receipts:
        if result not in {"ELIGIBLE_FOR_NEW_PROMOTION_DECISION", "SUPERSEDED"}:
            fail("eligible inputs must permit a new promotion decision or record supersession")
    else:
        if result != "DEFER_NO_SUPERSESSION":
            fail("incomplete inputs must fail closed as DEFER_NO_SUPERSESSION")
        if supersession.get("supersedes_decision_id") is not None:
            fail("deferred state must not supersede the prior decision")

    boundary = str(supersession.get("authority_boundary", "")).lower()
    if "does not" not in boundary and "do not" not in boundary:
        fail("supersession authority boundary lacks explicit non-claim")

    print(
        "REVIEW RECEIPTS AND SUPERSESSION: PASS - "
        f"{len(receipts)} receipts; result={result}"
    )


if __name__ == "__main__":
    main()
