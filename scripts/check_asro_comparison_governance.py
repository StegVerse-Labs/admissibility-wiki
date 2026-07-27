#!/usr/bin/env python3
"""Fail-closed validation for ASRO comparison ownership and contribution governance."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "docs" / "external-frameworks" / "stegverse-owner-declaration-asro-comparison.md"
PROTOCOL = ROOT / "docs" / "external-frameworks" / "asro-stegverse-comparison-contributor-protocol.md"
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


def require_markers(path: Path, markers: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing:{path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"missing_marker:{path.relative_to(ROOT)}:{marker}")


def main() -> int:
    errors: list[str] = []
    require_markers(OWNER, OWNER_MARKERS, errors)
    require_markers(PROTOCOL, PROTOCOL_MARKERS, errors)

    if not LEDGER.exists():
        errors.append(f"missing:{LEDGER.relative_to(ROOT)}")
    else:
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

    if errors:
        print("ASRO COMPARISON GOVERNANCE: FAIL - " + ", ".join(errors))
        return 1

    print("ASRO COMPARISON GOVERNANCE: PASS")
    print("Owner declaration, proposed contributor protocol, and append-only ledger preserve unilateral and bilateral boundaries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
