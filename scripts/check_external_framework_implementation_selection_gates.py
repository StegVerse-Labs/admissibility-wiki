#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"

EXPECTED_IDS = [
    "cedar-policy",
    "mcp",
    "a2a",
    "guardrails-ai",
    "llama-guard",
    "neMo-guardrails",
]

COMMON_BOUNDARIES = [
    "implementation_selection_is_certification",
    "implementation_selection_is_compatibility",
    "implementation_selection_creates_standing",
    "implementation_selection_creates_execution_authority",
    "selection_gate_may_authorize_external_consequence",
]


def main() -> int:
    failures: list[str] = []
    if not REGISTRY.exists():
        print("IMPLEMENTATION SELECTION GATES: FAIL")
        print(f"- missing {REGISTRY.relative_to(ROOT)}")
        return 1

    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("IMPLEMENTATION SELECTION GATES: FAIL")
        print(f"- invalid registry: {exc}")
        return 1

    if payload.get("artifact_type") != "external_framework_implementation_selection_gates":
        failures.append("artifact_type mismatch")
    if payload.get("schema_version") != "0.1":
        failures.append("schema_version mismatch")

    frameworks = payload.get("frameworks")
    if not isinstance(frameworks, list):
        failures.append("frameworks must be a list")
        frameworks = []

    ids = [item.get("framework_id") for item in frameworks if isinstance(item, dict)]
    if ids != EXPECTED_IDS:
        failures.append(f"framework order/identity mismatch: {ids}")

    for item in frameworks:
        if not isinstance(item, dict):
            failures.append("framework entry must be an object")
            continue
        framework_id = item.get("framework_id", "unknown")
        if item.get("selection_state") != "selection_required":
            failures.append(f"{framework_id}: selection_state must remain selection_required")
        required = item.get("required_fields")
        if not isinstance(required, list) or len(required) < 8 or len(set(required)) != len(required):
            failures.append(f"{framework_id}: required_fields must contain at least 8 unique fields")
        specific = item.get("framework_specific_requirements")
        if not isinstance(specific, list) or len(specific) < 3:
            failures.append(f"{framework_id}: insufficient framework-specific requirements")
        if item.get("execution_authorized") is not False:
            failures.append(f"{framework_id}: execution_authorized must be false")

    gate = payload.get("gate", {})
    for key in [
        "all_required_fields_present",
        "all_artifacts_hash_bound",
        "all_versions_pinned",
        "execution_jobs_may_be_added",
    ]:
        if gate.get(key) is not False:
            failures.append(f"gate.{key} must be false before implementation selection")

    boundary = payload.get("authority_boundary", {})
    for key in COMMON_BOUNDARIES:
        if boundary.get(key) is not False:
            failures.append(f"authority_boundary.{key} must be false")

    print("IMPLEMENTATION SELECTION GATES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
