#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_discovery_governance_activation_evidence.py"
SCHEMA = ROOT / "static" / "schemas" / "discovery-governance-activation-evidence-receipt.schema.json"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
HANDOFF = ROOT / "docs" / "DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md"

WRITER_MARKERS = (
    'discovery_governance_activation_evidence_receipt.v1',
    'ACTIVATION_EVIDENCE_COMPLETE',
    'ACTIVATION_EVIDENCE_FAIL_CLOSED',
    'DISCOVERY_WORKFLOW_DEPENDENCIES_SATISFIED',
    'canonical validation/build/deploy dependency chain not asserted by workflow',
    'standalone publication receipt differs from embedded closure',
    'receipt repository/run identity mismatch',
    'fixture_sha256',
    'all_required_public_routes_verified',
    'publication_complete',
)

WORKFLOW_MARKERS = (
    'DISCOVERY_WORKFLOW_DEPENDENCIES_SATISFIED: "true"',
    'python scripts/check_discovery_governance_activation_closure.py',
    'python scripts/write_discovery_governance_activation_evidence.py',
    'reports/discovery-governance-activation-evidence-receipt.json',
    'name: public-activation-receipt',
    'if-no-files-found: error',
)

FALSE_FIELDS = (
    'consent_granted', 'standing_granted', 'authority_granted',
    'admissibility_granted', 'commitment_granted',
    'execution_permission_granted', 'certification_granted',
    'endorsement_granted', 'interoperability_verified',
    'release_authority_granted', 'downstream_mutation_authority_granted',
    'user_manual_action_required',
)


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
    require_markers(WRITER, WRITER_MARKERS, "activation evidence writer", failures)
    require_markers(WORKFLOW, WORKFLOW_MARKERS, "canonical workflow", failures)

    if not SCHEMA.exists():
        failures.append(f"missing {SCHEMA.relative_to(ROOT)}")
    else:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        for field in (
            'schema', 'goal_id', 'repository', 'state',
            'canonical_dependency_chain_observed', 'proof_receipt',
            'publication_receipt', 'public_activation_receipt', 'failures',
        ):
            if field not in required:
                failures.append(f"activation evidence schema must require {field}")
        if properties.get('schema', {}).get('const') != 'discovery_governance_activation_evidence_receipt.v1':
            failures.append('activation evidence schema identifier mismatch')
        if set(properties.get('state', {}).get('enum', [])) != {
            'ACTIVATION_EVIDENCE_COMPLETE', 'ACTIVATION_EVIDENCE_FAIL_CLOSED'
        }:
            failures.append('activation evidence schema state enum mismatch')
        for field in FALSE_FIELDS:
            if properties.get(field, {}).get('const') is not False:
                failures.append(f"activation evidence schema must force {field}=false")

        proof = properties.get('proof_receipt', {}).get('properties', {})
        publication = properties.get('publication_receipt', {}).get('properties', {})
        public_activation = properties.get('public_activation_receipt', {}).get('properties', {})
        if proof.get('path', {}).get('const') != 'reports/discovery-governance-handoff-proof-receipt.json':
            failures.append('proof receipt path contract mismatch')
        if publication.get('path', {}).get('const') != 'reports/discovery-governance-publication-receipt.json':
            failures.append('publication receipt path contract mismatch')
        if public_activation.get('path', {}).get('const') != 'reports/public-activation-receipt.json':
            failures.append('public activation receipt path contract mismatch')

    if not HANDOFF.exists():
        failures.append(f"missing {HANDOFF.relative_to(ROOT)}")

    if failures:
        print('DISCOVERY GOVERNANCE ACTIVATION EVIDENCE CONTRACT: FAIL')
        for failure in failures:
            print(f'- {failure}')
        return 1
    print('DISCOVERY GOVERNANCE ACTIVATION EVIDENCE CONTRACT: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
