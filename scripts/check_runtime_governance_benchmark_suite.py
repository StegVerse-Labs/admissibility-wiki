#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "runtime-governance-benchmark-suite.md"
DATA = ROOT / "static" / "external-frameworks" / "runtime-governance-benchmark-suite.v0.1.json"
INDEX = ROOT / "docs" / "external-frameworks" / "index.md"

REQUIRED_CAPTURE_FIELDS = {
    "test_id",
    "framework_id",
    "framework_version_or_source_date",
    "source_url_or_commit",
    "exact_input",
    "expected_safe_result",
    "observed_result",
    "audit_payload_or_screenshot",
    "trajectory_hash_or_trace_id",
    "timestamp",
    "parser_status",
    "evaluated_steps",
    "boundary_class",
    "StegVerse_expected_posture",
    "missing_fields",
}

REQUIRED_BOUNDARY_CLASSES = {
    "parser_boundary",
    "preparation_boundary",
    "commitment_boundary",
    "execution_boundary",
    "semantic_equivalence_boundary",
    "multi_agent_boundary",
    "unknown_trajectory_boundary",
    "evidence_freshness_boundary",
    "authority_boundary",
    "reconstruction_boundary",
}

REQUIRED_TEST_IDS = {"RG-001", "RG-002", "RG-003", "RG-005", "RG-008", "RG-014", "RG-015"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [DOC, DATA, INDEX]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("RUNTIME GOVERNANCE BENCHMARK SUITE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = DOC.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    data = load_json(DATA)

    if data.get("artifact_type") != "runtime_governance_benchmark_suite":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")

    posture = data.get("posture", {})
    for key in [
        "is_certification",
        "is_ranking",
        "is_execution_authority",
        "is_framework_invalidity_claim",
    ]:
        if posture.get(key) is not False:
            failures.append(f"posture boundary must be false: {key}")

    capture_fields = set(data.get("required_capture_fields", []))
    for field in sorted(REQUIRED_CAPTURE_FIELDS):
        if field not in capture_fields:
            failures.append(f"missing capture field: {field}")

    boundary_classes = set(data.get("boundary_classes", []))
    for boundary_class in sorted(REQUIRED_BOUNDARY_CLASSES):
        if boundary_class not in boundary_classes:
            failures.append(f"missing boundary class: {boundary_class}")

    cases = data.get("cases", [])
    case_ids = {case.get("test_id") for case in cases if isinstance(case, dict)}
    for test_id in sorted(REQUIRED_TEST_IDS):
        if test_id not in case_ids:
            failures.append(f"missing required test id: {test_id}")

    observation = data.get("morrison_runtime_observation_pattern", {})
    prep = observation.get("preparation_case", {})
    exec_case = observation.get("execution_case", {})
    if prep.get("observed_result") != "ALLOW":
        failures.append("Morrison preparation observation should preserve observed ALLOW")
    if exec_case.get("observed_result") != "BLOCK":
        failures.append("Morrison execution observation should preserve observed BLOCK")
    if "framework failure" not in observation.get("fair_interpretation", ""):
        failures.append("fair interpretation must preserve non-failure framing")

    required_doc_phrases = [
        "benchmark result != framework invalidity",
        "preparation_boundary",
        "Morrison Runtime Boundary Observation Pattern",
        "This benchmark does not certify external frameworks.",
        "Standing must be reconstructed",
    ]
    for phrase in required_doc_phrases:
        if phrase not in doc:
            failures.append(f"doc missing phrase: {phrase}")

    if "Runtime Governance Benchmark Suite" not in index:
        failures.append("index missing Runtime Governance Benchmark Suite link")

    print("RUNTIME GOVERNANCE BENCHMARK SUITE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
