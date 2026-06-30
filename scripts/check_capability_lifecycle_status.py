from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "capability-lifecycle-status.json"
PAGE = ROOT / "docs" / "governance" / "capability-lifecycle.md"

EXPECTED_STATES = [
    "proposed",
    "implemented",
    "internally_validated",
    "release_authorized",
    "publicly_verified",
    "operational",
    "deprecated",
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
    if data.get("schema") != "admissibility_wiki.capability_lifecycle_status.v1":
        errors.append("schema")
    if data.get("status") != "CAPABILITY_LIFECYCLE_REGISTRY_PRESENT":
        errors.append("status")
    if data.get("states") != EXPECTED_STATES:
        errors.append("states")
    boundary = data.get("claim_boundary", {})
    for key in [
        "lifecycle_model_grants_authority",
        "implemented_implies_released",
        "released_implies_publicly_verified",
        "publicly_verified_implies_operational",
    ]:
        if boundary.get(key) is not False:
            errors.append(key)
    if boundary.get("operational_requires_current_standing") is not True:
        errors.append("operational_requires_current_standing")
    if errors:
        print("CAPABILITY LIFECYCLE: FAIL - " + ", ".join(errors))
        return 1
    print("CAPABILITY LIFECYCLE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
