#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_BASE = ROOT / "static" / "data" / "framework-evaluations"
BASE = REGISTRY_BASE / "asro"
DOC = ROOT / "docs" / "external-frameworks" / "asro.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    declaration = load(BASE / "stegverse-companion-layer-declaration.json")
    representative = load(BASE / "asro-author-provided-bounded-representative-object.json")
    reviewer = load(BASE / "reviewer-profile.json")
    manifest = load(BASE / "correspondence-manifest.json")
    expected = load(BASE / "expected-results.json")
    framework = load(REGISTRY_BASE / "asro.json")
    registry = load(REGISTRY_BASE / "index.json")
    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""

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
    forbidden = (
        "truth_established",
        "sufficiency_established",
        "validity_established",
        "admissibility_established",
        "authority_inherited",
    )
    for field in forbidden:
        if determination.get(field) is not False:
            failures.append(f"correspondence improperly establishes {field}")

    expected_result = expected.get("expected", {})
    if expected_result.get("collection_membership") != "ESTABLISHED":
        failures.append("expected fixture must require established collection membership")
    for field in ("object_identity_bound", "version_bound", "hash_bound", "applicable_time_bound"):
        if expected_result.get(field) is not True:
            failures.append(f"expected fixture must require {field}")
    for field in (
        "label_only_match_accepted",
        "truth_established",
        "sufficiency_established",
        "validity_established",
        "admissibility_established",
        "authority_inherited",
        "execution_authority_granted",
        "custody_transferred",
    ):
        if expected_result.get(field) is not False:
            failures.append(f"expected fixture must reject {field}")

    if framework.get("framework", {}).get("framework_id") != "asro":
        failures.append("ASRO framework record missing framework_id")
    if framework.get("test_runs") != []:
        failures.append("ASRO framework record must remain NOT_TESTED until execution records exist")
    if framework.get("publication", {}).get("projection_authority") != "NONE":
        failures.append("ASRO framework projection authority must remain NONE")

    asro_entries = [item for item in registry.get("frameworks", []) if item.get("framework_id") == "asro"]
    if len(asro_entries) != 1:
        failures.append("framework registry must contain exactly one ASRO entry")
    else:
        entry = asro_entries[0]
        if entry.get("canonical_schema_status") != "NOT_ASSERTED":
            failures.append("registry must not assert a canonical ASRO schema")
        if entry.get("reviewer_issuer_status") != "UNRESOLVED":
            failures.append("registry reviewer issuer must remain unresolved")
        if entry.get("live_test_status") != "NOT_TESTED":
            failures.append("registry live test must remain NOT_TESTED")

    for marker in (
        "correspondence != admissibility",
        "correspondence != authority inheritance",
        "issuer: unresolved",
        "ASRO-author-provided bounded representative object",
    ):
        if marker not in doc_text:
            failures.append(f"ASRO documentation missing marker: {marker}")

    if failures:
        print("ASRO BOUNDED COMPARISON: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO BOUNDED COMPARISON: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
