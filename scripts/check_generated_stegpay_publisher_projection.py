#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "static/status/generated-stegpay-publisher-projection.json"
EXPECTED_PUBLISHER_HASH = "bbae4456bb09de7eaa3b9782c000fdef106ad035c1f2dee64f62e4102df302a1"
EXPECTED_SITE_HASH = "687d06eb93693d0bd78f00cdefd465d23d92b54c0bbfa7bc0a04b1364f9a452f"
EXPECTED_PROPAGATION_HASH = "e59e71bf31879f0bf29a8356f8027304a94a4dee59d3c0be35c3ecc505e7cec9"
EXPECTED_CONSUMER_RECEIPT_HASH = "b8084ecc9821eb7738e4dccffd239185a072e0bc630e71c72906098a830cf515"
EXPECTED_GENERATED_UTC = "2026-08-27T11:58:18Z"
EXPECTED_EVENT_ID = "09373107-5e4b-483e-85de-9e26c126fc0c"


def fail(message: str) -> None:
    raise SystemExit(f"GENERATED STEGPAY ADMISSIBILITY PROJECTION: FAIL: {message}")


def main() -> int:
    if not PATH.exists():
        fail(f"missing {PATH.relative_to(ROOT)}")
    value = json.loads(PATH.read_text(encoding="utf-8"))
    checks = {
        "source repository": value.get("source_repository") == "GCAT-BCAT-Engine/Publisher",
        "source path": value.get("source_path") == "data/generated-stegpay-site-ingestion.json",
        "source generation": value.get("source_generated_utc") == EXPECTED_GENERATED_UTC,
        "publisher projection hash": value.get("publisher_projection_hash_sha256") == EXPECTED_PUBLISHER_HASH,
        "site receipt hash": value.get("site_receipt_hash_sha256") == EXPECTED_SITE_HASH,
        "propagation hash": value.get("propagation_hash_sha256") == EXPECTED_PROPAGATION_HASH,
        "consumer receipt hash": value.get("consumer_receipt_hash_sha256") == EXPECTED_CONSUMER_RECEIPT_HASH,
        "event id": value.get("event_id") == EXPECTED_EVENT_ID,
        "state": value.get("state") == "BOUNDED_TEST_EVIDENCE_IMPORTED",
        "determination": value.get("determination") == "VERIFIED_TEST_TRANSPORT_AND_CONSUMPTION_ONLY",
        "test only": value.get("test_only") is True,
    }
    false_fields = [
        "admissibility_determination_granted",
        "publication_authorized",
        "release_authorized",
        "execution_authorized",
        "custody_recorded",
        "payment_is_entitlement",
        "transport_is_authority",
    ]
    for field in false_fields:
        checks[field] = value.get(field) is False
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        fail(", ".join(failed))
    print("GENERATED_STEGPAY_ADMISSIBILITY_IMPORT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
