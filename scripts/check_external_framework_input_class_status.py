from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "external-framework-input-class-status.json"
PAGE = ROOT / "docs" / "governance" / "external-frameworks-as-input-class.md"
PARENT_PAGE = ROOT / "docs" / "governance" / "governed-ecosystem-transitions.md"

EXPECTED_PATH = [
    "external_framework_artifact",
    "governed_ingestion",
    "cge_fingerprinting",
    "gcat_bcat_evaluation",
    "transition_table_standing",
    "allow_deny_fail_closed",
    "receipt_chain_or_strp_record",
    "governed_output",
]

FALSE_CLAIMS = [
    "certification_claimed",
    "endorsement_claimed",
    "formalism_adoption_claimed",
    "admissibility_proof_claimed",
    "execution_authority_claimed",
    "canonical_strp_admission_claimed",
]


def main():
    errors = []
    if not STATUS.exists():
        errors.append("missing_status")
        data = {}
    else:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
    if not PAGE.exists():
        errors.append("missing_page")
    if not PARENT_PAGE.exists():
        errors.append("missing_parent_page")
    if data.get("schema") != "admissibility_wiki.external_framework_input_class_status.v1":
        errors.append("schema")
    if data.get("status") != "EXTERNAL_FRAMEWORK_INPUT_CLASS_FRAMING_PRESENT":
        errors.append("status")
    if data.get("transition_path") != EXPECTED_PATH:
        errors.append("transition_path")
    boundary = data.get("claim_boundary", {})
    if boundary.get("external_frameworks_are_input_class") is not True:
        errors.append("external_frameworks_are_input_class")
    if boundary.get("compatibility_evidence_only") is not True:
        errors.append("compatibility_evidence_only")
    for key in FALSE_CLAIMS:
        if boundary.get(key) is not False:
            errors.append(key)
    if errors:
        print("EXTERNAL FRAMEWORK INPUT CLASS: FAIL - " + ", ".join(errors))
        return 1
    print("EXTERNAL FRAMEWORK INPUT CLASS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
