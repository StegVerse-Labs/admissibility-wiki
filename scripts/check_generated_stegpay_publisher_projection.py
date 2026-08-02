#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "static/status/generated-stegpay-publisher-projection.json"
EXPECTED_PUBLISHER_HASH = "29366d3597dd98b868a46efbcb4ba32bd8a750e1a684ed382775a657e5bfc66a"
EXPECTED_SITE_HASH = "45e8e8849f6d0967de66da6bc45f874c33fcea703a80ba165f45ffa6fecd81d1"
EXPECTED_PROPAGATION_HASH = "aecfd09a016e1daaa32b66f0e7aa2bc2681edc70be14f25637fa95df2a1468e3"
EXPECTED_EVENT_ID = "09373107-5e4b-483e-85de-9e26c126fc0c"


def fail(message: str) -> None:
    raise SystemExit(f"GENERATED STEGPAY ADMISSIBILITY PROJECTION: FAIL: {message}")


def main() -> int:
    if not PATH.exists():
        fail(f"missing {PATH.relative_to(ROOT)}")
    value = json.loads(PATH.read_text(encoding="utf-8"))
    checks = {
        "publisher projection hash": value.get("publisher_projection_hash_sha256") == EXPECTED_PUBLISHER_HASH,
        "site receipt hash": value.get("site_receipt_hash_sha256") == EXPECTED_SITE_HASH,
        "propagation hash": value.get("propagation_hash_sha256") == EXPECTED_PROPAGATION_HASH,
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
