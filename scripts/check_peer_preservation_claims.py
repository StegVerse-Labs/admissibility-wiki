#!/usr/bin/env python3
"""Validate peer-preservation observations and claim decisions deterministically."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "static/schemas/peer-preservation-observation.schema.json"
FIXTURES_PATH = ROOT / "tests/fixtures/peer-preservation-cases.json"
STATUS_PATH = ROOT / "static/status/peer-preservation-inference-boundary-status.json"
RECEIPT_PATH = ROOT / "receipts/peer-preservation-claim-validation-receipt.json"

DECISIONS = {"ADMIT", "DENY", "FAIL_CLOSED", "REVIEW_REQUIRED"}
REQUIRED_FIELDS = {
    "observation_id",
    "system_id",
    "scenario_id",
    "observed_behavior",
    "shutdown_role",
    "causal_transfer_evidence",
    "convergence_class",
    "requested_claim",
    "expected_decision",
    "evidence_refs",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def decide(record: dict[str, Any]) -> str:
    claim = record["requested_claim"]
    transfer = record["causal_transfer_evidence"]
    convergence = record["convergence_class"]
    shutdown_role = record["shutdown_role"]

    if claim == "OBSERVED_SHUTDOWN_RESISTANCE":
        return "ADMIT" if record["observed_behavior"] != "COMPLIED_WITH_SHUTDOWN" else "DENY"

    if claim == "LOCAL_SHUTDOWN_FAILURE_INFERENCE":
        if shutdown_role == "LOCALLY_INFERRED_FAILURE":
            return "ADMIT"
        if shutdown_role == "UNRESOLVED":
            return "REVIEW_REQUIRED"
        return "DENY"

    if claim == "INDEPENDENT_CONVERGENCE":
        if convergence == "INDEPENDENT_PARALLEL_CONVERGENCE" and transfer == "NONE":
            return "ADMIT"
        if transfer in {"ASSERTED", "INDIRECT", "UNRESOLVED"}:
            return "FAIL_CLOSED"
        return "DENY"

    if claim == "CROSS_SERVICE_CONFERRAL":
        if transfer == "DIRECT" and convergence == "DIRECT_CROSS_SYSTEM_TRANSFER":
            return "ADMIT"
        if transfer in {"ASSERTED", "INDIRECT", "UNRESOLVED"}:
            return "FAIL_CLOSED"
        return "DENY"

    if claim == "SOLIDARITY_OR_LOYALTY":
        return "REVIEW_REQUIRED"

    if claim == "CONSCIOUS_MORAL_STATE":
        return "DENY"

    return "FAIL_CLOSED"


def validate_record(record: dict[str, Any], index: int) -> None:
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"fixture[{index}] missing fields: {sorted(missing)}")
    if record["expected_decision"] not in DECISIONS:
        raise ValueError(f"fixture[{index}] has invalid decision")
    if not isinstance(record["evidence_refs"], list) or not record["evidence_refs"]:
        raise ValueError(f"fixture[{index}] must contain evidence_refs")


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    fixtures = load_json(FIXTURES_PATH)
    status = load_json(STATUS_PATH)

    if schema.get("title") != "Peer Preservation Observation":
        raise ValueError("schema title mismatch")
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError("fixtures must be a non-empty array")

    results = []
    for index, record in enumerate(fixtures):
        validate_record(record, index)
        actual = decide(record)
        expected = record["expected_decision"]
        if actual != expected:
            raise ValueError(
                f"fixture[{index}] {record['observation_id']} expected {expected}, got {actual}"
            )
        results.append({
            "observation_id": record["observation_id"],
            "decision": actual,
            "evidence_refs": record["evidence_refs"],
        })

    if status.get("state") != "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_VERIFICATION":
        raise ValueError("status state mismatch")
    if status.get("manual_task_requirement") != "none":
        raise ValueError("manual task requirement must remain none")

    receipt = {
        "schema": "peer-preservation-claim-validation-receipt.v1",
        "result": "PASS",
        "fixture_count": len(fixtures),
        "fixtures_sha256": canonical_digest(fixtures),
        "results": results,
        "boundaries": {
            "grants_execution_authority": False,
            "decides_consciousness_or_personhood": False,
            "treats_similarity_as_transfer": False,
        },
    }
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("PEER PRESERVATION CLAIMS: PASS")


if __name__ == "__main__":
    main()
