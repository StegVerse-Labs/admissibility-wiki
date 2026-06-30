from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "governed-ecosystem-index-status.json"
PAGE = ROOT / "docs" / "governance" / "governed-ecosystem-index.md"
VERIFY_PAGE = ROOT / "docs" / "governance" / "ecosystem-capability-status.md"


def main():
    errors = []
    if not STATUS.exists():
        errors.append("missing_status")
        data = {}
    else:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
    if not PAGE.exists():
        errors.append("missing_page")
    if not VERIFY_PAGE.exists():
        errors.append("missing_verification_page")
    if data.get("schema") != "admissibility_wiki.governed_ecosystem_index_status.v1":
        errors.append("schema")
    if data.get("status") != "GOVERNED_ECOSYSTEM_INDEX_PRESENT":
        errors.append("status")
    boundary = data.get("claim_boundary", {})
    for key in [
        "index_grants_authority",
        "index_claims_release_authorization",
        "index_claims_operational_standing",
    ]:
        if boundary.get(key) is not False:
            errors.append(key)
    if errors:
        print("GOVERNED ECOSYSTEM INDEX: FAIL - " + ", ".join(errors))
        return 1
    print("GOVERNED ECOSYSTEM INDEX: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
