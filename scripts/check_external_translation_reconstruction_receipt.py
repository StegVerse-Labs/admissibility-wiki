#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "external-translation" / "reconstruction-receipt.json"


def canonical_sha256(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"EXTERNAL TRANSLATION RECONSTRUCTION RECEIPT: FAIL - {message}")


def main() -> None:
    if not REPORT.exists():
        fail(f"missing generated receipt: {REPORT.relative_to(ROOT)}")

    receipt = json.loads(REPORT.read_text(encoding="utf-8"))
    if receipt.get("schema") != "admissibility_wiki.external_translation_reconstruction_receipt.v1":
        fail("unexpected schema")
    if receipt.get("overall_status") != "PASS":
        fail(f"overall_status is {receipt.get('overall_status')}")

    checks = receipt.get("cross_record_checks")
    if not isinstance(checks, dict) or not checks:
        fail("cross_record_checks must be a non-empty object")
    failed = sorted(name for name, value in checks.items() if value is not True)
    if failed:
        fail(f"failed cross-record checks: {failed}")

    hashes = receipt.get("input_hashes")
    if not isinstance(hashes, dict) or not hashes:
        fail("input_hashes must be a non-empty object")
    for name, record in hashes.items():
        path_value = record.get("path")
        digest = record.get("canonical_json_sha256")
        if not isinstance(path_value, str) or not path_value:
            fail(f"{name} has no input path")
        path = ROOT / path_value
        if not path.exists():
            fail(f"{name} input is missing: {path_value}")
        actual = canonical_sha256(path)
        if digest != actual:
            fail(f"{name} hash mismatch")

    review_receipts = receipt.get("review_receipts")
    if not isinstance(review_receipts, list) or len(review_receipts) != 3:
        fail("exactly three review receipt summaries are required")

    supersession = receipt.get("supersession", {})
    if receipt.get("locator_verification") == "UNRESOLVED":
        if supersession.get("evaluation_result") != "DEFER_NO_SUPERSESSION":
            fail("unresolved locator must remain DEFER_NO_SUPERSESSION")
        if supersession.get("supersedes_decision_id") is not None:
            fail("unresolved locator must not supersede a decision")

    continuation = receipt.get("continuation", {})
    for key in ("owner", "next_event", "permitted_scope"):
        if not isinstance(continuation.get(key), str) or not continuation[key].strip():
            fail(f"continuation.{key} must be a non-empty string")

    boundary = str(receipt.get("authority_boundary", "")).lower()
    if "does not" not in boundary and "do not" not in boundary:
        fail("authority boundary lacks an explicit non-claim")

    print(
        "EXTERNAL TRANSLATION RECONSTRUCTION RECEIPT: PASS - "
        f"{len(hashes)} inputs and {len(checks)} cross-record checks verified"
    )


if __name__ == "__main__":
    main()
