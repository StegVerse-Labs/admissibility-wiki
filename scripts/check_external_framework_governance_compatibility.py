#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "static" / "external-frameworks" / "compatibility-testing-standard.v1.json"
STATUS = ROOT / "static" / "external-frameworks" / "governance-compatibility-testing-status.v1.json"
UNION = ROOT / "static" / "external-frameworks" / "canonical-union-inventory.v1.json"
OPA_PIPELINE = ROOT / "scripts" / "summarize_opa_evidence_pipeline.py"
CONTRACTS = {
    "open-policy-agent": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "opa-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_opa_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "open-policy-agent.md", "allowed_states": {"CONTRACT_AUTHORED"}},
    "cedar-policy": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "cedar-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_cedar_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "cedar-policy.md", "allowed_states": {"CONTRACT_AUTHORED_RUNTIME_PENDING"}},
    "spiffe-spire": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "spiffe-spire-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_spiffe_spire_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "spiffe-spire.md", "allowed_states": {"CONTRACT_AUTHORED_RUNTIME_PENDING"}},
    "w3c-verifiable-credentials": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "w3c-vc-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_w3c_vc_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "w3c-verifiable-credentials.md", "allowed_states": {"CONTRACT_AUTHORED_RUNTIME_PENDING"}},
    "in-toto": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "in-toto-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_in_toto_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "in-toto.md", "allowed_states": {"CONTRACT_AUTHORED_RUNTIME_PENDING"}},
    "slsa": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "slsa-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_slsa_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "slsa.md", "allowed_states": {"CONTRACT_AUTHORED_RUNTIME_PENDING"}},
    "sigstore": {"fixture": ROOT / "tests" / "fixtures" / "external-frameworks" / "sigstore-governance-compatibility-cases.v1.json", "runner": ROOT / "scripts" / "run_sigstore_governance_compatibility.py", "page": ROOT / "docs" / "external-frameworks" / "sigstore.md", "allowed_states": {"CONTRACT_AUTHORED_RUNTIME_PENDING"}},
}


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
    if standard.get("schema") != "external_framework_governance_compatibility_testing_standard.v1":
        fail("unexpected standard schema")
    required_layers = set(standard.get("required_layers", []))
    for layer in {"native_framework_execution", "semantic_translation", "stegverse_commit_time_evaluation", "failure_boundary_evaluation", "fresh_runner_replay", "page_and_machine_readable_result_publication"}:
        if layer not in required_layers:
            fail(f"standard missing layer: {layer}")

    canonical_ids = {entry.get("record_id") for entry in union.get("entries", []) if entry.get("record_id")}
    if len(canonical_ids) != 38 or union.get("counts", {}).get("records") != 38:
        fail(f"canonical inventory count mismatch: {len(canonical_ids)}")

    records = status.get("records", [])
    records_by_id = {record.get("framework_id"): record for record in records}
    if set(records_by_id) != set(CONTRACTS):
        fail(f"authored contract set mismatch: {sorted(records_by_id)}")
    if not set(records_by_id).issubset(canonical_ids):
        fail(f"status references unknown framework IDs: {sorted(set(records_by_id) - canonical_ids)}")

    required_families = set(standard.get("required_case_families", []))
    for framework_id, contract in CONTRACTS.items():
        fixture = load(contract["fixture"])
        if not contract["runner"].exists() or not contract["page"].exists():
            fail(f"missing runner or page for {framework_id}")
        cases = fixture.get("cases", [])
        families = {case.get("family") for case in cases}
        if len(cases) != 6 or families != required_families:
            fail(f"case contract mismatch for {framework_id}: count={len(cases)} families={sorted(families)}")
        record = records_by_id[framework_id]
        if record.get("state") not in contract["allowed_states"]:
            fail(f"invalid state for {framework_id}: {record.get('state')}")
        if record.get("case_count") != 6:
            fail(f"case_count stale for {framework_id}")
        if record.get("stegverse_governance_compatibility_observed") is not False:
            fail(f"compatibility may not be pre-claimed for {framework_id}")
        for case in cases:
            if case.get("expected_stegverse_result") not in {"ALLOW", "DENY", "ESCALATE", "FAIL_CLOSED"}:
                fail(f"invalid expected result: {framework_id}/{case.get('case_id')}")

    if not OPA_PIPELINE.exists():
        fail("OPA evidence pipeline summarizer missing")
    opa_pipeline_text = OPA_PIPELINE.read_text(encoding="utf-8")
    for marker in ("run_opa_governance_compatibility.py", "opa-stegverse-governance-compatibility-receipt.json", "governance_compatibility_observed", "compatibility_receipt_grants_execution_authority"):
        if marker not in opa_pipeline_text:
            fail(f"OPA execution binding missing marker: {marker}")

    if records_by_id["open-policy-agent"].get("native_execution_observed") is not True or records_by_id["open-policy-agent"].get("fresh_runner_replay_observed") is not True:
        fail("OPA native execution and fresh-runner replay must remain observed")
    if records_by_id["cedar-policy"].get("binary_build_observed") is not True or records_by_id["cedar-policy"].get("native_execution_observed") is not False:
        fail("Cedar must remain build-observed and runtime-unobserved")
    for framework_id in ("spiffe-spire", "w3c-verifiable-credentials", "in-toto", "slsa", "sigstore"):
        record = records_by_id[framework_id]
        if record.get("source_reviewed") is not True or record.get("native_execution_observed") is not False:
            fail(f"{framework_id} must remain source-reviewed and runtime-unobserved")

    expected_counts = {"canonical_records": 38, "contract_authored": 7, "governance_compatibility_observed": 0, "fresh_runner_reproduced": 0, "independent_implementation_reproduced": 0, "not_started": 31}
    for key, expected in expected_counts.items():
        if status.get("counts", {}).get(key) != expected:
            fail(f"status count stale: {key}={status.get('counts', {}).get(key)} expected={expected}")

    joined = json.dumps(standard).lower() + json.dumps(status).lower()
    for phrase in ["does not certify", "execution authority", "general compatibility", "policy evidence", "identity verification", "credential verification", "provenance verification", "signature verification"]:
        if phrase not in joined:
            fail(f"missing boundary phrase: {phrase}")

    print("EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: PASS")
    print("canonical_records=38")
    print("contracts_authored=7")
    print("compatibility_observed=0")
    print("opa_execution_binding=installed_pending_observation")
    for framework_id in CONTRACTS:
        print(f"{framework_id}_case_families=6")


if __name__ == "__main__":
    main()
