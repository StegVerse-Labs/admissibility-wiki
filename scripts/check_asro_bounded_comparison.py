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
SOURCE_OBSERVATION = BASE / "public-source-observation-2026-07-26.json"
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
    source_observation = load(SOURCE_OBSERVATION)
    reviewer = load(BASE / "reviewer-profile.json")
    manifest = load(BASE / "correspondence-manifest.json")
    framework = load(REGISTRY_BASE / "asro.json")
    registry = load(REGISTRY_BASE / "index.json")
    doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""

    if declaration.get("canonical_status") != "CONTROLLING_SOURCE_DECLARATION":
        failures.append("StegVerse declaration is not controlling")

    if derivative.get("artifact_type") != "stegverse_generated_bounded_metadata_derivative":
        failures.append("public comparison object must be a StegVerse-generated derivative")
    if derivative.get("creator") != "StegVerse Labs":
        failures.append("public derivative creator must be StegVerse Labs")
    source = derivative.get("source_example", {})
    if derivative.get("source_provider") != "James Aull / ASRO™":
        failures.append("underlying source provider attribution is missing")
    if source.get("publicly_reproduced") is not False:
        failures.append("underlying source example must not be represented as publicly reproduced")
    if source.get("content_hash_recorded") is not False:
        failures.append("source-input hash must remain unset until mutually bound")
    if not str(source.get("source_linkage_status", "")).startswith("UNRESOLVED"):
        failures.append("source linkage must remain unresolved until mutually approved")
    if derivative.get("canonical_status") != "NON_CANONICAL":
        failures.append("StegVerse derivative must remain non-canonical")
    if derivative.get("released_asro_native_schema") is not False:
        failures.append("derivative must not be presented as a released ASRO-native schema")

    if deprecated_alias.get("status") != "DEPRECATED_MISCLASSIFIED_PUBLIC_ALIAS":
        failures.append("historical misleading path must remain a deprecated provenance alias")
    if deprecated_alias.get("replacement") != str(DERIVATIVE.relative_to(ROOT)):
        failures.append("deprecated alias must point to the corrected derivative")

    if source_observation.get("commit_sha") != "46f8fd2f8f35668b2b27fcbdb4e24e06b58513a2":
        failures.append("current public ASRO source commit is not pinned")
    if source_observation.get("source_path") != "README.md":
        failures.append("current public ASRO source path is not pinned")
    historical = source_observation.get("historical_observation_relationship", {})
    if historical.get("status") != "UNRESOLVED_NO_RETROACTIVE_SUBSTITUTION":
        failures.append("historical source observation must remain unresolved without retroactive substitution")
    if historical.get("current_observation_may_replace_historical_record") is not False:
        failures.append("current source observation must not replace historical observation")

    if reviewer.get("issuer") != "unresolved":
        failures.append("reviewer issuer must remain unresolved until designation")
    if reviewer.get("provenance", {}).get("derivation_status") != "DERIVATIVE":
        failures.append("reviewer profile must remain derivative")

    membership = manifest.get("collection_membership", {})
    reference = membership.get("declared_reference", {})
    if reference.get("object_id") != derivative.get("object_id"):
        failures.append("manifest must bind the corrected derivative identity")
    if reference.get("path") != str(DERIVATIVE.relative_to(ROOT)):
        failures.append("manifest must bind the corrected derivative path")
    if reference.get("sha256") != derivative.get("sha256"):
        failures.append("manifest must bind the corrected derivative hash")
    if "NOT_SOURCE_INPUT" not in str(reference.get("hash_scope", "")):
        failures.append("manifest hash scope must be derivative-only")
    if membership.get("label_only_match_sufficient") is not False:
        failures.append("label-only matching must be rejected")

    source_membership = membership.get("source_example", {})
    if membership.get("source_membership_result") != "UNRESOLVED":
        failures.append("original source-example membership must remain unresolved")
    if source_membership.get("source_input_sha256") is not None:
        failures.append("original source-example hash must remain unset")
    if source_membership.get("source_input_reference") is not None:
        failures.append("original source-example reference must remain unset")

    determination = manifest.get("determination", {})
    for field in (
        "truth_established",
        "sufficiency_established",
        "validity_established",
        "admissibility_established",
        "authority_inherited",
    ):
        if determination.get(field) is not False:
            failures.append(f"correspondence improperly establishes {field}")

    if framework.get("status") != "PROVISIONAL_CORRECTION_IN_PROGRESS":
        failures.append("ASRO evaluation must remain provisional during correction")
    if framework.get("publication_class") != "UNILATERAL_STEGVERSE_ANALYSIS":
        failures.append("ASRO evaluation publication class must remain unilateral StegVerse analysis")
    if framework.get("bilateral_seam_comparison_record_issued") is not False:
        failures.append("bilateral Seam Comparison Record must remain unissued")
    if framework.get("framework", {}).get("source_version_status") != "PARTIAL_CURRENT_OBSERVATION_HISTORICAL_UNRESOLVED":
        failures.append("source version status must distinguish current pinning from unresolved historical observation")
    runs = framework.get("test_runs", [])
    if len(runs) != 1 or runs[0].get("result") != "HISTORICAL_PASS_SUPERSEDED_PENDING_CORRECTED_RUN":
        failures.append("historical run must be preserved but superseded pending corrected execution")
    elif runs[0].get("admissibility") != "NOT_EVALUATED":
        failures.append("ASRO bounded run must not establish admissibility")
    if framework.get("correction_state", {}).get("corrected_run_required") is not True:
        failures.append("corrected run must remain required")
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

    for marker in (
        "correspondence != admissibility",
        "correspondence != authority inheritance",
        "issuer: unresolved",
        "External ASRO-native execution remains `NOT_TESTED`",
    ):
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
    print("Corrected provenance, current public-source pinning, unilateral publication status, and superseded historical run remain fail-closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
