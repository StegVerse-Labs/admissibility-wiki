from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "admissible-automated-transitions.md"
MANIFEST = ROOT / "static" / "governance" / "admissible-automated-transitions.v0.1.json"
RECEIPT = ROOT / "receipts" / "admissible-automated-transitions-observatory-receipt.json"
STATUS = ROOT / "static" / "status" / "admissible-automated-transitions-status.json"
RUN_SCHEMA = ROOT / "schemas" / "automated-transition-run-receipt.schema.json"
RUN_EXAMPLE = ROOT / "examples" / "automated-transition-run-receipt.json"
SIDEBAR = ROOT / "sidebars.js"
PACKAGE = ROOT / "package.json"
HANDOFF = ROOT / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"

TRANSITION_ID = "automation.github-handoff-watch.hourly.v1"
SIDEBAR_ENTRY = "governance/admissible-automated-transitions"
PACKAGE_SCRIPT = "validate:admissible-automated-transitions"
REQUIRED_ELEMENTS = {
    "transition_id",
    "input_state",
    "proposed_action",
    "actor",
    "target",
    "scope",
    "policy_reference",
    "delegation_reference",
    "evidence_references",
    "authority_class",
    "review_posture",
    "execution_context",
    "validity_window",
    "recoverability_profile",
    "admissibility_result",
    "commit_time_validity",
    "output_state",
    "receipt_chain",
    "continuation_rule",
}
RUN_REQUIRED_FIELDS = {
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


def load_json(path: Path, errors: list[str], label: str) -> dict:
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
    manifest = load_json(MANIFEST, errors, "manifest")
    receipt = load_json(RECEIPT, errors, "receipt")
    status = load_json(STATUS, errors, "status")
    run_schema = load_json(RUN_SCHEMA, errors, "run_schema")
    run_example = load_json(RUN_EXAMPLE, errors, "run_example")
    package = load_json(PACKAGE, errors, "package")

    if not PAGE.exists():
        errors.append("missing_page")
    else:
        page_text = PAGE.read_text(encoding="utf-8")
        for required in [
            "Admissible Automated Transitions",
            TRANSITION_ID,
            "Derived transition-table elements",
            "commit-time validity",
            "Run-specific final receipt",
            "Master-Records",
            "The triggering email, workflow result, schedule, or manual request does not determine the task.",
        ]:
            if required not in page_text:
                errors.append(f"page_missing:{required}")

    if not SIDEBAR.exists() or SIDEBAR_ENTRY not in SIDEBAR.read_text(encoding="utf-8"):
        errors.append("sidebar_entry")
    if not HANDOFF.exists() or TRANSITION_ID not in HANDOFF.read_text(encoding="utf-8"):
        errors.append("handoff_catalog_entry")

    scripts = package.get("scripts", {})
    if scripts.get(PACKAGE_SCRIPT) != "python scripts/check_admissible_automated_transitions.py":
        errors.append("package_script")
    if f"npm run {PACKAGE_SCRIPT}" not in scripts.get("validate", ""):
        errors.append("canonical_validation_chain")

    if manifest.get("manifest_id") != "admissible-automated-transitions.v0.1":
        errors.append("manifest_id")
    transitions = manifest.get("transitions", [])
    matching = [item for item in transitions if item.get("transition_id") == TRANSITION_ID]
    if len(matching) != 1:
        errors.append("transition_catalog")
    else:
        item = matching[0]
        if item.get("lifecycle_state") != "ACTIVE_BOOTSTRAP_ORCHESTRATION":
            errors.append("lifecycle_state")
        authority = item.get("task_authority", {})
        if authority.get("source") != "current *_MIRROR_HANDOFF.md":
            errors.append("task_authority_source")
        if authority.get("event_does_not_select_task") is not True:
            errors.append("event_task_boundary")
        scope = item.get("scope", {})
        if scope.get("ecosystem_authority_inferred") is not False:
            errors.append("ecosystem_authority_boundary")

        derivation = item.get("transition_table_derivation", {})
        missing = sorted(REQUIRED_ELEMENTS - set(derivation))
        if missing:
            errors.append("missing_transition_elements:" + ",".join(missing))
        delegation = derivation.get("delegation_reference", {})
        if delegation.get("missing_or_ambiguous_result") != "FAIL_CLOSED":
            errors.append("delegation_fail_closed")
        authority_class = derivation.get("authority_class", {})
        if authority_class.get("release_deploy_merge_or_ecosystem_authority_inferred") is not False:
            errors.append("authority_class_boundary")
        validity = derivation.get("commit_time_validity", {})
        if validity.get("required_before_mutation") is not True:
            errors.append("commit_time_validity")
        receipt_chain = derivation.get("receipt_chain", {})
        if receipt_chain.get("run_specific_receipt_required") is not True:
            errors.append("run_specific_receipt")
        result_enum = derivation.get("admissibility_result", {}).get("enum", [])
        if result_enum != ["ALLOW", "DENY", "FAIL_CLOSED"]:
            errors.append("admissibility_result_enum")

    if receipt.get("result") not in {
        "DECLARED_AND_INSTALLED",
        "DECLARED_INSTALLED_AND_LOCALLY_CHECKABLE",
        "TRANSITION_TABLE_DERIVATION_INSTALLED",
        "RUN_RECEIPT_MODEL_INSTALLED",
    }:
        errors.append("receipt_result")
    if TRANSITION_ID not in receipt.get("catalogued_transition_ids", []):
        errors.append("receipt_transition_id")

    if status.get("schema") != "admissibility_wiki.admissible_automated_transitions_status.v1":
        errors.append("status_schema")
    if status.get("status") not in {
        "OBSERVATORY_ARTIFACTS_INSTALLED",
        "TRANSITION_TABLE_DERIVATION_INSTALLED",
        "RUN_RECEIPT_MODEL_INSTALLED",
    }:
        errors.append("status_value")
    boundary = status.get("authority_boundary", {})
    if boundary.get("catalog_grants_execution_authority") is not False:
        errors.append("catalog_authority_boundary")
    if boundary.get("cross_repository_authority_inferred") is not False:
        errors.append("cross_repo_boundary")
    if boundary.get("run_specific_receipts_required") is not True:
        errors.append("run_receipt_boundary")

    schema_required = set(run_schema.get("required", []))
    missing_schema_fields = sorted(RUN_REQUIRED_FIELDS - schema_required)
    if missing_schema_fields:
        errors.append("run_schema_required:" + ",".join(missing_schema_fields))
    result_enum = run_schema.get("properties", {}).get("admissibility_result", {}).get("enum", [])
    if result_enum != ["ALLOW", "DENY", "FAIL_CLOSED"]:
        errors.append("run_schema_result_enum")

    missing_example_fields = sorted(RUN_REQUIRED_FIELDS - set(run_example))
    if missing_example_fields:
        errors.append("run_example_required:" + ",".join(missing_example_fields))
    if run_example.get("transition_id") != TRANSITION_ID:
        errors.append("run_example_transition_id")
    if run_example.get("admissibility_result") not in {"ALLOW", "DENY", "FAIL_CLOSED"}:
        errors.append("run_example_result")
    if run_example.get("commit_time_validity", {}).get("checked") is not True:
        errors.append("run_example_commit_time_check")
    if run_example.get("master_records", {}).get("record_status") != "NOT_SUBMITTED":
        errors.append("run_example_master_records_boundary")

    if errors:
        print("ADMISSIBLE AUTOMATED TRANSITIONS: FAIL - " + ", ".join(errors))
        return 1
    print("ADMISSIBLE AUTOMATED TRANSITIONS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
