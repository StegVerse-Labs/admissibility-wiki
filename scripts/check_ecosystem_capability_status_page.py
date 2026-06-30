from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "ecosystem-capability-status-page.json"
PAGE = ROOT / "docs" / "governance" / "ecosystem-capability-status.md"
EXAMPLE = ROOT / "static" / "status" / "ecosystem-capability-status.example.json"
EXAMPLE_VALIDATOR = ROOT / "scripts" / "check_ecosystem_capability_status_example.py"


def main():
    errors = []
    if not STATUS.exists():
        errors.append("missing_status")
        data = {}
    else:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
    for path, label in [
        (PAGE, "missing_page"),
        (EXAMPLE, "missing_example"),
        (EXAMPLE_VALIDATOR, "missing_example_validator"),
    ]:
        if not path.exists():
            errors.append(label)
    if data.get("schema") != "admissibility_wiki.ecosystem_capability_status_page.v1":
        errors.append("schema")
    if data.get("status") != "ECOSYSTEM_CAPABILITY_STATUS_PAGE_PRESENT":
        errors.append("status")
    boundary = data.get("claim_boundary", {})
    for key in [
        "status_page_grants_authority",
        "status_example_is_release_evidence",
        "status_example_is_public_verification",
    ]:
        if boundary.get(key) is not False:
            errors.append(key)
    if boundary.get("operational_requires_current_standing") is not True:
        errors.append("operational_requires_current_standing")
    if errors:
        print("ECOSYSTEM CAPABILITY STATUS PAGE: FAIL - " + ", ".join(errors))
        return 1
    print("ECOSYSTEM CAPABILITY STATUS PAGE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
