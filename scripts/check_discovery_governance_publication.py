#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT_CHECKER = ROOT / "scripts" / "check_governed_llm_deployment_status.py"
STATUS = ROOT / "static" / "status" / "discovery-governance-handoff-status.json"
DOCTRINE = ROOT / "docs" / "formalisms" / "discovery-governance-minimum-handoff.md"
SCHEMA = ROOT / "static" / "schemas" / "discovery-governance-handoff.schema.json"
HANDOFF = ROOT / "docs" / "DISCOVERY_GOVERNANCE_HANDOFF_MIRROR_HANDOFF.md"

REQUIRED_MARKERS = (
    '"discovery_governance_doctrine"',
    '"discovery_governance_schema"',
    '"discovery_governance_status"',
    'discovery-governance-publication-receipt.json',
    'discovery_governance_publication_receipt.v1',
    'DOCUMENTED_ARCHITECTURAL_ALIGNMENT',
    'implementation_equivalence_established',
    'interoperability_verified',
    'consent_granted',
    'admissibility_granted',
    'execution_permission_granted',
    'downstream_mutation_authority_granted',
)


def main() -> int:
    failures: list[str] = []
    for path in (DEPLOYMENT_CHECKER, STATUS, DOCTRINE, SCHEMA, HANDOFF):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if DEPLOYMENT_CHECKER.exists():
        text = DEPLOYMENT_CHECKER.read_text(encoding="utf-8")
        for marker in REQUIRED_MARKERS:
            if marker not in text:
                failures.append(f"deployment checker missing marker: {marker}")
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
    if failures:
        print("DISCOVERY GOVERNANCE PUBLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DISCOVERY GOVERNANCE PUBLICATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
