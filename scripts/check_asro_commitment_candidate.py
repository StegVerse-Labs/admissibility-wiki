from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "external-frameworks" / "asro.md"
MANIFEST = ROOT / "docs" / "external-frameworks" / "asro.json"
CANDIDATE = ROOT / "docs" / "external-frameworks" / "asro-commitment-candidate.json"

FALSE_AUTHORITY_FLAGS = [
    ("authority_boundary", "commitment_candidate_is_authority"),
    ("authority_boundary", "asro_attestation_is_authority"),
    ("authority_boundary", "external_framework_inclusion_is_certification"),
    ("authority_boundary", "external_framework_inclusion_is_endorsement"),
    ("authority_boundary", "external_framework_inclusion_is_admissibility_proof"),
    ("authority_boundary", "external_framework_inclusion_is_execution_authority"),
]

REQUIRED_PAGE_MARKERS = [
    "ASRO External Framework Crosswalk",
    "Commitment Candidate Fixture",
    "docs/external-frameworks/asro-commitment-candidate.json",
    "ASRO is not a StegVerse canonical formalism.",
    "ASRO does not prove transition admissibility.",
    "ASRO does not grant execution authority inside StegVerse.",
]

REQUIRED_CANDIDATE_FIELDS = [
    "artifact_type",
    "schema_version",
    "framework_id",
    "status",
    "transition_id",
    "requested_action",
    "actor",
    "target",
    "scope",
    "policy_reference",
    "delegation_reference",
    "evidence_references",
    "execution_context",
    "validity_window",
    "recoverability_profile",
    "expected_spe_result",
    "authority_boundary",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    for path in [PAGE, MANIFEST, CANDIDATE]:
        if not path.exists():
            errors.append(f"missing:{path.relative_to(ROOT)}")

    page_text = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    for marker in REQUIRED_PAGE_MARKERS:
        if marker not in page_text:
            errors.append(f"missing_page_marker:{marker}")

    manifest = load_json(MANIFEST) if MANIFEST.exists() else {}
    if manifest.get("framework_id") != "asro":
        errors.append("manifest_framework_id")
    if manifest.get("boundary", {}).get("execution_authority_claim") is not False:
        errors.append("manifest_execution_authority_claim")
    if manifest.get("boundary", {}).get("commit_time_authority_claim") is not False:
        errors.append("manifest_commit_time_authority_claim")

    candidate = load_json(CANDIDATE) if CANDIDATE.exists() else {}
    for field in REQUIRED_CANDIDATE_FIELDS:
        if field not in candidate:
            errors.append(f"candidate_missing:{field}")

    if candidate.get("artifact_type") != "external_framework_commitment_candidate_fixture":
        errors.append("candidate_artifact_type")
    if candidate.get("framework_id") != "asro":
        errors.append("candidate_framework_id")
    if candidate.get("status") != "NON_AUTHORIZING_FIXTURE":
        errors.append("candidate_status")

    for group, key in FALSE_AUTHORITY_FLAGS:
        if candidate.get(group, {}).get(key) is not False:
            errors.append(f"candidate_{key}")

    execution_context = candidate.get("execution_context", {})
    for key in [
        "live_provider_activation",
        "production_authority",
        "public_endorsement",
        "repository_mutation_authority",
        "general_external_llm_validation",
    ]:
        if execution_context.get(key) is not False:
            errors.append(f"candidate_execution_context_{key}")

    expected = candidate.get("expected_spe_result", {})
    if expected.get("default") != "FAIL-CLOSED":
        errors.append("candidate_expected_default_fail_closed")

    if errors:
        print("ASRO COMMITMENT CANDIDATE: FAIL - " + ", ".join(errors))
        return 1

    print("ASRO COMMITMENT CANDIDATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
