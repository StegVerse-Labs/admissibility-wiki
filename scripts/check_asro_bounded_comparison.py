#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_BASE = ROOT / "static" / "data" / "framework-evaluations"
BASE = REGISTRY_BASE / "asro"
DOC = ROOT / "docs" / "external-frameworks" / "asro.md"
DERIVATIVE = BASE / "stegverse-generated-bounded-metadata-derivative.json"
DEPRECATED_ALIAS = BASE / "asro-author-provided-bounded-representative-object.json"
DEPENDENT_VALIDATORS = [
    ROOT / "scripts" / "check_asro_provenance_correction.py",
    ROOT / "scripts" / "check_asro_comparison_governance.py",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_validator(path: Path) -> tuple[int, str]:
    if not path.exists():
        return 127, f"missing validator: {path.relative_to(ROOT)}"
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.rstrip()


def main() -> int:
    failures: list[str] = []
    declaration = load(BASE / "stegverse-companion-layer-declaration.json")
    derivative = load(DERIVATIVE)
    deprecated_alias = load(DEPRECATED_ALIAS)
    reviewer = load(BASE / "reviewer-profile.json")
    manifest = load(BASE / "correspondence-manifest.json")
    expected = load(BASE / "expected-results.json")
    framework = load(REGISTRY_BASE / "asro.json")
    registry = load(REGISTRY_BASE / "index.json")
    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""

    if declaration.get("canonical_status") != "CONTROLLING_SOURCE_DECLARATION":
        failures.append("StegVerse declaration is not controlling")

    if derivative.get("artifact_type") != "stegverse_generated_bounded_metadata_derivative":
        failures.append("public comparison object must be classified as a StegVerse-generated derivative")
    if derivative.get("creator") != "StegVerse Labs":
        failures.append("public derivative creator must be StegVerse Labs")
    source = derivative.get("source_provenance", {})
    if source.get("source_provider") != "James Aull / ASRO":
        failures.append("underlying source provider attribution is missing")
    if source.get("source_example_publicly_reproduced") is not False:
        failures.append("underlying source example must not be represented as publicly reproduced")
    if source.get("source_input_content_hash") is not None:
        failures.append("source-input hash must remain unset until mutually bound")
    if source.get("source_linkage_status") != "UNRESOLVED":
        failures.append("source linkage must remain unresolved until mutually approved")
    if derivative.get("canonical_status") != "NON_CANONICAL":
        failures.append("StegVerse derivative must remain non-canonical")
    if derivative.get("released_asro_native_schema") is not False:
        failures.append("derivative must not be presented as a released ASRO-native schema")

    if deprecated_alias.get("status") != "DEPRECATED_PROVENANCE_ALIAS":
        failures.append("historical misleading path must remain a deprecated provenance alias")
    if deprecated_alias.get("replacement_path") != str(DERIVATIVE.relative_to(ROOT)):
        failures.append("deprecated alias must point to the corrected derivative")

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

    expected_result = expected.get("expected", {})
    if expected_result.get("collection_membership") != "ESTABLISHED":
        failures.append("expected fixture must require established collection membership")
    for field in ("object_identity_bound", "version_bound", "hash_bound", "applicable_time_bound"):
        if expected_result.get(field) is not True:
            failures.append(f"expected fixture must require {field}")
    for field in ("label_only_match_accepted", "truth_established", "sufficiency_established", "validity_established", "admissibility_established", "authority_inherited", "execution_authority_granted", "custody_transferred"):
        if expected_result.get(field) is not False:
            failures.append(f"expected fixture must reject {field}")

    if framework.get("framework", {}).get("framework_id") != "asro":
        failures.append("ASRO framework record missing framework_id")
    runs = framework.get("test_runs", [])
    if len(runs) != 1 or runs[0].get("result") != "PASS":
        failures.append("ASRO framework record must contain exactly one passing StegVerse run")
    elif runs[0].get("admissibility") not in (None, "NOT_EVALUATED"):
        failures.append("ASRO bounded run must not establish admissibility")
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
        if entry.get("live_test_status") != "STEGVERSE_RUN_PASS_EXTERNAL_NOT_TESTED":
            failures.append("registry must distinguish StegVerse run PASS from external ASRO execution")

    for marker in ("correspondence != admissibility", "correspondence != authority inheritance", "issuer: unresolved", "ASRO-author-provided bounded representative object"):
        if marker not in doc_text:
            failures.append(f"ASRO documentation missing marker: {marker}")

    for validator in DEPENDENT_VALIDATORS:
        code, output = run_validator(validator)
        if output:
            print(output)
        if code != 0:
            failures.append(f"dependent validator failed: {validator.relative_to(ROOT)}")

    if failures:
        print("ASRO BOUNDED COMPARISON: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO BOUNDED COMPARISON: PASS")
    print("Source/derivative provenance, owner declaration, contributor protocol, and append-only ledger remain fail-closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
