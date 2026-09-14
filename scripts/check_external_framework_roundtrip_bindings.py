#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_external_framework_roundtrip_bindings.py"
REGISTRY_PATH = ROOT / "docs" / "external-frameworks" / "index.json"
OVERLAY_PATH = ROOT / "data" / "external-framework-roundtrip-endpoints.json"


def load_builder():
    spec = importlib.util.spec_from_file_location("roundtrip_bindings", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    if not REGISTRY_PATH.exists():
        failures.append("missing canonical external-framework registry")
    if not OVERLAY_PATH.exists():
        failures.append("missing explicit endpoint overlay")
    if failures:
        for failure in failures:
            print(f"EXTERNAL FRAMEWORK ROUNDTRIP BINDINGS: FAIL - {failure}")
        return 1

    module = load_builder()
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    overlay = json.loads(OVERLAY_PATH.read_text(encoding="utf-8"))

    try:
        result = module.build_bindings(registry, overlay)
    except Exception as exc:
        print(f"EXTERNAL FRAMEWORK ROUNDTRIP BINDINGS: FAIL - live projection error: {exc}")
        return 1

    entries = registry.get("entries", [])
    bindings = result.get("bindings", [])
    registry_ids = [item.get("framework_id") for item in entries if isinstance(item, dict)]
    binding_ids = [item.get("framework_id") for item in bindings if isinstance(item, dict)]

    if binding_ids != registry_ids:
        failures.append("binding identities/order do not exactly match canonical registry")
    if result.get("framework_count") != len(registry_ids):
        failures.append("framework_count mismatch")
    if result.get("framework_count") != result.get("explicit_endpoint_bound_count", 0) + result.get("unbound_count", 0):
        failures.append("bound/unbound counts do not reconcile")
    if result.get("authority_effect") != "NONE_COORDINATION_ONLY":
        failures.append("registry authority effect must remain NONE_COORDINATION_ONLY")
    if result.get("transition_effect") != "NONE_PLAN_ONLY":
        failures.append("registry transition effect must remain NONE_PLAN_ONLY")

    for binding in bindings:
        framework_id = binding.get("framework_id")
        endpoint = binding.get("runtime_endpoint_ref")
        state = binding.get("binding_state")
        if endpoint is None and state != "UNBOUND_NO_RUNTIME_ENDPOINT_REF":
            failures.append(f"unbound state mismatch: {framework_id}")
        if endpoint is not None and state != "EXPLICIT_ENDPOINT_BOUND":
            failures.append(f"bound state mismatch: {framework_id}")
        if binding.get("authority_effect") != "NONE_COORDINATION_ONLY":
            failures.append(f"binding authority effect mismatch: {framework_id}")
        if binding.get("transition_effect") != "NONE_PLAN_ONLY":
            failures.append(f"binding transition effect mismatch: {framework_id}")

    sample_registry = {
        "schema_version": "0.4",
        "entries": [
            {"framework_id": "alpha", "name": "Alpha", "status": "SOURCED-CROSSWALK-PROVISIONAL", "manifest_path": "docs/external-frameworks/alpha.json", "source": "https://alpha.test"},
            {"framework_id": "beta", "name": "Beta", "status": "OFFICIAL-SOURCE-REQUIRED", "manifest_path": "docs/external-frameworks/beta.json", "source": "official source required"},
        ],
    }
    sample = module.build_bindings(sample_registry, {"bindings": {"alpha": {"runtime_endpoint_ref": "https://alpha.test/evaluate"}}})
    rows = {row["framework_id"]: row for row in sample["bindings"]}
    if rows["alpha"]["binding_state"] != "EXPLICIT_ENDPOINT_BOUND":
        failures.append("synthetic explicit binding was not retained")
    if rows["beta"]["binding_state"] != "UNBOUND_NO_RUNTIME_ENDPOINT_REF":
        failures.append("synthetic missing binding was not fail-closed unbound")

    try:
        module.build_bindings(sample_registry, {"bindings": {"unknown": "https://unknown.test"}})
        failures.append("unknown overlay framework id was accepted")
    except ValueError:
        pass

    duplicate = dict(sample_registry)
    duplicate["entries"] = list(sample_registry["entries"]) + [dict(sample_registry["entries"][0])]
    try:
        module.build_bindings(duplicate, None)
        failures.append("duplicate registry framework id was accepted")
    except ValueError:
        pass

    if failures:
        print("EXTERNAL FRAMEWORK ROUNDTRIP BINDINGS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("EXTERNAL FRAMEWORK ROUNDTRIP BINDINGS: PASS")
    print(f"frameworks={result['framework_count']}")
    print(f"explicit_endpoint_bound={result['explicit_endpoint_bound_count']}")
    print(f"unbound={result['unbound_count']}")
    print("authority_effect=NONE_COORDINATION_ONLY")
    print("transition_effect=NONE_PLAN_ONLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
