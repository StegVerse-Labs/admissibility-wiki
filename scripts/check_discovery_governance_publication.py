#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT_CHECKER = ROOT / "scripts" / "check_governed_llm_deployment_status.py"
PUBLIC_RECEIPT_WRITER = ROOT / "scripts" / "write-public-activation-receipt.mjs"
PUBLIC_RECEIPT_WRITER_TEST = ROOT / "scripts" / "check-public-activation-receipt-writer.mjs"
ACTIVATION_CLOSURE_CHECKER = ROOT / "scripts" / "check_discovery_governance_activation_closure.py"
ACTIVATION_EVIDENCE_WRITER = ROOT / "scripts" / "write_discovery_governance_activation_evidence.py"
CANONICAL_WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
STATUS = ROOT / "static" / "status" / "discovery-governance-handoff-status.json"
DOCTRINE = ROOT / "docs" / "formalisms" / "discovery-governance-minimum-handoff.md"
SCHEMA = ROOT / "static" / "schemas" / "discovery-governance-handoff.schema.json"
PUBLICATION_SCHEMA = ROOT / "static" / "schemas" / "discovery-governance-publication-receipt.schema.json"
ACTIVATION_EVIDENCE_SCHEMA = ROOT / "static" / "schemas" / "discovery-governance-activation-evidence-receipt.schema.json"
EXAMPLE = ROOT / "static" / "examples" / "discovery-governance-handoff.example.json"
HANDOFF = ROOT / "docs" / "DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md"

DEPLOYMENT_MARKERS = (
    '"discovery_governance_doctrine"', '"discovery_governance_schema"',
    '"discovery_governance_status"', '"discovery_governance_example"',
    '"discovery_governance_publication_receipt_schema"',
    'discovery-governance-publication-receipt.json',
    'discovery_governance_publication_receipt.v1',
    'DOCUMENTED_ARCHITECTURAL_ALIGNMENT', 'implementation_equivalence_established',
    'interoperability_verified', 'consent_granted', 'admissibility_granted',
    'execution_permission_granted', 'downstream_mutation_authority_granted',
)

WRITER_MARKERS = (
    "const discoveryReceiptPath = 'reports/discovery-governance-publication-receipt.json'",
    "discovery_governance: discoveryReceipt",
    "discovery_governance_publication_receipt: discoveryReceiptPath",
    "discoveryReceipt.all_required_public_routes_verified === true",
    "A discovery handoff does not grant consent, standing, authority, admissibility, commitment, execution permission, certification, or endorsement.",
)

WRITER_TEST_MARKERS = (
    "const DISCOVERY_RECEIPT = 'reports/discovery-governance-publication-receipt.json'",
    "const DISCOVERY_ROUTES = [",
    "embedded discovery closure differs from standalone receipt",
    "discovery-governance receipt binding mismatch",
    "discovery-governance boundary mismatch",
)

ACTIVATION_CLOSURE_MARKERS = (
    'embedded discovery closure does not exactly match standalone receipt',
    'bounded route verification state does not match individual route evidence',
    'public and discovery receipt {field} mismatch',
    'public publication_complete cannot be true when discovery routes fail',
    'DISCOVERY GOVERNANCE ACTIVATION CLOSURE: PASS',
)

ACTIVATION_EVIDENCE_MARKERS = (
    'discovery_governance_activation_evidence_receipt.v1',
    'ACTIVATION_EVIDENCE_COMPLETE',
    'canonical validation/build/deploy dependency chain not asserted by workflow',
    'standalone publication receipt differs from embedded closure',
    'receipt repository/run identity mismatch',
    'release_authority_granted',
    'downstream_mutation_authority_granted',
)

WORKFLOW_MARKERS = (
    "name: discovery-governance-proof-receipt",
    "reports/discovery-governance-handoff-proof-receipt.json",
    "Download discovery governance proof receipt",
    "Verify discovery governance activation closure",
    "Write discovery governance activation evidence receipt",
    "DISCOVERY_WORKFLOW_DEPENDENCIES_SATISFIED: 'true'",
    "reports/discovery-governance-activation-evidence-receipt.json",
    "reports/discovery-governance-publication-receipt.json",
    "name: public-activation-receipt",
    "if-no-files-found: error",
)

