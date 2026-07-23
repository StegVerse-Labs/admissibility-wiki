#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "ADMISSIBILITY_AUTOMATION_HANDOFF.md"
MESH_CHECK = ROOT / "scripts" / "check_documentation_mesh_status.py"
ST016_PROMOTION_CHECK = ROOT / "scripts" / "check_st016_promotion_bundle.py"
RUN_RECEIPT_CHECK = ROOT / "scripts" / "check_automated_transition_run_receipt.py"
CONCEPTUAL_INHERITANCE_CHECK = ROOT / "scripts" / "check_conceptual_inheritance_claims.py"
CONCEPTUAL_INHERITANCE_STATUS_CHECK = ROOT / "scripts" / "check_conceptual_inheritance_status.py"
CONCEPTUAL_INHERITANCE_PUBLICATION_CHECK = ROOT / "scripts" / "check_conceptual_inheritance_publication.py"
CONCEPTUAL_INHERITANCE_PROPAGATION_CHECK = ROOT / "scripts" / "check_conceptual_inheritance_propagation_plan.py"
ORIGINAL_DRAWING_PUBLICATION_CHECK = ROOT / "scripts" / "check_original_drawing_publication.py"
OPTIMIZATION_TARGET_BINDING_CHECK = ROOT / "scripts" / "check_optimization_target_binding_at_commit.py"
OPTIMIZATION_TARGET_PUBLICATION_CHECK = ROOT / "scripts" / "check_optimization_target_binding_publication.py"
AI_LED_RADIOLOGY_CHECK = ROOT / "scripts" / "check_ai_led_radiology_execution.py"
AI_LED_RADIOLOGY_PUBLICATION_CHECK = ROOT / "scripts" / "check_ai_led_radiology_publication.py"
AI_LED_RADIOLOGY_HANDOFF_SYNC_CHECK = ROOT / "scripts" / "check_ai_led_radiology_handoff_sync.py"
VERIFICATION_EXECUTION_AUTHORITY_CHECK = ROOT / "scripts" / "check_verification_execution_authority.py"
COMMIT_BOUNDARY_BINDING_CHECK = ROOT / "scripts" / "check_commit_boundary_binding.py"
QUANTUM_SECURITY_PUBLICATION_CHECK = ROOT / "scripts" / "check_quantum_resilient_security_publication.py"
PEER_PRESERVATION_CHECK = ROOT / "scripts" / "check_peer_preservation_claims.py"
ROBOTIC_LAW_ENFORCEMENT_CHECK = ROOT / "scripts" / "check_robotic_law_enforcement_admissibility.py"
DISCOVERY_GOVERNANCE_HANDOFF_CHECK = ROOT / "scripts" / "check_discovery_governance_handoff.py"
DISCOVERY_GOVERNANCE_PROOF_RECEIPT_CHECK = ROOT / "scripts" / "check_discovery_governance_proof_receipt.py"
DISCOVERY_GOVERNANCE_PUBLICATION_CHECK = ROOT / "scripts" / "check_discovery_governance_publication.py"
DISCOVERY_GOVERNANCE_ACTIVATION_EVIDENCE_CONTRACT_CHECK = ROOT / "scripts" / "check_discovery_governance_activation_evidence_contract.py"
DISCOVERY_GOVERNANCE_ACTIVATION_EVIDENCE_RUNTIME_CHECK = ROOT / "scripts" / "check_discovery_governance_activation_evidence_runtime.py"
DISCOVERY_GOVERNANCE_HANDOFF_SYNC_CHECK = ROOT / "scripts" / "check_discovery_governance_handoff_sync.py"
GLOSSARY_CONSISTENCY_CHECK = ROOT / "scripts" / "check_glossary_consistency.py"
ACTIVATION_SECTION_CHECK = ROOT / "scripts" / "check_activation_section.py"
RESEARCH_SOCIAL_STEGVERSE_CHECK = ROOT / "scripts" / "check_research_social_stegverse_sections.py"
NAVIGATION_COVERAGE_CHECK = ROOT / "scripts" / "check_navigation_coverage.py"
RELEASE_READINESS_CHECK = ROOT / "scripts" / "check_release_readiness.py"
ECOSYSTEM_CHAT_ACTIVATION_CHECK = ROOT / "scripts" / "check_ecosystem_chat_activation_projection.py"
ASRO_BOUNDED_COMPARISON_CHECK = ROOT / "scripts" / "check_asro_bounded_comparison.py"
RECIPROCAL_FRAMEWORK_CHECK = ROOT / "scripts" / "check_reciprocal_framework_evaluations.py"
RECIPROCAL_SYMMETRY_CHECK = ROOT / "scripts" / "check_reciprocal_boundary_symmetry.py"
RECIPROCAL_REPLAY_CHECK = ROOT / "scripts" / "check_reciprocal_evaluation_replay.py"
REQUIRED = (
    "scripts/check_ios_workflow_mirror_status.py",
    "static/status/ios-workflow-mirror-status.json",
    "validate:ios-workflow-mirror",
    "canonical workflow remains source of truth",
    "schemas/automated-transition-run-receipt.schema.json",
    "examples/automated-transition-run-receipt.json",
    "Master-Records",
    "optimization-target-binding-at-commit",
    "static/status/optimization-target-binding-publication-verification.json",
)


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return
    result = subprocess.run(
        [sys.executable, str(path)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    print(result.stdout.rstrip())
    if result.returncode != 0:
        failures.append(f"{label} validation failed")


def main() -> int:
    failures: list[str] = []
    if not HANDOFF.exists():
        failures.append("missing ADMISSIBILITY_AUTOMATION_HANDOFF.md")
    else:
        text = HANDOFF.read_text(encoding="utf-8")
        failures.extend(f"missing marker: {marker}" for marker in REQUIRED if marker not in text)

    checks = (
        (MESH_CHECK, "documentation mesh"),
        (ST016_PROMOTION_CHECK, "ST-016 promotion bundle"),
        (RUN_RECEIPT_CHECK, "automated transition run receipt"),
        (CONCEPTUAL_INHERITANCE_CHECK, "conceptual inheritance claims"),
        (CONCEPTUAL_INHERITANCE_STATUS_CHECK, "conceptual inheritance activation status"),
        (CONCEPTUAL_INHERITANCE_PUBLICATION_CHECK, "conceptual inheritance publication gate"),
        (CONCEPTUAL_INHERITANCE_PROPAGATION_CHECK, "conceptual inheritance propagation plan"),
        (ORIGINAL_DRAWING_PUBLICATION_CHECK, "original drawing publication"),
        (OPTIMIZATION_TARGET_BINDING_CHECK, "optimization target binding at commit"),
        (OPTIMIZATION_TARGET_PUBLICATION_CHECK, "optimization target binding publication gate"),
        (AI_LED_RADIOLOGY_CHECK, "AI-led radiology execution boundary"),
        (AI_LED_RADIOLOGY_PUBLICATION_CHECK, "AI-led radiology publication gate"),
        (AI_LED_RADIOLOGY_HANDOFF_SYNC_CHECK, "AI-led radiology handoff sync"),
        (VERIFICATION_EXECUTION_AUTHORITY_CHECK, "verification versus execution authority"),
        (COMMIT_BOUNDARY_BINDING_CHECK, "commit-boundary binding predicate"),
        (QUANTUM_SECURITY_PUBLICATION_CHECK, "quantum-resilient security publication"),
        (PEER_PRESERVATION_CHECK, "peer-preservation inference boundary"),
        (ROBOTIC_LAW_ENFORCEMENT_CHECK, "robotic law-enforcement deployment admissibility"),
        (DISCOVERY_GOVERNANCE_HANDOFF_CHECK, "discovery-to-governance minimum handoff"),
        (DISCOVERY_GOVERNANCE_PROOF_RECEIPT_CHECK, "discovery-to-governance proof receipt"),
        (DISCOVERY_GOVERNANCE_PUBLICATION_CHECK, "discovery-to-governance publication contract"),
        (DISCOVERY_GOVERNANCE_ACTIVATION_EVIDENCE_CONTRACT_CHECK, "discovery-to-governance activation evidence contract"),
        (DISCOVERY_GOVERNANCE_ACTIVATION_EVIDENCE_RUNTIME_CHECK, "discovery-to-governance activation evidence runtime"),
        (DISCOVERY_GOVERNANCE_HANDOFF_SYNC_CHECK, "discovery-to-governance handoff synchronization"),
        (GLOSSARY_CONSISTENCY_CHECK, "glossary consistency"),
        (ACTIVATION_SECTION_CHECK, "activation section"),
        (RESEARCH_SOCIAL_STEGVERSE_CHECK, "research social and StegVerse sections"),
        (NAVIGATION_COVERAGE_CHECK, "navigation and orphan coverage"),
        (ECOSYSTEM_CHAT_ACTIVATION_CHECK, "Ecosystem Chat activation projection"),
        (ASRO_BOUNDED_COMPARISON_CHECK, "ASRO bounded comparison"),
        (RECIPROCAL_FRAMEWORK_CHECK, "reciprocal framework evaluations"),
        (RECIPROCAL_SYMMETRY_CHECK, "reciprocal boundary symmetry"),
        (RECIPROCAL_REPLAY_CHECK, "reciprocal evaluation replay"),
        (RELEASE_READINESS_CHECK, "release readiness"),
    )
    for path, label in checks:
        run_check(path, label, failures)

    if failures:
        print("ADMISSIBILITY AUTOMATION HANDOFF: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ADMISSIBILITY AUTOMATION HANDOFF: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
