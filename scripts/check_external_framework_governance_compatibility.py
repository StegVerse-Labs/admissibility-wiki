#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "static/external-frameworks/compatibility-testing-standard.v1.json"
STATUS = ROOT / "static/external-frameworks/governance-compatibility-testing-status.v1.json"
UNION = ROOT / "static/external-frameworks/canonical-union-inventory.v1.json"
OPA_PIPELINE = ROOT / "scripts/summarize_opa_evidence_pipeline.py"
OPA_REPLAY = ROOT / "scripts/run_independent_opa_ci_replay.py"
CONTRACTS = {
    "open-policy-agent": ("opa", "open-policy-agent.md", "BOUNDED_COMPATIBILITY_OBSERVED"),
    "cedar-policy": ("cedar", "cedar-policy.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "spiffe-spire": ("spiffe-spire", "spiffe-spire.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "w3c-verifiable-credentials": ("w3c-vc", "w3c-verifiable-credentials.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "in-toto": ("in-toto", "in-toto.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "slsa": ("slsa", "slsa.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "sigstore": ("sigstore", "sigstore.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "openid-connect": ("openid-connect", "openid-connect.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "oauth2": ("oauth2", "oauth2.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "w3c-did": ("w3c-did", "w3c-did.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "oscal": ("oscal", "oscal.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "openlineage": ("openlineage", "openlineage.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "w3c-prov": ("w3c-prov", "w3c-prov.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "model-context-protocol": ("model-context-protocol", "model-context-protocol.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "agent2agent-protocol": ("agent2agent-protocol", "agent2agent-protocol.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "guardrails-ai": ("guardrails-ai", "guardrails-ai.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "llama-guard": ("llama-guard", "llama-guard.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "nemo-guardrails": ("nemo-guardrails", "nemo-guardrails.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "glm": ("glm", "glm.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "evide": ("evide", "evide.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "asro": ("asro", "asro.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "decisionassure": ("decisionassure", "decisionassure.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "mindforge": ("mindforge", "mindforge.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
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
    for layer in {"native_framework_execution","semantic_translation","stegverse_commit_time_evaluation","failure_boundary_evaluation","fresh_runner_replay","page_and_machine_readable_result_publication"}:
        if layer not in set(standard.get("required_layers", [])):
            fail(f"standard missing layer: {layer}")

    canonical_ids = {entry.get("record_id") for entry in union.get("entries", []) if entry.get("record_id")}
    if len(canonical_ids) != 38 or union.get("counts", {}).get("records") != 38:
        fail(f"canonical inventory count mismatch: {len(canonical_ids)}")
    records = {record.get("framework_id"): record for record in status.get("records", [])}
    if set(records) != set(CONTRACTS):
        fail(f"authored contract set mismatch: {sorted(records)}")
    if not set(records).issubset(canonical_ids):
        fail(f"unknown framework IDs: {sorted(set(records) - canonical_ids)}")

    required_families = set(standard.get("required_case_families", []))
    for framework_id, (stem, page_name, state) in CONTRACTS.items():
        fixture = ROOT / "tests/fixtures/external-frameworks" / f"{stem}-governance-compatibility-cases.v1.json"
        runner = ROOT / "scripts" / f"run_{stem.replace('-', '_')}_governance_compatibility.py"
        page = ROOT / "docs/external-frameworks" / page_name
        data = load(fixture)
        cases = data.get("cases", [])
        families = {case.get("family") for case in cases}
        if not runner.exists() or not page.exists():
            fail(f"missing runner or page for {framework_id}")
        if len(cases) != 6 or families != required_families:
            fail(f"case contract mismatch for {framework_id}: count={len(cases)} families={sorted(families)}")
        record = records[framework_id]
        if record.get("state") != state:
            fail(f"invalid state for {framework_id}: {record.get('state')}")
        if record.get("case_count") != 6:
            fail(f"invalid case count for {framework_id}")
        expected_observed = framework_id == "open-policy-agent"
        if record.get("stegverse_governance_compatibility_observed") is not expected_observed:
            fail(f"invalid compatibility observation state for {framework_id}")
        for case in cases:
            if case.get("expected_stegverse_result") not in {"ALLOW","DENY","ESCALATE","FAIL_CLOSED"}:
                fail(f"invalid expected result: {framework_id}/{case.get('case_id')}")

    opa_text = (OPA_PIPELINE.read_text(encoding="utf-8") if OPA_PIPELINE.exists() else "") + (OPA_REPLAY.read_text(encoding="utf-8") if OPA_REPLAY.exists() else "")
    for marker in ("run_opa_governance_compatibility.py","opa-stegverse-governance-compatibility-receipt.json","governance_compatibility_observed","compatibility_receipt_grants_execution_authority"):
        if marker not in opa_text:
            fail(f"OPA execution binding missing marker: {marker}")

    opa = records["open-policy-agent"]
    if not all(opa.get(key) is True for key in ("native_execution_observed","same_environment_replay_observed","fresh_runner_replay_observed","stegverse_governance_compatibility_observed")):
        fail("OPA bounded execution, replay, and compatibility observations must remain recorded")
    observed = opa.get("observed_evidence", {})
    if observed.get("workflow_run_id") != "29455057960" or observed.get("commit") != "618a57fb618cd29c90264eb1cab5f4d6814a55f6":
        fail("OPA observation must remain bound to the directly inspected workflow evidence")
    if observed.get("total_cases") != 6 or observed.get("matching_cases") != 6 or observed.get("bounded_compatibility_state") != "GOVERNANCE_COMPATIBILITY_OBSERVED":
        fail("OPA bounded receipt summary mismatch")
    if observed.get("independent_implementation_or_provider_review") is not False:
        fail("OPA must not claim independent implementation or provider review")

    if records["cedar-policy"].get("binary_build_observed") is not True or records["cedar-policy"].get("native_execution_observed") is not False:
        fail("Cedar must remain build-observed and runtime-unobserved")
    for framework_id in ("spiffe-spire","w3c-verifiable-credentials","in-toto","slsa","sigstore","openid-connect","oauth2","w3c-did","oscal","openlineage","w3c-prov","model-context-protocol","agent2agent-protocol","guardrails-ai","llama-guard","nemo-guardrails","glm","evide","asro"):
        if records[framework_id].get("source_reviewed") is not True or records[framework_id].get("native_execution_observed") is not False:
            fail(f"{framework_id} must remain source-reviewed and runtime-unobserved")
    for framework_id in ("decisionassure", "mindforge"):
        record = records[framework_id]
        if record.get("source_reviewed") is not False or record.get("artifact_package_required") is not True or record.get("native_execution_observed") is not False:
            fail(f"{framework_id} must remain artifact-package-required and runtime-unobserved")

    expected_counts = {"canonical_records":38,"contract_authored":23,"governance_compatibility_observed":1,"fresh_runner_reproduced":1,"independent_implementation_reproduced":0,"not_started":15}
    for key, expected in expected_counts.items():
        if status.get("counts", {}).get(key) != expected:
            fail(f"status count stale: {key}={status.get('counts', {}).get(key)} expected={expected}")

    joined = json.dumps(standard).lower() + json.dumps(status).lower()
    for phrase in ["does not certify","execution authority","general compatibility","policy evidence","identity verification","credential verification","provenance verification","signature verification","authentication","token acceptance","did control","control evidence","lineage visibility","provenance representation","tool discovery","task completion","validator pass","safe classification","rail pass","manifest validity","post-event","operational assurance","trace validity","historical review"]:
        if phrase not in joined:
            fail(f"missing boundary phrase: {phrase}")

    print("EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: PASS")
    print("canonical_records=38")
    print("contracts_authored=23")
    print("compatibility_observed=1")
    print("opa_bounded_compatibility=observed_run_29455057960")
    for framework_id in CONTRACTS:
        print(f"{framework_id}_case_families=6")


if __name__ == "__main__":
    main()