REQUIRED_NON_AUTHORITY = {
    "CONSENT", "STANDING", "AUTHORITY", "ADMISSIBILITY", "COMMITMENT",
    "EXECUTION_PERMISSION", "CERTIFICATION", "ENDORSEMENT",
}


def require_markers(path: Path, markers: tuple[str, ...], label: str, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            failures.append(f"{label} missing marker: {marker}")


def main() -> int:
    failures: list[str] = []
    for path in (
        STATUS, DOCTRINE, SCHEMA, PUBLICATION_SCHEMA,
        ACTIVATION_EVIDENCE_SCHEMA, EXAMPLE, HANDOFF,
    ):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    require_markers(DEPLOYMENT_CHECKER, DEPLOYMENT_MARKERS, "deployment checker", failures)
    require_markers(PUBLIC_RECEIPT_WRITER, WRITER_MARKERS, "public receipt writer", failures)
    require_markers(PUBLIC_RECEIPT_WRITER_TEST, WRITER_TEST_MARKERS, "public receipt writer test", failures)
    require_markers(ACTIVATION_CLOSURE_CHECKER, ACTIVATION_CLOSURE_MARKERS, "activation closure checker", failures)
    require_markers(ACTIVATION_EVIDENCE_WRITER, ACTIVATION_EVIDENCE_MARKERS, "activation evidence writer", failures)
    require_markers(CANONICAL_WORKFLOW, WORKFLOW_MARKERS, "canonical workflow", failures)

    if STATUS.exists():
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        if status.get("goal_id") != "discovery-governance-minimum-handoff":
            failures.append("status goal_id mismatch")
        observation = status.get("external_observation", {})
        if observation.get("classification") != "DOCUMENTED_ARCHITECTURAL_ALIGNMENT":
            failures.append("external observation classification mismatch")
        if observation.get("implementation_equivalence") is not False:
            failures.append("implementation equivalence must remain false")
        if observation.get("interoperability_verified") is not False:
            failures.append("interoperability verification must remain false")

    if EXAMPLE.exists():
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        if example.get("schema_version") != "discovery_governance_handoff.v1":
            failures.append("public example schema_version mismatch")
        if example.get("asserted_outcome") != "REVIEW_REQUIRED":
            failures.append("public example must preserve REVIEW_REQUIRED posture")
        if example.get("authority_assertions") != []:
            failures.append("public example must contain no authority assertions")
        declarations = set(example.get("non_authority_declaration", []))
        if not REQUIRED_NON_AUTHORITY.issubset(declarations):
            failures.append("public example lacks complete non-authority declaration")
        if not example.get("unresolved_assumptions"):
            failures.append("public REVIEW_REQUIRED example must identify unresolved assumptions")

    if PUBLICATION_SCHEMA.exists():
        schema = json.loads(PUBLICATION_SCHEMA.read_text(encoding="utf-8"))
        props = schema.get("properties", {})
        for field in (
            "implementation_equivalence_established", "interoperability_verified",
            "consent_granted", "standing_granted", "authority_granted",
            "admissibility_granted", "commitment_granted",
            "execution_permission_granted", "certification_granted",
            "endorsement_granted", "downstream_mutation_authority_granted",
        ):
            if props.get(field, {}).get("const") is not False:
                failures.append(f"publication schema must force {field}=false")

    if ACTIVATION_EVIDENCE_SCHEMA.exists():
        schema = json.loads(ACTIVATION_EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
        props = schema.get("properties", {})
        for field in (
            "consent_granted", "standing_granted", "authority_granted",
            "admissibility_granted", "commitment_granted",
            "execution_permission_granted", "certification_granted",
            "endorsement_granted", "interoperability_verified",
            "release_authority_granted", "downstream_mutation_authority_granted",
            "user_manual_action_required",
        ):
            if props.get(field, {}).get("const") is not False:
                failures.append(f"activation evidence schema must force {field}=false")

    if failures:
        print("DISCOVERY GOVERNANCE PUBLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE PUBLICATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
