from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "governed-output-classes-status.json"
PAGE = ROOT / "docs" / "governance" / "governed-output-classes.md"
PARENT_PAGE = ROOT / "docs" / "governance" / "governed-ecosystem-transitions.md"

EXPECTED_CLASSES = [
    "admitted_response",
    "denial_receipt",
    "fail_closed_receipt",
    "committed_repo_change",
    "strp_handoff",
    "receipt_chain_continuation",
    "state_transition_summary",
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
    if data.get("schema") != "admissibility_wiki.governed_output_classes_status.v1":
        errors.append("schema")
    if data.get("status") != "GOVERNED_OUTPUT_CLASS_REGISTRY_PRESENT":
        errors.append("status")
    if data.get("output_classes") != EXPECTED_CLASSES:
        errors.append("output_classes")
    boundary = data.get("claim_boundary", {})
    for key in [
        "registration_grants_validity",
        "registration_grants_execution_authority",
        "registration_grants_canonical_receipt_admission",
    ]:
        if boundary.get(key) is not False:
            errors.append(key)
    for key in [
        "each_instance_requires_transition_record",
        "each_instance_requires_authority_posture",
        "each_instance_requires_receipt_binding",
    ]:
        if boundary.get(key) is not True:
            errors.append(key)
    if errors:
        print("GOVERNED OUTPUT CLASSES: FAIL - " + ", ".join(errors))
        return 1
    print("GOVERNED OUTPUT CLASSES: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
