#!/usr/bin/env python3
"""Fail-closed validation for ASRO comparison ownership and contribution governance."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "docs" / "external-frameworks" / "stegverse-owner-declaration-asro-comparison.md"
PROTOCOL = ROOT / "docs" / "external-frameworks" / "asro-stegverse-comparison-contributor-protocol.md"
DECLARATION = ROOT / "static" / "data" / "framework-evaluations" / "asro" / "stegverse-companion-layer-declaration.json"
HISTORICAL_PIN = ROOT / "static" / "data" / "framework-evaluations" / "asro" / "historical-public-source-pin-2026-07-23.json"
ACCOUNTABLE = ROOT / "static" / "data" / "framework-evaluations" / "asro" / "stegverse-accountable-party-declaration.json"
LEDGER = ROOT / "static" / "data" / "framework-evaluations" / "asro" / "contribution-ledger.jsonl"

OWNER_MARKERS = [
    "entity_form: project and technical lab; no separate legal-entity status is asserted",
    "accountable_person: Rigel Randolph",
    "publication_status: UNILATERAL_STEGVERSE_DECLARATION",
    "bilateral_authorization: false",
    "The existing admissibility-wiki ASRO packet is unilateral StegVerse analysis.",
    "A future bilateral record requires exact-language authorization from both owners",
]

PROTOCOL_MARKERS = [
    "protocol_status: STEGVERSE_PROPOSED_COMPARISON_SPECIFIC_PROTOCOL",
    "bilateral_authorization: false",
    "shared_ownership_created: false",
    "future_work_guaranteed: false",
    "Private, internal, unpublished, or unreleased material may not be incorporated",
    "Any bilateral Seam Comparison Record requires exact-language authorization from both owners.",
    "This proposed protocol creates no partnership",
]

REQUIRED_INTAKE_AREAS = {
    "artifact_identity",
    "declaring_owner",
    "claimed_function",
    "explicit_non_claims",
    "timing_position",
    "authority_boundary",
    "evidence_status",
    "composition_constraints",
    "known_divergence_risks",
    "declaration_validity_and_staleness",
    "reviewer_use_limitations",
}

REQUIRED_LEDGER_FIELDS = {
    "schema",
    "entry_id",
    "date",
    "contributor",
    "source_type",
    "source_reference",
    "contribution_type",
    "originating_framework",
    "resulting_derivative",
    "attribution",
    "authorization_state",
    "later_correction",
    "authority_boundary",
}


def load_json(path: Path, label: str, errors: list[str]) -> dict | None:
    if not path.exists():
        errors.append(f"missing:{path.relative_to(ROOT)}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label}_invalid_json:{exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label}_must_be_object")
        return None
    return value


def require_markers(path: Path, markers: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing:{path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"missing_marker:{path.relative_to(ROOT)}:{marker}")


def require_false_authority(authority: dict, keys: tuple[str, ...], prefix: str, errors: list[str]) -> None:
    for key in keys:
        if authority.get(key) is not False:
            errors.append(f"{prefix}_authority_must_be_false:{key}")


def validate_declaration(errors: list[str]) -> None:
    declaration = load_json(DECLARATION, "declaration", errors)
    if declaration is None:
        return

    if declaration.get("schema_version") != "1.1.0":
        errors.append("declaration_schema_version")
    if declaration.get("declaration_revision") != 2:
        errors.append("declaration_revision")
    intake = declaration.get("intake_areas") or {}
    if set(intake) != REQUIRED_INTAKE_AREAS:
        errors.append("declaration_eleven_area_mapping")
    for name in REQUIRED_INTAKE_AREAS:
        item = intake.get(name) or {}
        if item.get("state") != "DECLARED" or not item.get("value"):
            errors.append(f"declaration_area_incomplete:{name}")

    disposition = declaration.get("review_disposition") or {}
    expected = {
        "provenance_correction": "ACCEPTED_FOR_HISTORICAL_CLASSIFICATION",
        "contributor_protocol": "DIRECTIONALLY_ACCEPTABLE_NOT_BILATERALLY_AUTHORIZED",
        "external_asro_native_execution": "NOT_TESTED",
        "reciprocal_execution": "DEFERRED",
        "independent_reviewer_issuer": "UNRESOLVED",
    }
    for key, value in expected.items():
        if disposition.get(key) != value:
            errors.append(f"declaration_disposition:{key}")

    historical = declaration.get("historical_source_binding") or {}
    if historical.get("original_2026_07_23_public_source_pin") != "PENDING":
        errors.append("historical_source_pin_must_remain_pending")
    if historical.get("later_public_source_may_substitute_backward") is not False:
        errors.append("historical_source_backward_substitution_not_blocked")

    require_false_authority(
        declaration.get("authority") or {},
        ("external_review", "certification", "execution", "custody", "bilateral_authorization"),
        "declaration",
        errors,
    )

    recorded = declaration.get("sha256")
    unsigned = dict(declaration)
    unsigned.pop("sha256", None)
    computed = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if recorded != computed:
        errors.append("declaration_sha256_mismatch")


def validate_historical_pin(errors: list[str]) -> None:
    pin = load_json(HISTORICAL_PIN, "historical_pin", errors)
    if pin is None:
        return
    if pin.get("artifact_type") != "historical_public_source_pin":
        errors.append("historical_pin_artifact_type")
    if pin.get("target_observation_date") != "2026-07-23":
        errors.append("historical_pin_target_date")
    repo = pin.get("public_repository") or {}
    if repo.get("commit_sha_at_target_date") != "46f8fd2f8f35668b2b27fcbdb4e24e06b58513a2":
        errors.append("historical_pin_repository_commit")
    if repo.get("commit_status") != "CONFIRMED_BY_PUBLIC_COMMIT_HISTORY_NO_LATER_COMMIT_BEFORE_TARGET_DATE":
        errors.append("historical_pin_commit_status")
    source_path = pin.get("source_path") or {}
    if source_path.get("value") is not None or source_path.get("status") != "UNRESOLVED_FROM_HISTORICAL_RECORD":
        errors.append("historical_pin_exact_source_path_must_remain_unresolved")
    if source_path.get("candidate_reference_status") != "PRESENT_AT_PINNED_COMMIT_NOT_RETROACTIVELY_ASSERTED_AS_THE_EXACT_PATH_OBSERVED":
        errors.append("historical_pin_candidate_path_boundary")
    if pin.get("historical_identity_status") != "REPOSITORY_COMMIT_PINNED_EXACT_SOURCE_PATH_UNRESOLVED":
        errors.append("historical_pin_identity_status")
    if pin.get("later_source_may_substitute_backward") is not False or pin.get("later_implementation_may_substitute_backward") is not False:
        errors.append("historical_pin_backward_substitution_not_blocked")
    require_false_authority(
        pin.get("authority") or {},
        ("external_review", "certification", "endorsement", "joint_issuance", "admissibility", "execution", "custody", "bilateral_authorization"),
        "historical_pin",
        errors,
    )


def validate_accountable_party(errors: list[str]) -> None:
    accountable = load_json(ACCOUNTABLE, "accountable_party", errors)
    if accountable is None:
        return
    if accountable.get("artifact_type") != "stegverse_accountable_party_declaration":
        errors.append("accountable_party_artifact_type")
    if accountable.get("declaring_entity") != "StegVerse Labs":
        errors.append("accountable_party_entity")
    if accountable.get("accountability_basis") != "ROLE" or accountable.get("accountable_role") != "Founder and Architect":
        errors.append("accountable_party_role")
    contact = accountable.get("contact_point") or {}
    for key in ("primary", "canonical_repository", "canonical_organization", "canonical_website"):
        if not contact.get(key):
            errors.append(f"accountable_party_contact:{key}")
    if accountable.get("publication_status") != "UNILATERAL_STEGVERSE_DECLARATION":
        errors.append("accountable_party_publication_status")
    non_claims = set(accountable.get("relationship_non_claims") or [])
    for required in ("no partnership", "no shared ownership", "no certification", "no joint issuance", "no authority transfer"):
        if required not in non_claims:
            errors.append(f"accountable_party_missing_non_claim:{required}")
    authority = accountable.get("authority") or {}
    if authority.get("self_declaration") is not True:
        errors.append("accountable_party_self_declaration")
    require_false_authority(
        authority,
        ("external_review", "certification", "execution", "custody_transfer", "bilateral_authorization", "authority_over_external_materials"),
        "accountable_party",
        errors,
    )
    if accountable.get("external_identity_policy") != "No external individual identity is asserted by this machine-readable declaration.":
        errors.append("accountable_party_external_identity_policy")


def validate_ledger(errors: list[str]) -> None:
    if not LEDGER.exists():
        errors.append(f"missing:{LEDGER.relative_to(ROOT)}")
        return

    entries = []
    for line_number, line in enumerate(LEDGER.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"ledger_invalid_json_line_{line_number}:{exc}")
            continue
        missing = REQUIRED_LEDGER_FIELDS - set(entry)
        if missing:
            errors.append(f"ledger_missing_fields_line_{line_number}:{','.join(sorted(missing))}")
        if entry.get("schema") != "asro_stegverse.contribution_ledger_entry.v1":
            errors.append(f"ledger_schema_line_{line_number}")
        boundary = str(entry.get("authority_boundary", "")).lower()
        if not any(term in boundary for term in ("does not", "non-authorizing", "no ")):
            errors.append(f"ledger_authority_boundary_line_{line_number}")
        entries.append(entry)

    ids = [entry.get("entry_id") for entry in entries]
    if len(ids) != len(set(ids)):
        errors.append("ledger_duplicate_entry_id")
    dates = [str(entry.get("date")) for entry in entries]
    if dates != sorted(dates):
        errors.append("ledger_not_append_chronological")
    if not any(date.startswith("2026-05-06") for date in dates):
        errors.append("ledger_missing_may_6_origin")
    if not any(entry.get("contribution_type") == "provenance-correction" for entry in entries):
        errors.append("ledger_missing_provenance_correction")

    expected_entries = {
        "asro-sv-ledger-2026-08-16-001": "PROTOCOL_DIRECTIONALLY_ACCEPTABLE_NOT_BILATERALLY_AUTHORIZED",
        "asro-sv-ledger-2026-08-18-001": "EXACT_HISTORICAL_SOURCE_PATH_UNRESOLVED",
        "asro-sv-ledger-2026-08-18-002": "BILATERAL_AUTHORIZATION_FALSE",
    }
    by_id = {entry.get("entry_id"): entry for entry in entries}
    for entry_id, marker in expected_entries.items():
        entry = by_id.get(entry_id)
        if entry is None:
            errors.append(f"ledger_missing_required_entry:{entry_id}")
        elif marker not in str(entry.get("authorization_state")):
            errors.append(f"ledger_required_authorization_state:{entry_id}")


def main() -> int:
    errors: list[str] = []
    require_markers(OWNER, OWNER_MARKERS, errors)
    require_markers(PROTOCOL, PROTOCOL_MARKERS, errors)
    validate_declaration(errors)
    validate_historical_pin(errors)
    validate_accountable_party(errors)
    validate_ledger(errors)

    if errors:
        print("ASRO COMPARISON GOVERNANCE: FAIL - " + ", ".join(errors))
        return 1

    print("ASRO COMPARISON GOVERNANCE: PASS")
    print("Owner, eleven-area declaration, bounded historical pin, accountable-party declaration, proposed protocol, and append-only ledger preserve evidence and authority boundaries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
