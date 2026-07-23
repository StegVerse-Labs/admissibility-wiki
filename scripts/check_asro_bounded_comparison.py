#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "static" / "data" / "framework-evaluations" / "asro"


def load(name: str) -> dict:
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    declaration = load("stegverse-companion-layer-declaration.json")
    representative = load("asro-author-provided-bounded-representative-object.json")
    reviewer = load("reviewer-profile.json")
    manifest = load("correspondence-manifest.json")

    if declaration.get("canonical_status") != "CONTROLLING_SOURCE_DECLARATION":
        failures.append("StegVerse declaration is not controlling")
    if representative.get("canonical_status") != "NON_CANONICAL":
        failures.append("ASRO representative object must remain non-canonical")
    if representative.get("released_asro_native_schema") is not False:
        failures.append("representative object must not be presented as a released ASRO-native schema")
    if reviewer.get("issuer") != "unresolved":
        failures.append("reviewer issuer must remain unresolved until designation")
    if reviewer.get("provenance", {}).get("derivation_status") != "DERIVATIVE":
        failures.append("reviewer profile must remain derivative")
    membership = manifest.get("collection_membership", {})
    reference = membership.get("declared_reference", {})
    for field in ("object_id", "version", "sha256", "applicable_time"):
        if not reference.get(field):
            failures.append(f"declared reference missing {field}")
    if membership.get("label_only_match_sufficient") is not False:
        failures.append("label-only matching must be rejected")
    determination = manifest.get("determination", {})
    for field in ("truth_established", "sufficiency_established", "validity_established", "admissibility_established", "authority_inherited"):
        if determination.get(field) is not False:
            failures.append(f"correspondence improperly establishes {field}")

    if failures:
        print("ASRO BOUNDED COMPARISON: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO BOUNDED COMPARISON: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
