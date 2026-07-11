from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "automated-transition-run-receipt.schema.json"
EXAMPLE = ROOT / "examples" / "automated-transition-run-receipt.json"
PAGE = ROOT / "docs" / "governance" / "admissible-automated-transitions.md"

REQUIRED_FIELDS = {
    "receipt_id",
    "receipt_version",
    "transition_id",
    "run_id",
    "event_ref",
    "origin_class",
    "actor_ref",
    "target_ref",
    "scope",
    "policy_refs",
    "delegation_refs",
    "evidence_refs",
    "transition_signature",
    "micro_node_manifest_ref",
    "admissibility_result",
    "commit_time_validity",
    "action_result",
    "verification",
    "input_state_hash",
    "output_state_hash",
    "previous_receipt_ref",
    "resulting_handoff_ref",
    "recorded_at",
    "authority_boundary",
}


def load_json(path: Path, label: str, errors: list[str]) -> dict:
    if not path.exists():
        errors.append(f"missing_{label}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errors.append(f"invalid_{label}_json")
        return {}


def main() -> int:
    errors: list[str] = []
    schema = load_json(SCHEMA, "schema", errors)
    example = load_json(EXAMPLE, "example", errors)

    missing_schema = sorted(REQUIRED_FIELDS - set(schema.get("required", [])))
    if missing_schema:
        errors.append("schema_required:" + ",".join(missing_schema))

    missing_example = sorted(REQUIRED_FIELDS - set(example))
    if missing_example:
        errors.append("example_required:" + ",".join(missing_example))

    if example.get("admissibility_result") not in {"ALLOW", "DENY", "FAIL_CLOSED"}:
        errors.append("admissibility_result")

    validity = example.get("commit_time_validity", {})
    if validity.get("checked") is not True:
        errors.append("commit_time_checked")
    if validity.get("result") not in {"VALID", "INVALID", "NOT_APPLICABLE"}:
        errors.append("commit_time_result")

    if not example.get("policy_refs"):
        errors.append("policy_refs")
    if not example.get("delegation_refs"):
        errors.append("delegation_refs")
    if not example.get("evidence_refs"):
        errors.append("evidence_refs")

    signature = example.get("transition_signature", {})
    for key in ["mutation", "authority", "evidence", "recoverability", "verification", "continuation"]:
        if key not in signature:
            errors.append(f"signature:{key}")

    master_records = example.get("master_records", {})
    if master_records.get("record_status") not in {"NOT_SUBMITTED", "PENDING", "RECORDED", "REJECTED"}:
        errors.append("master_records_status")
    if master_records.get("reconstruction_status") not in {"NOT_CHECKED", "PARTIAL", "PASS", "FAIL"}:
        errors.append("reconstruction_status")

    boundary = example.get("authority_boundary", "")
    if "does not prove" not in boundary:
        errors.append("authority_boundary")

    if not PAGE.exists():
        errors.append("missing_page")
    else:
        page = PAGE.read_text(encoding="utf-8")
        for required in [
            "schemas/automated-transition-run-receipt.schema.json",
            "examples/automated-transition-run-receipt.json",
            "Master-Records",
        ]:
            if required not in page:
                errors.append(f"page_missing:{required}")

    if errors:
        print("AUTOMATED TRANSITION RUN RECEIPT: FAIL - " + ", ".join(errors))
        return 1

    print("AUTOMATED TRANSITION RUN RECEIPT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
