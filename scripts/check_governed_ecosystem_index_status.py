from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "governed-ecosystem-index-status.json"
PAGE = ROOT / "docs" / "governance" / "governed-ecosystem-index.md"
VERIFY_PAGE = ROOT / "docs" / "governance" / "ecosystem-capability-status.md"
GUARDIAN_STATUS = ROOT / "static" / "status" / "guardian-destination-resolution-status.json"


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
    if not GUARDIAN_STATUS.exists():
        errors.append("missing_guardian_status")
    if data.get("schema") != "admissibility_wiki.governed_ecosystem_index_status.v1":
        errors.append("schema")
    if data.get("status") != "GOVERNED_ECOSYSTEM_INDEX_PRESENT":
        errors.append("status")

    destination = data.get("destination_resolution", {})
    if destination.get("guardian_status_artifact") != "static/status/guardian-destination-resolution-status.json":
        errors.append("guardian_status_artifact")
    if destination.get("canonical_public_guardian_destination") != "StegVerse-002/stegguardian-wiki":
        errors.append("canonical_public_guardian_destination")
    if destination.get("canonical_private_guardian_destination") != "StegVerse-002/StegGuardian":
        errors.append("canonical_private_guardian_destination")

    boundary = data.get("claim_boundary", {})
    for key in [
        "index_grants_authority",
        "index_claims_release_authorization",
        "index_claims_operational_standing",
        "guardian_destination_resolution_grants_activation",
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
