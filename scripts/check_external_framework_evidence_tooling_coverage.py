#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "evidence-tooling-coverage.v0.1.json"
EXPECTED = {
    "opa",
    "cedar-policy",
    "mcp",
    "a2a",
    "guardrails-ai",
    "llama-guard",
    "nemo-guardrails",
}


def main() -> int:
    failures: list[str] = []
    if not REGISTRY.exists():
        print("EXTERNAL FRAMEWORK EVIDENCE TOOLING COVERAGE: FAIL")
        print(f"- missing registry: {REGISTRY.relative_to(ROOT)}")
        return 1

    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "external_framework_evidence_tooling_coverage":
        failures.append("artifact_type mismatch")
    if payload.get("schema_version") != "0.1":
        failures.append("schema_version mismatch")

    rows = payload.get("coverage", [])
    ids = {row.get("framework_id") for row in rows if isinstance(row, dict)}
    if ids != EXPECTED:
        failures.append(f"framework coverage mismatch: expected={sorted(EXPECTED)} actual={sorted(ids)}")
    if len(rows) != len(EXPECTED):
        failures.append(f"expected {len(EXPECTED)} coverage rows, found {len(rows)}")

    for row in rows:
        if not isinstance(row, dict):
            failures.append("coverage row must be an object")
            continue
        framework_id = row.get("framework_id", "unknown")
        for field in ["capture_harness", "artifact_validator", "pipeline_summary", "automation_state", "observed_evidence_state"]:
            if not row.get(field):
                failures.append(f"{framework_id}: missing {field}")
        for field in ["capture_harness", "artifact_validator", "pipeline_summary", "manifest"]:
            value = row.get(field)
            if value and not (ROOT / value).exists():
                failures.append(f"{framework_id}: missing referenced path {value}")
        if framework_id in {"mcp", "a2a", "guardrails-ai", "llama-guard", "nemo-guardrails"} and not row.get("manifest"):
            failures.append(f"{framework_id}: reusable command tooling requires manifest")
        if row.get("observed_evidence_state") not in {"not_captured", "pending_artifact_inspection", "captured_unverified", "replay_confirmed_same_environment", "replay_confirmed_independent_environment_fresh_runner"}:
            failures.append(f"{framework_id}: invalid observed_evidence_state")

    boundary = payload.get("authority_boundary", {})
    for key in [
        "tooling_coverage_is_execution",
        "artifact_validation_is_compatibility",
        "pipeline_summary_creates_standing",
        "tooling_configuration_creates_execution_authority",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"authority_boundary.{key} must be false")

    print("EXTERNAL FRAMEWORK EVIDENCE TOOLING COVERAGE:", "FAIL" if failures else "PASS")
    print(f"coverage: {len(ids & EXPECTED)}/{len(EXPECTED)} priority frameworks")
    print("observed evidence remains separate from tooling readiness")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
