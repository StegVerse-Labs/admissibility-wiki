#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "static/data/framework-evaluations/asro"
DERIVATIVE = BASE / "stegverse-generated-bounded-metadata-derivative.json"
ALIAS = BASE / "asro-author-provided-bounded-representative-object.json"
MANIFEST = BASE / "correspondence-manifest.json"
TEST_CASE = ROOT / "static/data/framework-evaluations/test-cases/asro-declared-reference-membership-v1.json"
RECEIPT = ROOT / "receipts/asro-bounded-comparison-run-001.json"
DOC = ROOT / "docs/external-frameworks/asro-provenance-correction-2026-07-26.md"


def load(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    try:
        derivative = load(DERIVATIVE)
        alias = load(ALIAS)
        manifest = load(MANIFEST)
        test_case = load(TEST_CASE)
        receipt = load(RECEIPT)
        if not DOC.exists():
            errors.append(f"missing:{DOC.relative_to(ROOT)}")

        expected_derivative = {
            "artifact_type": "stegverse_generated_bounded_metadata_derivative",
            "creator": "StegVerse Labs",
            "classification": "STEGVERSE_GENERATED_BOUNDED_DERIVATIVE",
            "canonical_status": "NON_CANONICAL",
            "released_asro_native_schema": False,
            "derivation_status": "TRANSFORMED_OR_REDUCED",
        }
        for key, value in expected_derivative.items():
            if derivative.get(key) != value:
                errors.append(f"derivative:{key}")

        source = derivative.get("source_example", {})
        if source.get("publicly_reproduced") is not False:
            errors.append("derivative:source_publicly_reproduced")
        if source.get("content_hash_recorded") is not False:
            errors.append("derivative:source_content_hash_recorded")
        if not str(source.get("source_linkage_status", "")).startswith("UNRESOLVED"):
            errors.append("derivative:source_linkage_status")

        if alias.get("status") != "DEPRECATED_MISCLASSIFIED_PUBLIC_ALIAS":
            errors.append("alias:status")
        if alias.get("replacement") != str(DERIVATIVE.relative_to(ROOT)):
            errors.append("alias:replacement")
        if alias.get("history_preservation", {}).get("prior_public_history_rewritten") is not False:
            errors.append("alias:history_rewrite")
        for field in ("asro_release", "jointly_issued", "certification", "endorsement", "admissibility", "execution"):
            if alias.get("authority_boundary", {}).get(field) is not False:
                errors.append(f"alias:authority:{field}")

        membership = manifest.get("collection_membership", {})
        reference = membership.get("declared_reference", {})
        manifest_source = membership.get("source_example", {})
        if manifest.get("status") != "CORRECTED_PROVISIONAL":
            errors.append("manifest:status")
        if reference.get("artifact_role") != "PUBLIC_STEGVERSE_METADATA_DERIVATIVE":
            errors.append("manifest:artifact_role")
        if reference.get("path") != str(DERIVATIVE.relative_to(ROOT)):
            errors.append("manifest:derivative_path")
        if reference.get("sha256") != derivative.get("sha256"):
            errors.append("manifest:derivative_hash")
        if "NOT_SOURCE_INPUT" not in str(reference.get("hash_scope", "")):
            errors.append("manifest:hash_scope")
        if manifest_source.get("source_input_reference") is not None or manifest_source.get("source_input_sha256") is not None:
            errors.append("manifest:false_source_binding")
        if membership.get("source_membership_result") != "UNRESOLVED":
            errors.append("manifest:source_membership")
        if manifest.get("sha256") is not None:
            errors.append("manifest:premature_final_hash")

        if test_case.get("status") != "PROVISIONAL_CORRECTION_IN_PROGRESS":
            errors.append("test_case:status")
        if test_case.get("frozen_at") is not None or test_case.get("package_sha256") is not None:
            errors.append("test_case:premature_freeze")
        test_source = test_case.get("source_example", {})
        if test_source.get("source_input_reference") is not None or test_source.get("source_input_sha256") is not None:
            errors.append("test_case:false_source_binding")
        if test_source.get("correspondence_status") != "UNRESOLVED":
            errors.append("test_case:source_correspondence")
        if test_case.get("replay", {}).get("historical_run_status") != "PRESERVED_NOT_RETROACTIVELY_REWRITTEN":
            errors.append("test_case:history_preservation")

        if receipt.get("status") != "PROVISIONAL_SUPERSEDED_PENDING_CORRECTED_RUN":
            errors.append("receipt:status")
        if receipt.get("current_test_package_sha256") is not None or receipt.get("receipt_hash") is not None:
            errors.append("receipt:premature_hash")
        if receipt.get("finalization_status") != "UNFINALIZED_PENDING_CORRECTED_PACKAGE_HASH_AND_RUN":
            errors.append("receipt:finalization_status")
        if receipt.get("current_effect", {}).get("external_asro_native_execution") != "NOT_TESTED":
            errors.append("receipt:external_execution")
        if receipt.get("current_effect", {}).get("reviewer_issuer") != "unresolved":
            errors.append("receipt:reviewer_issuer")
        nonclaims = receipt.get("bounded_non_claims", {})
        for field in (
            "original_source_json_hashed",
            "original_source_correspondence_established",
            "truth_established",
            "admissibility_established",
            "authority_inherited",
            "certification_issued",
            "joint_issuance_claimed",
        ):
            if nonclaims.get(field) is not False:
                errors.append(f"receipt:nonclaim:{field}")

        if DOC.exists():
            text = DOC.read_text(encoding="utf-8")
            for marker in (
                "Existing public packet: UNILATERAL_STEGVERSE_ANALYSIS",
                "Bilateral Seam Comparison Record: NOT_ISSUED",
                "External ASRO-native execution: NOT_TESTED",
                "Accountable reviewer or issuer: unresolved",
            ):
                if marker not in text:
                    errors.append(f"doc:{marker}")
    except (AssertionError, json.JSONDecodeError) as exc:
        errors.append(str(exc))

    if errors:
        print("ASRO PROVENANCE CORRECTION: FAIL - " + ", ".join(errors))
        return 1
    print("ASRO PROVENANCE CORRECTION: PASS")
    print("Source and derivative remain separate; manifest, fixture, and receipt remain provisional until corrected integrity and run evidence are generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
