#!/usr/bin/env python3
"""Fail-closed validation of the wiki's Admissible Resolution upstream continuity record."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/status/admissible-resolution-upstream-continuity.json"
LOCAL_RECEIPT = ROOT / "static/status/admissible-resolution-ingestion-receipt.json"

EXPECTED_FALSE = (
    "publication_authorized",
    "release_authorized",
    "execution_authorized",
    "custody_recorded",
    "certification_authority_created",
    "admissibility_determined",
    "standing_created",
    "cross_repository_mutation_authorized",
)


def fail(message: str) -> int:
    print(f"ADMISSIBLE RESOLUTION UPSTREAM CONTINUITY: FAIL - {message}")
    return 1


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if not STATUS.exists() or not LOCAL_RECEIPT.exists():
        return fail("required status or local receipt missing")
    try:
        data = load(STATUS)
        receipt = load(LOCAL_RECEIPT)
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"record unreadable: {exc}")

    if data.get("state_type") != "admissible_resolution_upstream_continuity":
        return fail("state_type mismatch")
    if data.get("destination_repository") != "StegVerse-Labs/admissibility-wiki":
        return fail("destination mismatch")
    if data.get("decision_id") != receipt.get("decision_id") or data.get("decision_id") != "AR-CHAIN-001":
        return fail("decision continuity mismatch")
    if data.get("local_receipt_path") != "static/status/admissible-resolution-ingestion-receipt.json":
        return fail("local receipt path mismatch")

    upstream = data.get("upstream", {})
    expected = {
        "formal_owner": ("Admissible-Existence/AE", "d8dae4892c4d8d916984c4924908c585ab2b1ccc"),
        "validation_factory": ("Admissible-Existence/ae-validation-factory", "c8350329857bb95dcf70b466a3c022ed1e1a9286"),
        "operational_owner": ("Admissible-Existence/TT", "e3d2c4ab1246393f67954ee638f9db19ec13e5e1"),
    }
    for key, (repository, commit) in expected.items():
        record = upstream.get(key, {})
        if record.get("repository") != repository:
            return fail(f"{key} repository mismatch")
        commit_value = record.get("merged_commit", record.get("merged_destination_ledger_commit"))
        if commit_value != commit:
            return fail(f"{key} commit mismatch")
        if record.get("validation_state") != "HOSTED_VALIDATED":
            return fail(f"{key} validation not hosted-validated")

    local = data.get("local_state", {})
    required_true = (
        "bounded_ingestion_receipt_present",
        "local_checker_bound_to_canonical_aggregate",
        "upstream_continuity_verified",
    )
    for field in required_true:
        if local.get(field) is not True:
            return fail(f"{field} must be true")
    if local.get("public_projection_state") != "NOT_YET_PROJECTED":
        return fail("public projection posture mismatch")
    for field in (
        "site_activation_dependency_satisfied",
        "guardian_propagation_authorized",
        "repository_wide_canonical_pass_observed_for_this_record",
    ):
        if local.get(field) is not False:
            return fail(f"premature completion claim: {field}")

    authority = data.get("authority", {})
    for field in EXPECTED_FALSE:
        if authority.get(field) is not False:
            return fail(f"authority escalation: {field}")
    if data.get("manual_user_action_required") is not False:
        return fail("manual user action must remain false")
    if data.get("archive_readiness") is not False:
        return fail("archive readiness must remain false")

    print(
        "ADMISSIBLE RESOLUTION UPSTREAM CONTINUITY: PASS - AE, Factory, and TT hosted evidence "
        "bound to local bounded receipt with Site, Guardian, authority, and archive gates fail-closed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
