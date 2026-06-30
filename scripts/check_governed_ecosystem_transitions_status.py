from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "governed-ecosystem-transitions-status.json"
PAGE = ROOT / "docs" / "governance" / "governed-ecosystem-transitions.md"

EXPECTED_PATH = [
    "input_or_request",
    "governed_ingestion",
    "cge_fingerprinting",
    "gcat_bcat_evaluation",
    "transition_table_standing",
    "allow_deny_fail_closed",
    "receipt_chain_or_strp_record",
    "governed_output",
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
    if data.get("schema") != "admissibility_wiki.governed_ecosystem_transitions_status.v1":
        errors.append("schema")
    if data.get("status") != "GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT":
        errors.append("status")
    if data.get("transition_path") != EXPECTED_PATH:
        errors.append("transition_path")
    boundary = data.get("claim_boundary", {})
    if boundary.get("external_frameworks_are_input_class") is not True:
        errors.append("external_frameworks_are_input_class")
    for key in ["live_connector_installed", "production_authority_claimed", "canonical_strp_admission_claimed"]:
        if boundary.get(key) is not False:
            errors.append(key)
    if errors:
        print("GOVERNED ECOSYSTEM TRANSITIONS: FAIL - " + ", ".join(errors))
        return 1
    print("GOVERNED ECOSYSTEM TRANSITIONS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
