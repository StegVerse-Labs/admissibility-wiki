#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "static" / "external-frameworks" / "compatibility-testing-standard.v1.json"
STATUS = ROOT / "static" / "external-frameworks" / "governance-compatibility-testing-status.v1.json"
UNION = ROOT / "static" / "external-frameworks" / "canonical-union-inventory.v1.json"
OPA_FIXTURE = ROOT / "tests" / "fixtures" / "external-frameworks" / "opa-governance-compatibility-cases.v1.json"
OPA_RUNNER = ROOT / "scripts" / "run_opa_governance_compatibility.py"
OPA_PAGE = ROOT / "docs" / "external-frameworks" / "open-policy-agent.md"


def fail(message: str) -> None:
    raise SystemExit(f"EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: FAIL - {message}")


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    standard = load(STANDARD)
    status = load(STATUS)
    union = load(UNION)
    fixture = load(OPA_FIXTURE)
    if not OPA_RUNNER.exists():
        fail("OPA compatibility runner missing")
    if not OPA_PAGE.exists():
        fail("OPA page missing")

    if standard.get("schema") != "external_framework_governance_compatibility_testing_standard.v1":
        fail("unexpected standard schema")
    required_layers = set(standard.get("required_layers", []))
    for layer in {
        "native_framework_execution",
        "semantic_translation",
        "stegverse_commit_time_evaluation",
        "failure_boundary_evaluation",
        "fresh_runner_replay",
        "page_and_machine_readable_result_publication",
    }:
        if layer not in required_layers:
            fail(f"standard missing layer: {layer}")

    case_families = set(standard.get("required_case_families", []))
    fixture_families = {case.get("family") for case in fixture.get("cases", [])}
    if fixture_families != case_families:
        fail(f"OPA fixture case families mismatch: {sorted(fixture_families)}")
    if len(fixture.get("cases", [])) != 6:
        fail("OPA fixture must contain six cases")

    union_entries = union.get("entries", [])
    canonical_ids = {entry.get("record_id") for entry in union_entries if entry.get("record_id")}
    if len(canonical_ids) != 38:
        fail(f"canonical inventory count mismatch: {len(canonical_ids)}")
    if union.get("counts", {}).get("records") != 38:
        fail("canonical union stored record count mismatch")

    records = status.get("records", [])
    record_ids = {record.get("framework_id") for record in records}
    if not record_ids.issubset(canonical_ids):
        fail(f"status references unknown framework IDs: {sorted(record_ids - canonical_ids)}")
    if record_ids != {"open-policy-agent"}:
        fail("initial authored contract record must be exactly open-policy-agent")

    counts = status.get("counts", {})
    if counts.get("canonical_records") != 38:
        fail("status canonical record count stale")
    if counts.get("contract_authored") != 1:
        fail("status contract_authored count stale")
    if counts.get("governance_compatibility_observed") != 0:
        fail("compatibility must remain unobserved until workflow receipt exists")
    if counts.get("not_started") != 37:
        fail("status not_started count stale")

    opa = records[0]
    if opa.get("state") != "CONTRACT_AUTHORED":
        fail("OPA state must remain CONTRACT_AUTHORED before observed receipt")
    if opa.get("native_execution_observed") is not True:
        fail("OPA native execution observation must be recorded")
    if opa.get("fresh_runner_replay_observed") is not True:
        fail("OPA fresh-runner replay observation must be recorded")
    if opa.get("stegverse_governance_compatibility_observed") is not False:
        fail("OPA governance compatibility may not be pre-claimed")

    for case in fixture["cases"]:
        if case.get("expected_stegverse_result") not in {"ALLOW", "DENY", "ESCALATE", "FAIL_CLOSED"}:
            fail(f"invalid expected result: {case.get('case_id')}")
        transition = case.get("transition", {})
        required_fields = {
            "actor_identity_verified",
            "delegation_current",
            "policy_reference_current",
            "evidence_fresh",
            "target_matches_scope",
            "recoverability_satisfied",
            "execution_context_current",
        }
        if set(transition) != required_fields:
            fail(f"transition field mismatch: {case.get('case_id')}")

    joined = json.dumps(standard).lower() + json.dumps(status).lower() + fixture.get("authority_boundary", "").lower()
    for phrase in [
        "does not certify",
        "execution authority",
        "general compatibility",
        "policy evidence",
    ]:
        if phrase not in joined:
            fail(f"missing boundary phrase: {phrase}")

    print("EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: PASS")
    print("canonical_records=38")
    print("contracts_authored=1")
    print("compatibility_observed=0")
    print("opa_case_families=6")


if __name__ == "__main__":
    main()
