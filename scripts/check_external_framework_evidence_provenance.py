#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "external-frameworks"
REGISTRY = DOCS / "index.json"
ROLLOUT = DOCS / "evidence-provenance-rollout.json"
SUPPLEMENT = ROOT / "static" / "external-frameworks" / "evidence-provenance-rollout-supplement.v1.json"

REQUIRED_STANDARD_FILES = [DOCS / "evaluation-standard.md", DOCS / "failure-class-catalog.md", DOCS / "external-framework-template.md", DOCS / "EXPANSION_POLICY.json", DOCS / "evidence-provenance-rollout.md", ROLLOUT, SUPPLEMENT]
REQUIRED_INDEX_LINKS = ["./evaluation-standard.md", "./failure-class-catalog.md", "./external-framework-template.md", "./evidence-provenance-rollout.md"]
REQUIRED_STANDARD_TERMS = ["Evidence Provenance", "Claim Traceability Rule", "Comparative Fairness Rule", "Observed Behavior Rule", "Required Runtime Result Artifact Set", "Machine-Readable Companion Requirement"]
REQUIRED_FAILURE_CLASSES = ["FC-001", "Semantic Equivalence Divergence", "FC-007", "Fail-Open Runtime Error", "FC-012", "Evidence Class Confusion"]
REQUIRED_TEMPLATE_SECTIONS = ["## Evidence Provenance", "## Parameterized Test Cases", "## StegVerse Analysis", "## Failure Classes", "## Non-Claims"]
COMMON_PROVENANCE_TERMS = ["## Evidence Provenance", "Official Framework Sources", "Official Implementation Sources", "Observed Behavior", "Reproduced Behavior", "StegVerse Analysis", "Interoperability Assessment", "Standing"]
GUIDANCE_TERMS = COMMON_PROVENANCE_TERMS + ["F1:", "S1:", "S2:", "H1:", "not_applicable_for_runtime_result"]
ARTIFACT_TERMS = COMMON_PROVENANCE_TERMS + ["F1:", "F2:", "S1:", "S2:", "H1:"]

