#!/usr/bin/env python3
"""Validate the bounded Admissible Resolution ingestion receipt."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "static/status/admissible-resolution-ingestion-receipt.json"
EXPECTED_IDS = ["T-060", "T-061", "T-062", "T-063", "T-064", "T-065"]
EXPECTED_FALSE_AUTHORITY = (
    "publication_authorized",
    "release_authorized",
    "execution_authorized",
    "custody_recorded",
    "certification_authority_created",
    "admissibility_determined",
    "standing_created",
)


def fail(message: str) -> int:
    print(f"ADMISSIBLE RESOLUTION INGESTION: FAIL - {message}")
    return 1


def main() -> int:
    if not RECEIPT.exists():
        return fail("receipt missing")

    try:
        data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"receipt unreadable: {exc}")

    expected = {
        "state_type": "admissible_resolution_ingestion_receipt",
        "destination_repository": "StegVerse-Labs/admissibility-wiki",
        "source_repository": "Admissible-Existence/TT",
        "decision_id": "AR-CHAIN-001",
        "classification": "BOUNDED_FORMALISM_INGESTION_VERIFIED",
        "public_projection_state": "NOT_YET_PROJECTED",
        "manual_user_action_required": False,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            return fail(f"{key} mismatch")

    packet = data.get("source_packet", {})
    if packet.get("canonical_sha256") != "sha256:d01f86e79a0370035091c6472986186a4e2ce7c5304976b597fcef8a14da8bd6":
        return fail("source packet hash mismatch")
    if packet.get("state") != "READY_FOR_DESTINATION_HANDOFF_REVIEW":
        return fail("source packet state mismatch")

    registry = data.get("registry", {})
    if registry.get("family") != "Resolution":
        return fail("registry family mismatch")
    if registry.get("transition_ids") != EXPECTED_IDS:
        return fail("transition identifiers mismatch")
    if registry.get("expected_total_transition_elements") != 76:
        return fail("registry total mismatch")

    chain = data.get("verified_chain", {})
    if chain.get("required_nodes") != 6 or chain.get("allocated_nodes") != 6:
        return fail("node allocation mismatch")
    if chain.get("result") != "RESOLUTION_SATISFIED":
        return fail("resolution result mismatch")

    for field in (
        "canonical_input_hash",
        "source_resolution_receipt_hash",
        "factory_validation_receipt_hash",
        "tt_allocation_receipt_hash",
    ):
        value = chain.get(field)
        if not isinstance(value, str) or not value.startswith("sha256:") or len(value) != 71:
            return fail(f"invalid {field}")

    for required_true in (
        "reciprocal_review_required",
        "dispute_and_correction_path_required",
        "time_t_reconstruction_required",
    ):
        if data.get(required_true) is not True:
            return fail(f"{required_true} must be true")

    authority = data.get("authority", {})
    for field in EXPECTED_FALSE_AUTHORITY:
        if authority.get(field) is not False:
            return fail(f"authority escalation: {field}")

    print(
        "ADMISSIBLE RESOLUTION INGESTION: PASS - packet identity, registry, receipt chain, "
        "bounded review posture, and false authority fields verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
