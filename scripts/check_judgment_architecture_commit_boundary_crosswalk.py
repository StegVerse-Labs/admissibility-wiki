#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "docs/external-frameworks/fixtures/judgment-architecture-commit-boundary-crosswalk.v0.1.json"
SOURCE_SCHEMA = ROOT / "static/schemas/decision-commitment-record-candidate.schema.json"
TARGET_SCHEMA = ROOT / "static/schemas/commit-boundary-binding-record.schema.json"

REQUIRED_BINDINGS = {
    "record_id",
    "decision_maker",
    "authority_basis",
    "evidence_refs",
    "decision_criteria",
    "stop_mechanism",
    "recoverability_profile.rollback_test_receipt",
    "recoverability_profile.validity_window",
}

REQUIRED_DERIVATIONS = {
    "candidate_hash",
    "state_before_hash",
    "state_after_hash",
    "decision_validity",
    "origin.result",
    "authority.result",
    "admissibility.result",
    "invariants.result",
    "recoverability.margin",
    "recoverability.minimum_margin",
    "evidence.result",
    "binding_result",
    "reason_codes",
}


def main() -> int:
    failures: list[str] = []
    for path in (CROSSWALK, SOURCE_SCHEMA, TARGET_SCHEMA):
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")
    if failures:
        print("JUDGMENT ARCHITECTURE COMMIT-BOUNDARY CROSSWALK: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    data = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "judgment_architecture_commit_boundary_crosswalk":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("classification") != "DOCUMENTED_ARCHITECTURAL_ALIGNMENT":
        failures.append("classification must remain documented alignment")
    if data.get("authority_effect") != "NONE":
        failures.append("authority effect must be NONE")
    if data.get("default_posture") != "FAIL_CLOSED_UNTIL_BINDING_PREDICATE_INDEPENDENTLY_PASSES":
        failures.append("default posture must fail closed")

    bindings = {item.get("source") for item in data.get("field_bindings", []) if isinstance(item, dict)}
    for required in REQUIRED_BINDINGS:
        if required not in bindings:
            failures.append(f"missing source binding: {required}")

    derivations = set(data.get("required_independent_derivations", []))
    for required in REQUIRED_DERIVATIONS:
        if required not in derivations:
            failures.append(f"missing independent derivation: {required}")

    for key, value in data.get("non_claims", {}).items():
        if value is not False:
            failures.append(f"non-claim must be false: {key}")

    print("JUDGMENT ARCHITECTURE COMMIT-BOUNDARY CROSSWALK:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
