#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHAIN_PATH = ROOT / "tests" / "fixtures" / "external-framework-runtime-dispatch-observation-chain.json"
EXPECTED_STATES = ["NOT_DISPATCHED", "DISPATCH_ATTEMPTED", "DISPATCHED", "EXECUTION_OBSERVED"]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha256(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    failures: list[str] = []
    if not CHAIN_PATH.exists():
        print("EXTERNAL FRAMEWORK RUNTIME DISPATCH PROGRESSION: FAIL")
        print(f"- missing {CHAIN_PATH.relative_to(ROOT)}")
        return 1

    chain = load(CHAIN_PATH)
    if chain.get("chain_type") != "external_framework_runtime_dispatch_observation_chain":
        failures.append("chain_type mismatch")
    if chain.get("hash_algorithm") != "sha256-canonical-json":
        failures.append("hash_algorithm must be sha256-canonical-json")
    if chain.get("state_order") != EXPECTED_STATES:
        failures.append("state_order must match canonical dispatch progression")

    entries = chain.get("entries")
    if not isinstance(entries, list) or len(entries) != len(EXPECTED_STATES):
        failures.append("entries must contain exactly four progression states")
        entries = []

    previous_entry: dict[str, Any] | None = None
    previous_receipt: dict[str, Any] | None = None
    previous_time: datetime | None = None

    for index, entry in enumerate(entries):
        label = f"entry[{index}]"
        if entry.get("sequence") != index:
            failures.append(f"{label}: sequence mismatch")
        if entry.get("state") != EXPECTED_STATES[index]:
            failures.append(f"{label}: state mismatch")

        path_value = entry.get("receipt_path")
        if not isinstance(path_value, str) or not path_value:
            failures.append(f"{label}: receipt_path required")
            continue
        receipt_path = ROOT / path_value
        if not receipt_path.exists():
            failures.append(f"{label}: missing receipt {path_value}")
            continue

        receipt = load(receipt_path)
        actual_hash = canonical_sha256(receipt)
        if entry.get("receipt_sha256") != actual_hash:
            failures.append(f"{label}: receipt_sha256 does not match canonical receipt")
        if entry.get("receipt_id") != receipt.get("receipt_id"):
            failures.append(f"{label}: receipt_id mismatch")
        if entry.get("state") != receipt.get("dispatch_state"):
            failures.append(f"{label}: receipt dispatch_state mismatch")
        if receipt.get("framework_id") != chain.get("framework_id"):
            failures.append(f"{label}: framework_id drift")
        if receipt.get("authorized_transition_id") != chain.get("authorized_transition_id"):
            failures.append(f"{label}: authorized_transition_id drift")

        observed_at = receipt.get("observation", {}).get("observed_at")
        if not isinstance(observed_at, str):
            failures.append(f"{label}: observed_at required")
        else:
            try:
                current_time = parse_time(observed_at)
                if previous_time is not None and current_time <= previous_time:
                    failures.append(f"{label}: observed_at must strictly increase")
                previous_time = current_time
            except ValueError:
                failures.append(f"{label}: invalid observed_at")

        if previous_entry is None:
            if entry.get("previous_receipt_id") is not None or entry.get("previous_receipt_sha256") is not None:
                failures.append(f"{label}: genesis entry must not reference a predecessor")
        else:
            if entry.get("previous_receipt_id") != previous_entry.get("receipt_id"):
                failures.append(f"{label}: previous_receipt_id mismatch")
            if entry.get("previous_receipt_sha256") != previous_entry.get("receipt_sha256"):
                failures.append(f"{label}: previous_receipt_sha256 mismatch")
            if previous_receipt is not None:
                previous_attempt = previous_receipt.get("observation", {}).get("dispatch_attempt_id")
                current_attempt = receipt.get("observation", {}).get("dispatch_attempt_id")
                if index >= 2 and previous_attempt and current_attempt == previous_attempt:
                    failures.append(f"{label}: fixture progression must not reuse a synthetic attempt id as proof of continuity")

        previous_entry = entry
        previous_receipt = receipt

    boundary = chain.get("authority_boundary", {})
    for key in (
        "chain_validation_may_initiate_dispatch",
        "chain_validation_may_execute",
        "chain_progression_is_observed_production_execution",
        "fixture_chain_may_create_external_consequence",
    ):
        if boundary.get(key) is not False:
            failures.append(f"authority boundary must remain false: {key}")

    print("EXTERNAL FRAMEWORK RUNTIME DISPATCH PROGRESSION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
