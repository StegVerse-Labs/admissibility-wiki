from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "admissible-automated-transitions.md"
MANIFEST = ROOT / "static" / "governance" / "admissible-automated-transitions.v0.1.json"
RECEIPT = ROOT / "receipts" / "admissible-automated-transitions-observatory-receipt.json"
STATUS = ROOT / "static" / "status" / "admissible-automated-transitions-status.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"

TRANSITION_ID = "automation.github-handoff-watch.hourly.v1"
SIDEBAR_ENTRY = "governance/admissible-automated-transitions"
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

    if not PAGE.exists():
        errors.append("missing_page")
    else:
        page_text = PAGE.read_text(encoding="utf-8")
        for required in [
            "Admissible Automated Transitions",
            TRANSITION_ID,
            "Derived transition-table elements",
            "commit-time validity",
            "run-specific receipt",
            "The triggering email, workflow result, schedule, or manual request does not determine the task.",
        ]:
            if required not in page_text:
                errors.append(f"page_missing:{required}")

    if not SIDEBAR.exists() or SIDEBAR_ENTRY not in SIDEBAR.read_text(encoding="utf-8"):
        errors.append("sidebar_entry")
    if not HANDOFF.exists() or TRANSITION_ID not in HANDOFF.read_text(encoding="utf-8"):
        errors.append("handoff_catalog_entry")

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
    }:
        errors.append("receipt_result")
    if TRANSITION_ID not in receipt.get("catalogued_transition_ids", []):
        errors.append("receipt_transition_id")

    if status.get("schema") != "admissibility_wiki.admissible_automated_transitions_status.v1":
        errors.append("status_schema")
    if status.get("status") not in {
        "OBSERVATORY_ARTIFACTS_INSTALLED",
        "TRANSITION_TABLE_DERIVATION_INSTALLED",
    }:
        errors.append("status_value")
    boundary = status.get("authority_boundary", {})
    if boundary.get("catalog_grants_execution_authority") is not False:
        errors.append("catalog_authority_boundary")
    if boundary.get("cross_repository_authority_inferred") is not False:
        errors.append("cross_repo_boundary")
    if boundary.get("run_specific_receipts_required") is not True:
        errors.append("run_receipt_boundary")

    if errors:
        print("ADMISSIBLE AUTOMATED TRANSITIONS: FAIL - " + ", ".join(errors))
        return 1
    print("ADMISSIBLE AUTOMATED TRANSITIONS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
