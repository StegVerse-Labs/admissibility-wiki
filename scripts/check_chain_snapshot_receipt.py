#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "CHAIN_SNAPSHOT_RECEIPT_v0_1_0.json"

REQUIRED_FILES = [
    "snapshot",
    "continuation_manifest",
    "continuation_schema",
    "validator",
    "workflow_mirror",
    "workflow_manifest",
    "blocked_destination_manifest",
]

REQUIRED_BOUNDARIES = [
    "snapshot_is_release_tag",
    "snapshot_is_activation_evidence",
    "workflow_mirror_is_ci_activation",
    "no_activation_claim",
    "no_closure_claim",
    "no_adoption_claim",
    "no_endorsement_claim",
    "no_consequence_binding_standing_claim",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    if not RECEIPT.exists():
        print("CHAIN SNAPSHOT RECEIPT: FAIL")
        print("- missing receipt")
        return 1

    receipt = load_json(RECEIPT)

    if receipt.get("artifact_type") != "chain_snapshot_receipt":
        failures.append("artifact type mismatch")
    if receipt.get("status") != "BLOCKED_ON_DESTINATION_REPOSITORY":
        failures.append("status mismatch")
    if receipt.get("expected_validation_result") != "CHAIN CONTINUATION: PASS":
        failures.append("expected validation mismatch")

    for key in REQUIRED_FILES:
        value = receipt.get(key)
        if not isinstance(value, str):
            failures.append(f"missing file reference: {key}")
        elif not (ROOT / value).exists():
            failures.append(f"referenced file missing: {value}")

    boundary = receipt.get("boundary", {})
    for key in REQUIRED_BOUNDARIES:
        if key not in boundary:
            failures.append(f"missing boundary: {key}")
    if boundary.get("snapshot_is_release_tag") is not False:
        failures.append("snapshot release-tag boundary mismatch")
    if boundary.get("snapshot_is_activation_evidence") is not False:
        failures.append("snapshot activation boundary mismatch")
    if boundary.get("workflow_mirror_is_ci_activation") is not False:
        failures.append("workflow mirror boundary mismatch")
    for key in REQUIRED_BOUNDARIES[3:]:
        if boundary.get(key) is not True:
            failures.append(f"non-claim not enforced: {key}")

    print("CHAIN SNAPSHOT RECEIPT:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
