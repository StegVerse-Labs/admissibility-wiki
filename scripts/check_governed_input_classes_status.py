from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "governed-input-classes-status.json"
PAGE = ROOT / "docs" / "governance" / "governed-input-classes.md"
PARENT_PAGE = ROOT / "docs" / "governance" / "governed-ecosystem-transitions.md"

EXPECTED_CLASSES = [
    "external_framework_outputs",
    "llm_or_agent_outputs",
    "human_requests",
    "repo_tasks",
    "sdk_requests",
    "runtime_observations",
    "receipt_chain_continuations",
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
    if data.get("schema") != "admissibility_wiki.governed_input_classes_status.v1":
        errors.append("schema")
    if data.get("status") != "GOVERNED_INPUT_CLASS_REGISTRY_PRESENT":
        errors.append("status")
    if data.get("input_classes") != EXPECTED_CLASSES:
        errors.append("input_classes")
    boundary = data.get("claim_boundary", {})
    for key in [
        "registration_grants_admissibility",
        "registration_grants_execution_authority",
        "registration_grants_canonical_receipt_admission",
    ]:
        if boundary.get(key) is not False:
            errors.append(key)
    for key in [
        "each_instance_requires_governed_ingestion",
        "each_instance_requires_transition_evaluation",
    ]:
        if boundary.get(key) is not True:
            errors.append(key)
    if errors:
        print("GOVERNED INPUT CLASSES: FAIL - " + ", ".join(errors))
        return 1
    print("GOVERNED INPUT CLASSES: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
