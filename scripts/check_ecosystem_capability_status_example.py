from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "ecosystem-capability-status.example.json"
VALID_STATES = [
    "proposed",
    "implemented",
    "internally_validated",
    "release_authorized",
    "publicly_verified",
    "operational",
    "deprecated",
]
REQUIRED_EVIDENCE = [
    "docs/governance/governed-ecosystem-transitions.md",
    "docs/governance/governed-input-classes.md",
    "docs/governance/governed-output-classes.md",
    "docs/governance/governed-transition-map.md",
    "docs/governance/capability-lifecycle.md",
]


def main():
    errors = []
    if not STATUS.exists():
        errors.append("missing_status")
        data = {}
    else:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
    if data.get("schema") != "stegverse.ecosystem_capability_status.v1":
        errors.append("schema")
    if data.get("status") != "ECOSYSTEM_CAPABILITY_STATUS_EXAMPLE_PRESENT":
        errors.append("status")
    capabilities = data.get("capabilities", [])
    if len(capabilities) != 1:
        errors.append("capability_count")
    item = capabilities[0] if capabilities else {}
    if item.get("current_state") not in VALID_STATES:
        errors.append("current_state")
    for key in ["implemented", "internally_validated"]:
        if item.get(key) is not True:
            errors.append(key)
    for key in ["release_authorized", "publicly_verified", "operational", "deprecated"]:
        if item.get(key) is not False:
            errors.append(key)
    if item.get("evidence") != REQUIRED_EVIDENCE:
        errors.append("evidence")
    for evidence_path in item.get("evidence", []):
        if not (ROOT / evidence_path).exists():
            errors.append("missing_evidence:" + evidence_path)
    boundary = item.get("boundary", {})
    if boundary.get("status_record_is_authority") is not False:
        errors.append("status_record_is_authority")
    if boundary.get("operational_requires_current_standing") is not True:
        errors.append("operational_requires_current_standing")
    if errors:
        print("ECOSYSTEM CAPABILITY STATUS EXAMPLE: FAIL - " + ", ".join(errors))
        return 1
    print("ECOSYSTEM CAPABILITY STATUS EXAMPLE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
