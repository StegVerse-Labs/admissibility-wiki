#!/usr/bin/env python3
"""Validate the first bounded local execution receipt for the synthetic ITC test."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "static/status/conectrr-itc-synthetic-local-execution-receipt.v1.json"
EXPECTED_HASH = "216b7596ce5f675884edfd973a126df283450d799c7a680a68eb3d45b6a99f50"
EXPECTED_DISPOSITIONS = {"AGREE", "DISAGREE", "DEFER"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_false_authority(value: Any) -> None:
    if not isinstance(value, dict):
        fail("authority object required")
    for field in ("certification", "execution", "custody", "endorsement"):
        if value.get(field) is not False:
            fail(f"authority.{field} must remain false")


def main() -> int:
    if not RECEIPT.is_file():
        fail(f"missing receipt: {RECEIPT.relative_to(ROOT)}")
    doc = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if doc.get("schema") != "conectrr_itc_synthetic_local_execution_receipt.v1":
        fail("unexpected local execution receipt schema")
    if doc.get("test_id") != "conectrr-itc-synthetic-capability-smoke-test":
        fail("unexpected synthetic test id")
    if doc.get("execution_class") != "BOUNDED_LOCAL_NONCANONICAL":
        fail("local receipt must remain explicitly noncanonical")
    if doc.get("result") != "PASS" or doc.get("replay") != "PASS":
        fail("local synthetic execution and replay must be PASS")
    before = doc.get("source_hash_before")
    after = doc.get("source_hash_after")
    if not isinstance(before, str) or not SHA256_RE.fullmatch(before):
        fail("invalid source_hash_before")
    if not isinstance(after, str) or not SHA256_RE.fullmatch(after):
        fail("invalid source_hash_after")
    if before != EXPECTED_HASH or after != EXPECTED_HASH or before != after:
        fail("local receipt hash does not match the executed synthetic fixture")
    if doc.get("hashes_match") is not True:
        fail("hashes_match must be true")
    if set(doc.get("dispositions", [])) != EXPECTED_DISPOSITIONS:
        fail("AGREE, DISAGREE, and DEFER are required")
    if doc.get("drift_cases_exercised") != 10:
        fail("all ten drift cases must be exercised")
    if doc.get("authority_effect") != "NONE":
        fail("authority effect must remain NONE")
    if doc.get("external_validation_claimed") is not False:
        fail("local execution cannot claim external validation")
    if doc.get("canonical_workflow_observed") is not False:
        fail("local execution cannot claim canonical workflow observation")
    if doc.get("canonical_result") != "NOT_YET_OBSERVED":
        fail("canonical result must remain unobserved")
    require_false_authority(doc.get("authority"))
    non_claims = "\n".join(str(item) for item in doc.get("non_claims", []))
    for marker in (
        "not a canonical GitHub Actions workflow receipt",
        "not Conectrr interoperability",
        "not external validation",
        "bounded synthetic source immutability only",
        "does not establish reviewer standing",
    ):
        if marker not in non_claims:
            fail(f"missing non-claim marker: {marker}")
    print(f"OK: {RECEIPT.relative_to(ROOT)}")
    print("conectrr_itc_synthetic_local_execution=PASS")
    print(f"synthetic_source_hash={before}")
    print("canonical_workflow_observed=false")
    print("external_validation_claimed=false")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
