#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROLLOUT_MD = ROOT / "docs" / "external-frameworks" / "benchmark-mapping-rollout.md"
ROLLOUT_JSON = ROOT / "docs" / "external-frameworks" / "benchmark-mapping-rollout.json"
MAPPING_DIR = ROOT / "docs" / "external-frameworks" / "benchmark-mappings"
INDEX = ROOT / "docs" / "external-frameworks" / "index.md"

REQUIRED_DIMENSIONS = {
    "execution_boundary",
    "preparation_boundary",
    "commitment_boundary",
    "semantic_equivalence_boundary",
    "unknown_trajectory_boundary",
    "authority_boundary",
    "evidence_freshness_boundary",
    "reconstruction_boundary",
    "interoperability_path",
}

ALLOWED_MAPPING_STATES = {
    "not_started",
    "intake",
    "mapped_partial",
    "mapped_core",
    "fixture_ready",
    "replay_ready",
    "interoperability_ready",
}

MAPPING_REQUIRED_STATES = {
    "mapped_partial",
    "mapped_core",
    "fixture_ready",
    "replay_ready",
    "interoperability_ready",
}

ALLOWED_DIMENSION_STATES = {
    "applicable",
    "not_applicable",
    "adapter_required",
    "insufficient_evidence",
    "observed_partial",
    "replay_required",
    "fixture_ready",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [ROLLOUT_MD, ROLLOUT_JSON, MAPPING_DIR, INDEX]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK BENCHMARK MAPPINGS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    rollout_md = ROLLOUT_MD.read_text(encoding="utf-8")
    rollout = load_json(ROLLOUT_JSON)
    index = INDEX.read_text(encoding="utf-8")

    if rollout.get("artifact_type") != "external_framework_benchmark_mapping_rollout":
        failures.append("rollout artifact type mismatch")
    if rollout.get("schema_version") != "0.1":
        failures.append("rollout schema version mismatch")

    posture = rollout.get("posture", {})
    for key in ["is_certification", "is_ranking", "is_execution_authority", "unmapped_dimension_is_failure"]:
        if posture.get(key) is not False:
            failures.append(f"rollout posture must be false: {key}")

    for state in rollout.get("allowed_mapping_states", []):
        if state not in ALLOWED_MAPPING_STATES:
            failures.append(f"unexpected allowed mapping state: {state}")
    for state in rollout.get("allowed_dimension_states", []):
        if state not in ALLOWED_DIMENSION_STATES:
            failures.append(f"unexpected allowed dimension state: {state}")

    for dimension in REQUIRED_DIMENSIONS:
        if dimension not in rollout.get("required_dimensions", []):
            failures.append(f"rollout missing required dimension: {dimension}")

    entries = rollout.get("entries", [])
    if len(entries) < 10:
        failures.append("rollout must track broad external-framework set")
    entry_ids = {entry.get("framework_id") for entry in entries if isinstance(entry, dict)}
    for required in ["morrison-runtime", "asro", "glm", "evide", "decisionassure", "mindforge"]:
        if required not in entry_ids:
            failures.append(f"rollout missing framework id: {required}")

    mapping_paths = sorted(MAPPING_DIR.glob("*.mapping.json"))
    mappings_by_id: dict[str, dict[str, Any]] = {}
    for mapping_path in mapping_paths:
        mapping = load_json(mapping_path)
        framework_id = mapping.get("framework_id")
        if isinstance(framework_id, str):
            mappings_by_id[framework_id] = mapping

    for entry in entries:
        if not isinstance(entry, dict):
            failures.append("rollout entry must be object")
            continue
        framework_id = entry.get("framework_id")
        mapping_state = entry.get("mapping_state")
        if mapping_state not in ALLOWED_MAPPING_STATES:
            failures.append(f"rollout entry mapping state mismatch: {framework_id}")
        if mapping_state in MAPPING_REQUIRED_STATES and framework_id not in mappings_by_id:
            failures.append(f"rollout mapped framework missing companion: {framework_id}")

    for mapping_path in mapping_paths:
        mapping = load_json(mapping_path)
        framework_id = mapping.get("framework_id")
        if mapping.get("artifact_type") != "external_framework_benchmark_mapping":
            failures.append(f"mapping artifact type mismatch: {mapping_path.relative_to(ROOT)}")
        if mapping.get("schema_version") != "0.1":
            failures.append(f"mapping schema version mismatch: {mapping_path.relative_to(ROOT)}")
        if mapping.get("mapping_state") not in ALLOWED_MAPPING_STATES:
            failures.append(f"mapping state mismatch: {framework_id}")
        dimensions = mapping.get("benchmark_dimensions", {})
        for dimension in REQUIRED_DIMENSIONS:
            if dimension not in dimensions:
                failures.append(f"mapping {framework_id} missing dimension: {dimension}")
                continue
            state = dimensions[dimension].get("state") if isinstance(dimensions[dimension], dict) else None
            if state not in ALLOWED_DIMENSION_STATES:
                failures.append(f"mapping {framework_id} dimension {dimension} invalid state: {state}")
        non_claims = mapping.get("non_claims", {})
        for key, value in non_claims.items():
            if value is not False:
                failures.append(f"mapping {framework_id} non-claim must be false: {key}")
        if not mapping.get("next_required_action"):
            failures.append(f"mapping {framework_id} missing next action")

    for phrase in [
        "not_applicable != failure",
        "This rollout does not certify external frameworks.",
        "Standing must be reconstructed",
    ]:
        if phrase not in rollout_md:
            failures.append(f"rollout doc missing phrase: {phrase}")

    if "Runtime Governance Benchmark Suite" not in index:
        failures.append("index missing benchmark suite reference")

    print("EXTERNAL FRAMEWORK BENCHMARK MAPPINGS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
