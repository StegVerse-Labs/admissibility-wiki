#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
CEDAR_APPLIED_RECEIPT = ROOT / "reports" / "external-frameworks" / "cedar-build" / "cedar-binary-registry-promotion-receipt.applied-hash-only.json"
EXPECTED_IDS = ["cedar-policy", "mcp", "a2a", "guardrails-ai", "llama-guard", "neMo-guardrails"]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
COMMON_BOUNDARIES = [
    "implementation_selection_is_certification",
    "implementation_selection_is_compatibility",
    "implementation_selection_creates_standing",
    "implementation_selection_creates_execution_authority",
    "selection_gate_may_authorize_external_consequence",
]


def nonempty(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def validate_cedar_hash_promotion(compiled_hash: object, failures: list[str]) -> None:
    if compiled_hash is None:
        return
    if not isinstance(compiled_hash, str) or not HEX64.fullmatch(compiled_hash):
        failures.append("cedar-policy: compiled binary hash must be lowercase sha256")
        return
    if not CEDAR_APPLIED_RECEIPT.exists():
        failures.append("cedar-policy: applied hash-only promotion receipt missing")
        return
    try:
        receipt = load_json(CEDAR_APPLIED_RECEIPT)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        failures.append(f"cedar-policy: applied promotion receipt invalid: {exc}")
        return
    source = receipt.get("source_promotion_candidate", {})
    target = receipt.get("registry_target", {})
    expected = {
        "receipt_type": "cedar_binary_registry_promotion_receipt",
        "framework_id": "cedar-policy",
        "decision": "ALLOW_REGISTRY_PROMOTION_ONLY",
        "promotion_state": "APPLIED_HASH_ONLY",
        "registry_mutation_applied": True,
        "runtime_execution_authorized": False,
        "external_consequence_allowed": False,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            failures.append(f"cedar-policy: applied promotion receipt expected {key}={value!r}")
    if source.get("candidate_state") != "READY_FOR_REGISTRY_PROMOTION_REVIEW":
        failures.append("cedar-policy: applied promotion receipt requires ready candidate")
    if source.get("binary_sha256") != compiled_hash:
        failures.append("cedar-policy: registry hash differs from promoted binary hash")
    if target.get("field") != "frameworks[cedar-policy].selection.compiled_binary_sha256":
        failures.append("cedar-policy: applied promotion receipt targets wrong registry field")
    if target.get("proposed_value") != compiled_hash:
        failures.append("cedar-policy: applied promotion target differs from registry hash")


def main() -> int:
    failures: list[str] = []
    if not REGISTRY.exists():
        print("IMPLEMENTATION SELECTION GATES: FAIL")
        print(f"- missing {REGISTRY.relative_to(ROOT)}")
        return 1
    try:
        payload = load_json(REGISTRY)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
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

    selected_count = 0
    for item in frameworks:
        if not isinstance(item, dict):
            failures.append("framework entry must be an object")
            continue
        framework_id = item.get("framework_id", "unknown")
        state = item.get("selection_state")
        required = item.get("required_fields")
        specific = item.get("framework_specific_requirements")
        if not isinstance(required, list) or len(required) < 8 or len(set(required)) != len(required):
            failures.append(f"{framework_id}: required_fields must contain at least 8 unique fields")
            required = []
        if not isinstance(specific, list) or len(specific) < 3:
            failures.append(f"{framework_id}: insufficient framework-specific requirements")
            specific = []
        if item.get("execution_authorized") is not False:
            failures.append(f"{framework_id}: execution_authorized must remain false")

        if state == "selection_required":
            if item.get("selection"):
                failures.append(f"{framework_id}: selection_required must not contain selection payload")
        elif state == "implementation_selected_hash_bound":
            selected_count += 1
            selection = item.get("selection")
            if not isinstance(selection, dict):
                failures.append(f"{framework_id}: selected state requires selection object")
                continue
            missing = [field for field in required if not nonempty(selection.get(field))]
            if missing:
                failures.append(f"{framework_id}: missing selected fields: {missing}")
            context = selection.get("framework_specific_context")
            if not isinstance(context, dict) or any(not nonempty(context.get(field)) for field in specific):
                failures.append(f"{framework_id}: framework-specific context incomplete")
            evidence_path = selection.get("selection_evidence_path")
            if not isinstance(evidence_path, str) or not (ROOT / evidence_path).exists():
                failures.append(f"{framework_id}: selection evidence path missing")
            compiled_hash = selection.get("compiled_binary_sha256")
            if framework_id == "cedar-policy":
                validate_cedar_hash_promotion(compiled_hash, failures)
            elif compiled_hash is not None:
                failures.append(f"{framework_id}: compiled binary hash is not authorized by a promotion receipt")
        else:
            failures.append(f"{framework_id}: unsupported selection_state {state}")

    if selected_count != 1:
        failures.append(f"expected exactly one promoted hash-bound selection, found {selected_count}")

    gate = payload.get("gate", {})
    for key in ["all_required_fields_present", "all_artifacts_hash_bound", "all_versions_pinned", "execution_jobs_may_be_added"]:
        if gate.get(key) is not False:
            failures.append(f"gate.{key} must remain false")
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
