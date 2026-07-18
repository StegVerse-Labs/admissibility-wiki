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
    "morrison-runtime": ("morrison-runtime", "morrison-runtime.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "care-runtime": ("care-runtime", "care-runtime.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "kpt": ("kpt", "kpt.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "aar": ("aar", "aar.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "mitre-atlas": ("mitre-atlas", "mitre-atlas.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "owasp-top-10-llm": ("owasp-top-10-llm", "owasp-top-10-llm.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "agent-governance-playbook": ("agent-governance-playbook", "agent-governance-playbook.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "emergency-stop-convention": ("emergency-stop-convention", "killswitch-md.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "nist-ai-rmf": ("nist-ai-rmf", "nist-ai-rmf.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "iso-iec-42001": ("iso-iec-42001", "iso-iec-42001.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "eu-ai-act": ("eu-ai-act", "eu-ai-act.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "policy-cards": ("policy-cards", "policy-cards.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
    "runtime-governance-for-ai-agents": ("runtime-governance-for-ai-agents", "runtime-governance-policies-on-paths.md", "CONTRACT_AUTHORED_RUNTIME_PENDING"),
}


def fail(message: str) -> None:
    raise SystemExit(f"EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: FAIL - {message}")


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    standard, status, union = load(STANDARD), load(STATUS), load(UNION)
    if standard.get("schema") != "external_framework_governance_compatibility_testing_standard.v1":
        fail("unexpected standard schema")
    required_layers = {"native_framework_execution","semantic_translation","stegverse_commit_time_evaluation","failure_boundary_evaluation","fresh_runner_replay","page_and_machine_readable_result_publication"}
    if not required_layers.issubset(set(standard.get("required_layers", []))):
        fail("standard required layers incomplete")
    canonical_ids = {entry.get("record_id") for entry in union.get("entries", []) if entry.get("record_id")}
    if len(canonical_ids) != 38 or union.get("counts", {}).get("records") != 38:
        fail("canonical inventory count mismatch")
    defaults = status.get("record_defaults", {})
    records = {}
    for raw in status.get("records", []):
        record = dict(defaults)
        record.update(raw)
        records[record.get("framework_id")] = record
    if set(records) != set(CONTRACTS) or not set(records).issubset(canonical_ids):
        fail(f"authored contract set mismatch: {sorted(records)}")
    required_families = set(standard.get("required_case_families", []))
    for framework_id, (stem, page_name, state) in CONTRACTS.items():
        fixture = ROOT / "tests/fixtures/external-frameworks" / f"{stem}-governance-compatibility-cases.v1.json"
        runner = ROOT / "scripts" / f"run_{stem.replace('-', '_')}_governance_compatibility.py"
        page = ROOT / "docs/external-frameworks" / page_name
        data = load(fixture)
        cases = data.get("cases", [])
        if not runner.exists() or not page.exists() or len(cases) != 6 or {case.get('family') for case in cases} != required_families:
            fail(f"contract artifacts incomplete for {framework_id}")
        record = records[framework_id]
        if record.get("state") != state or record.get("case_count") != 6:
            fail(f"invalid state or case count for {framework_id}")
        if record.get("stegverse_governance_compatibility_observed") is not (framework_id == "open-policy-agent"):
            fail(f"invalid compatibility observation state for {framework_id}")
        if any(case.get("expected_stegverse_result") not in {"ALLOW","DENY","ESCALATE","FAIL_CLOSED"} for case in cases):
            fail(f"invalid expected result in {framework_id}")
    opa_text = (OPA_PIPELINE.read_text(encoding="utf-8") if OPA_PIPELINE.exists() else "") + (OPA_REPLAY.read_text(encoding="utf-8") if OPA_REPLAY.exists() else "")
    for marker in ("run_opa_governance_compatibility.py","opa-stegverse-governance-compatibility-receipt.json","governance_compatibility_observed","compatibility_receipt_grants_execution_authority"):
        if marker not in opa_text:
            fail(f"OPA execution binding missing marker: {marker}")
    opa = records["open-policy-agent"]
    observed = opa.get("observed_evidence", {})
    if not all(opa.get(key) is True for key in ("native_execution_observed","same_environment_replay_observed","fresh_runner_replay_observed","stegverse_governance_compatibility_observed")) or observed.get("workflow_run_id") != "29455057960" or observed.get("commit") != "618a57fb618cd29c90264eb1cab5f4d6814a55f6" or observed.get("matching_cases") != 6 or observed.get("independent_implementation_or_provider_review") is not False:
        fail("OPA evidence binding mismatch")
    if records["cedar-policy"].get("binary_build_observed") is not True or records["cedar-policy"].get("native_execution_observed") is not False:
        fail("Cedar posture stale")
    sourced = tuple(set(CONTRACTS) - {"open-policy-agent","cedar-policy","decisionassure","mindforge","care-runtime","kpt"})
    for framework_id in sourced:
        if records[framework_id].get("source_reviewed") is not True or records[framework_id].get("native_execution_observed") is not False:
            fail(f"{framework_id} source/runtime posture stale")
    for framework_id in ("decisionassure", "mindforge"):
        if records[framework_id].get("source_reviewed") is not False or records[framework_id].get("artifact_package_required") is not True or records[framework_id].get("native_execution_observed") is not False:
            fail(f"{framework_id} artifact posture stale")
    if records["morrison-runtime"].get("bounded_historical_observation_only") is not True or records["care-runtime"].get("screenshot_only_intake") is not True or records["kpt"].get("public_positioning_only") is not True:
        fail("bounded source posture stale")
    runtime = records["runtime-governance-for-ai-agents"]
    if runtime.get("official_source_confirmed") is not True or runtime.get("paper_source") is not True or runtime.get("implementation_attached") is not False or runtime.get("runtime_path_observed") is not False or runtime.get("independent_reproduction_observed") is not False or runtime.get("native_execution_observed") is not False:
        fail("Runtime Governance for AI Agents posture stale")
    required_false = (
        "runtime_verdict_means_action_authority","public_platform_display_means_action_authority","screenshot_intake_means_source_confirmation","kpt_decision_means_action_authority","public_positioning_means_source_confirmation","assessment_result_means_action_authority","forensic_visibility_means_commit_time_authority","threat_classification_means_action_authority","mitigation_mapping_means_commit_time_admissibility","risk_classification_means_action_authority","security_guidance_means_commit_time_admissibility","playbook_alignment_means_action_authority","continuation_recommendation_means_commit_time_admissibility","emergency_stop_signal_means_action_authority","stop_convention_means_current_standing","risk_management_alignment_means_action_authority","trustworthiness_profile_means_commit_time_admissibility","management_system_conformity_means_action_authority","certification_evidence_means_commit_time_admissibility","regulatory_classification_means_action_authority","legal_applicability_means_commit_time_admissibility","policy_card_declaration_means_action_authority","policy_rule_means_commit_time_admissibility","runtime_path_score_means_action_authority","runtime_recommendation_means_commit_time_admissibility",
    )
    boundaries = status.get("boundaries", {})
    for key in required_false:
        if boundaries.get(key) is not False:
            fail(f"non-authority boundary stale: {key}")
    if status.get("manual_tasks_required") != [] or status.get("user_action_required") is not False:
        fail("compatibility continuation must remain automation-owned with no manual task")
    expected_counts = {"canonical_records":38,"contract_authored":36,"governance_compatibility_observed":1,"fresh_runner_reproduced":1,"independent_implementation_reproduced":0,"not_started":2}
    for key, expected in expected_counts.items():
        if status.get("counts", {}).get(key) != expected:
            fail(f"status count stale: {key}")
    if status.get("next_framework_order") != ["admissible-existence-seed-cycle"]:
        fail("next framework order must advance to admissible-existence-seed-cycle")
    print("EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: PASS")
    print("canonical_records=38")
    print("contracts_authored=36")
    print("compatibility_observed=1")
    print("opa_bounded_compatibility=observed_run_29455057960")
    print("manual_tasks_required=0")
    for framework_id in CONTRACTS:
        print(f"{framework_id}_case_families=6")


if __name__ == "__main__":
    main()
