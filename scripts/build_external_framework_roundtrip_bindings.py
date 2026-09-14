#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
DEFAULT_OVERLAY = ROOT / "data" / "external-framework-roundtrip-endpoints.json"
DEFAULT_OUTPUT = ROOT / "reports" / "external-frameworks" / "roundtrip-bindings.json"
PARENT_GOAL = "MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001"
PARENT_COSV = "50000000100000"
REUSABLE_TASK = "RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001"
REQUIRED_ENDPOINT_EVIDENCE_FIELDS = (
    "endpoint_evidence_ref",
    "endpoint_observed_at",
    "endpoint_evidence_class",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_overlay(value: Any) -> dict[str, dict[str, Any]]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError("endpoint overlay must be an object")
    raw = value.get("bindings", value)
    if not isinstance(raw, dict):
        raise ValueError("endpoint overlay bindings must be an object keyed by framework_id")
    result: dict[str, dict[str, Any]] = {}
    for framework_id, binding in raw.items():
        if not isinstance(framework_id, str) or not framework_id:
            raise ValueError("endpoint overlay framework ids must be non-empty strings")
        if binding is None:
            result[framework_id] = {}
        elif isinstance(binding, str):
            raise ValueError(
                f"bare endpoint string is not evidence-qualified: {framework_id}; "
                "use an object with runtime_endpoint_ref and endpoint evidence fields"
            )
        elif isinstance(binding, dict):
            result[framework_id] = dict(binding)
        else:
            raise ValueError(f"invalid binding for {framework_id}")
    return result


def _clean_optional_string(value: Any, *, field: str, framework_id: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string or null: {framework_id}")
    return value.strip()


def _validate_endpoint_evidence(supplied: dict[str, Any], framework_id: str, endpoint: str | None) -> dict[str, str | None]:
    evidence = {
        field: _clean_optional_string(supplied.get(field), field=field, framework_id=framework_id)
        for field in REQUIRED_ENDPOINT_EVIDENCE_FIELDS
    }
    present = [field for field, value in evidence.items() if value]
    if endpoint:
        missing = [field for field, value in evidence.items() if not value]
        if missing:
            raise ValueError(
                f"runtime endpoint is not evidence-qualified for {framework_id}; missing=" + ",".join(missing)
            )
    elif present:
        raise ValueError(
            f"endpoint evidence supplied without runtime_endpoint_ref for {framework_id}; fields=" + ",".join(present)
        )
    return evidence


def build_bindings(registry: dict[str, Any], overlay: dict[str, Any] | None = None) -> dict[str, Any]:
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise ValueError("registry.entries must be a list")

    by_id: dict[str, dict[str, Any]] = {}
    ordered_ids: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("registry entry must be an object")
        framework_id = entry.get("framework_id")
        if not isinstance(framework_id, str) or not framework_id:
            raise ValueError("registry entry missing framework_id")
        if framework_id in by_id:
            raise ValueError(f"duplicate framework_id: {framework_id}")
        by_id[framework_id] = entry
        ordered_ids.append(framework_id)

    endpoint_overlay = normalize_overlay(overlay)
    unknown = sorted(set(endpoint_overlay) - set(by_id))
    if unknown:
        raise ValueError("endpoint overlay contains unknown framework ids: " + ",".join(unknown))

    bindings: list[dict[str, Any]] = []
    bound_count = 0
    for framework_id in ordered_ids:
        entry = by_id[framework_id]
        supplied = endpoint_overlay.get(framework_id, {})
        endpoint = _clean_optional_string(
            supplied.get("runtime_endpoint_ref"),
            field="runtime_endpoint_ref",
            framework_id=framework_id,
        )
        evidence = _validate_endpoint_evidence(supplied, framework_id, endpoint)
        if endpoint:
            bound_count += 1
        bindings.append({
            "framework_id": framework_id,
            "framework_name": entry.get("name"),
            "registry_status": entry.get("status"),
            "manifest_path": entry.get("manifest_path"),
            "source_reference": entry.get("source"),
            "runtime_endpoint_ref": endpoint,
            "endpoint_evidence_ref": evidence["endpoint_evidence_ref"],
            "endpoint_observed_at": evidence["endpoint_observed_at"],
            "endpoint_evidence_class": evidence["endpoint_evidence_class"],
            "binding_state": "EVIDENCE_QUALIFIED_ENDPOINT_BOUND" if endpoint else "UNBOUND_NO_RUNTIME_ENDPOINT_REF",
            "counterpart_provenance": supplied.get("counterpart_provenance", "UNOBSERVED_CANDIDATE"),
            "operation_class": supplied.get("operation_class", "RUNTIME_ROUNDTRIP"),
            "authority_effect": "NONE_COORDINATION_ONLY",
            "transition_effect": "NONE_PLAN_ONLY",
        })

    return {
        "schema": "stegverse.external-framework-roundtrip-binding-registry/v1",
        "parent_goal_task_id": PARENT_GOAL,
        "parent_cosv": PARENT_COSV,
        "reusable_task_id": REUSABLE_TASK,
        "source_registry_schema_version": registry.get("schema_version"),
        "framework_count": len(bindings),
        "explicit_endpoint_bound_count": bound_count,
        "unbound_count": len(bindings) - bound_count,
        "authority_effect": "NONE_COORDINATION_ONLY",
        "transition_effect": "NONE_PLAN_ONLY",
        "binding_semantics": {
            "one_row_per_registry_framework": True,
            "missing_endpoint_is_explicit_unbound_state": True,
            "bound_endpoint_requires_independent_evidence_metadata": True,
            "documentation_or_source_url_may_not_be_inferred_as_endpoint": True,
            "endpoint_binding_proves_authenticity": False,
            "endpoint_binding_proves_availability": False,
            "endpoint_binding_grants_execution_authority": False,
            "classification_owner": "RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001",
        },
        "bindings": bindings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--endpoint-overlay", type=Path, default=DEFAULT_OVERLAY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    registry = load_json(args.registry)
    overlay = load_json(args.endpoint_overlay) if args.endpoint_overlay.exists() else None
    result = build_bindings(registry, overlay)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "EXTERNAL FRAMEWORK ROUNDTRIP BINDINGS: "
        f"{result['framework_count']} frameworks; "
        f"{result['explicit_endpoint_bound_count']} evidence-qualified endpoint-bound; "
        f"{result['unbound_count']} unbound; authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