BATCH_PAGE_REQUIREMENTS = {
    "batch_1": {
        "glm": {"path": DOCS / "glm.md", "terms": COMMON_PROVENANCE_TERMS + ["F1:", "S1:", "S2:"]},
        "evide": {"path": DOCS / "evide.md", "terms": COMMON_PROVENANCE_TERMS + ["F1:", "S1:", "S2:"]},
        "morrison-runtime": {"path": DOCS / "morrison-runtime.md", "terms": ["Evidence Provenance", "Parameterized Boundary Case", "Semantic Value Movement Versus Tool Label", "FC-001", "raw audit payload", "timestamp"]},
    },
    "batch_2": {
        "decisionassure": {"path": DOCS / "decisionassure.md", "terms": COMMON_PROVENANCE_TERMS + ["artifact_package_required", "S1:", "S2:", "H1:"]},
        "mindforge": {"path": DOCS / "mindforge.md", "terms": COMMON_PROVENANCE_TERMS + ["artifact_package_required", "S1:", "S2:", "H1:"]},
        "asro": {"path": DOCS / "asro.md", "terms": COMMON_PROVENANCE_TERMS + ["F1:", "F2:", "V1:", "S1:", "S2:"]},
    },
    "batch_3": {
        "mitre-atlas": {"path": DOCS / "mitre-atlas.md", "terms": GUIDANCE_TERMS + ["threat_context_crosswalk"]},
        "owasp-top-10-llm": {"path": DOCS / "owasp-top-10-llm.md", "terms": GUIDANCE_TERMS + ["risk_category_crosswalk"]},
        "nist-ai-rmf": {"path": DOCS / "nist-ai-rmf.md", "terms": GUIDANCE_TERMS + ["risk_management_crosswalk"]},
        "iso-iec-42001": {"path": DOCS / "iso-iec-42001.md", "terms": GUIDANCE_TERMS + ["ai_management_system_crosswalk"]},
        "eu-ai-act": {"path": DOCS / "eu-ai-act.md", "terms": GUIDANCE_TERMS + ["legal_obligation_crosswalk"]},
    },
    "batch_4": {
        "policy-cards": {"path": DOCS / "policy-cards.md", "terms": ARTIFACT_TERMS + ["runtime_policy_artifact_crosswalk"]},
        "runtime-governance-for-ai-agents": {"path": DOCS / "runtime-governance-policies-on-paths.md", "terms": ARTIFACT_TERMS + ["runtime_path_governance_crosswalk"]},
        "agent-governance-playbook": {"path": DOCS / "agent-governance-playbook.md", "terms": ARTIFACT_TERMS + ["agent_continuation_crosswalk"]},
        "emergency-stop-convention": {"path": DOCS / "killswitch-md.md", "terms": ARTIFACT_TERMS + ["emergency_stop_fail_closed_crosswalk"]},
        "care-runtime": {"path": DOCS / "care-runtime.md", "terms": COMMON_PROVENANCE_TERMS + ["missing_or_unconfirmed", "O1:", "S1:", "S2:", "H1:"]},
        "aar": {"path": DOCS / "aar.md", "terms": ARTIFACT_TERMS + ["provisional_crosswalk_with_page_provenance"]},
    },
}
REQUIRED_ROLLOUT_ENTRY_FIELDS = ["framework_id", "name", "page", "source_status", "official_framework_sources", "official_implementation_sources", "observed_behavior", "reproduced_behavior", "stegverse_analysis", "interoperability_assessment", "standing", "next_action"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def main() -> int:
    failures: list[str] = []
    for path in REQUIRED_STANDARD_FILES + [REGISTRY]:
        if not path.exists():
            failures.append(f"missing standard file: {path.relative_to(ROOT)}")
    for batch_id, requirements in BATCH_PAGE_REQUIREMENTS.items():
        for framework_id, requirement in requirements.items():
            if not requirement["path"].exists():
                failures.append(f"missing {batch_id} page: {framework_id}: {requirement['path'].relative_to(ROOT)}")
    if failures:
        print("EXTERNAL FRAMEWORK EVIDENCE PROVENANCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    index = read(DOCS / "index.md")
    standard = read(DOCS / "evaluation-standard.md")
    catalog = read(DOCS / "failure-class-catalog.md")
    template = read(DOCS / "external-framework-template.md")
    rollout_page = read(DOCS / "evidence-provenance-rollout.md")
    rollout = load_json(ROLLOUT)
    supplement = load_json(SUPPLEMENT)
    registry = load_json(REGISTRY)

    for link in REQUIRED_INDEX_LINKS:
        if link not in index:
            failures.append(f"index missing link: {link}")
    for term in REQUIRED_STANDARD_TERMS:
        if term not in standard:
            failures.append(f"evaluation standard missing term: {term}")
    for term in REQUIRED_FAILURE_CLASSES:
        if term not in catalog:
            failures.append(f"failure catalog missing term: {term}")
    for section in REQUIRED_TEMPLATE_SECTIONS:
        if section not in template:
            failures.append(f"template missing section: {section}")
    for batch_id, requirements in BATCH_PAGE_REQUIREMENTS.items():
        for framework_id, requirement in requirements.items():
            content = read(requirement["path"])
            for term in requirement["terms"]:
                if term not in content:
                    failures.append(f"{batch_id} page {framework_id} missing term: {term}")
    for term in ["First-Pass Rollout Matrix", "Batch 1", "Batch 5"]:
        if term not in rollout_page:
            failures.append(f"rollout page missing term: {term}")
    if rollout.get("artifact_type") != "external_framework_evidence_provenance_rollout":
        failures.append("rollout artifact_type mismatch")
    if rollout.get("schema_version") != "0.1":
        failures.append("rollout schema_version mismatch")
    if supplement.get("schema") != "external_framework_evidence_provenance_rollout_supplement.v1":
        failures.append("supplement schema mismatch")
    if supplement.get("base_rollout") != "docs/external-frameworks/evidence-provenance-rollout.json":
        failures.append("supplement base rollout reference mismatch")

    registry_ids = [entry.get("framework_id") for entry in registry.get("entries", [])]
    base_entries = rollout.get("entries", [])
    supplemental_entries = supplement.get("entries", [])
    all_entries = [*base_entries, *supplemental_entries]
    rollout_ids = [entry.get("framework_id") for entry in all_entries]
    if len(rollout_ids) != len(set(rollout_ids)):
        failures.append("combined rollout contains duplicate framework_id entries")
    for framework_id in sorted(set(registry_ids) - set(rollout_ids)):
        failures.append(f"registry framework missing from rollout: {framework_id}")
    for framework_id in sorted(set(rollout_ids) - set(registry_ids)):
        failures.append(f"rollout framework not found in registry: {framework_id}")
    for entry in all_entries:
        framework_id = entry.get("framework_id", "UNKNOWN")
        for field in REQUIRED_ROLLOUT_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"rollout entry {framework_id} missing field: {field}")
        page = entry.get("page")
        if isinstance(page, str) and page.startswith("docs/external-frameworks/") and not (ROOT / page).exists():
            failures.append(f"rollout entry {framework_id} page does not exist: {page}")
    if supplement.get("counts", {}).get("records") != len(supplemental_entries):
        failures.append("supplement records count is stale")
    if "does not certify compatibility" not in supplement.get("boundary", ""):
        failures.append("supplement boundary must prohibit compatibility certification")

    for batch_id in ["batch_1", "batch_2", "batch_3", "batch_4"]:
        if rollout.get("batch_status", {}).get(batch_id) != "PAGE_PROVENANCE_SECTIONS_INSTALLED":
            failures.append(f"rollout {batch_id} status must be PAGE_PROVENANCE_SECTIONS_INSTALLED")
    boundary = rollout.get("global_boundary", {})
    for key in ["rollout_is_certification", "rollout_is_endorsement", "rollout_is_execution_authority", "compatibility_is_certification", "observed_behavior_generalized_beyond_captured_evidence"]:
        if boundary.get(key) is not False:
            failures.append(f"rollout boundary must be false: {key}")
    morrison = read(DOCS / "morrison-runtime.md")
    for fragment in ["| 1 | ALLOW | BLOCK | False allow", "| Test | Observed Result | StegVerse Expected Result | Validation Meaning |"]:
        if fragment in morrison:
            failures.append("Morrison page still contains unsupported historical public result table")

    print("EXTERNAL FRAMEWORK EVIDENCE PROVENANCE:", "FAIL" if failures else "PASS")
    print(f"base_rollout_records={len(base_entries)}")
    print(f"supplemental_rollout_records={len(supplemental_entries)}")
    print(f"combined_rollout_records={len(all_entries)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
