from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "governed-transition-map-status.json"
PAGE = ROOT / "docs" / "governance" / "governed-transition-map.md"
INPUT_PAGE = ROOT / "docs" / "governance" / "governed-input-classes.md"
OUTPUT_PAGE = ROOT / "docs" / "governance" / "governed-output-classes.md"

EXPECTED_PATH = [
    "input_class_instance",
    "governed_ingestion",
    "cge_fingerprinting",
    "gcat_bcat_evaluation",
    "transition_table_standing",
    "allow_deny_fail_closed",
    "receipt_chain_or_strp_record",
    "output_class_instance",
]


def main():
    errors = []
    if not STATUS.exists():
        errors.append("missing_status")
        data = {}
    else:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
    for path, label in [(PAGE, "missing_page"), (INPUT_PAGE, "missing_input_page"), (OUTPUT_PAGE, "missing_output_page")]:
        if not path.exists():
            errors.append(label)
    if data.get("schema") != "admissibility_wiki.governed_transition_map_status.v1":
        errors.append("schema")
    if data.get("status") != "GOVERNED_TRANSITION_MAP_PRESENT":
        errors.append("status")
    if data.get("transition_path") != EXPECTED_PATH:
        errors.append("transition_path")
    boundary = data.get("claim_boundary", {})
    for key in ["map_grants_authority", "map_grants_admissibility", "map_grants_output_permission"]:
        if boundary.get(key) is not False:
            errors.append(key)
    for key in ["each_transition_requires_current_standing", "each_transition_requires_receipt_binding"]:
        if boundary.get(key) is not True:
            errors.append(key)
    if errors:
        print("GOVERNED TRANSITION MAP: FAIL - " + ", ".join(errors))
        return 1
    print("GOVERNED TRANSITION MAP: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
