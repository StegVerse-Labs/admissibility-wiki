#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "canonical-decision-enum-registry.md"
REGISTRY = ROOT / "static" / "ontology" / "canonical-decision-enum-registry.v0.1.json"
STATUS = ROOT / "static" / "status" / "canonical-decision-enum-registry-status.json"
DECISION_RECORD = ROOT / "docs" / "governance" / "decision-record.md"
SIDEBAR = ROOT / "sidebars.js"

RUNTIME_VALUES = ["ALLOW", "DENY", "DEFER"]
WIKI_VALUES = ["ALLOW", "ALLOW_AS_OVERLAP", "DENY", "DEFER", "ESCALATE", "REFUSE", "SUPERSEDE"]
POSTURE_VALUES = ["FAIL-CLOSED", "FAIL_CLOSED", "CONDITIONAL"]
SURFACE_LABELS = [
    "runtime_transition_decision",
    "wiki_governance_decision",
    "interop_failure_posture",
    "downstream_status_label",
]

REQUIRED_PAGE_SNIPPETS = [
    "Canonical Decision Enum Registry",
    "Runtime Transition Surface",
    "Wiki Governance Surface",
    "Interop Failure and Status Terms",
    "Required Use Rule",
    "static/ontology/canonical-decision-enum-registry.v0.1.json",
]

REQUIRED_DECISION_RECORD_SNIPPETS = [
    "docs/governance/canonical-decision-enum-registry.md",
    "static/ontology/canonical-decision-enum-registry.v0.1.json",
    "enum_surface",
    "wiki_governance_decision",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path, label: str) -> dict:
    raw = require_file(path)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - {label} JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - {label} JSON root must be an object")
    return data


def require_snippets(label: str, text: str, snippets: list[str]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        raise SystemExit(
            f"CANONICAL DECISION ENUM REGISTRY: FAIL - {label} missing: {', '.join(missing)}"
        )


def require_registry() -> None:
    data = read_json(REGISTRY, "registry")
    if data.get("schema") != "canonical_decision_enum_registry.v0.1":
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - registry schema mismatch")
    if data.get("status") != "active":
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - registry status must be active")

    boundary = data.get("boundary")
    if not isinstance(boundary, dict):
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - boundary must be an object")
    for key in [
        "registry_is_runtime_authority",
        "registry_is_spe_resolution",
        "public_page_visibility_is_authority",
        "unmapped_surface_copy_is_valid",
    ]:
        if boundary.get(key) is not False:
            raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - boundary {key} must be false")

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict):
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - surfaces must be an object")
    expected = {
        "runtime_transition_decision": RUNTIME_VALUES,
        "wiki_governance_decision": WIKI_VALUES,
        "interop_failure_posture": POSTURE_VALUES,
    }
    for surface, values in expected.items():
        surface_data = surfaces.get(surface)
        if not isinstance(surface_data, dict):
            raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - missing surface {surface}")
        if surface_data.get("values") != values:
            raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - {surface} values mismatch")

    if data.get("required_surface_labels") != SURFACE_LABELS:
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - required surface labels mismatch")

    value_map = data.get("value_map")
    if not isinstance(value_map, dict):
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - value_map must be an object")
    for value in sorted(set(RUNTIME_VALUES + WIKI_VALUES + POSTURE_VALUES)):
        item = value_map.get(value)
        if not isinstance(item, dict):
            raise SystemExit(f"CANONICAL DECISION ENUM REGISTRY: FAIL - value_map missing {value}")
        if item.get("mapping_required_across_surfaces") is not True:
            raise SystemExit(
                f"CANONICAL DECISION ENUM REGISTRY: FAIL - {value} must require mapping across surfaces"
            )


def require_status() -> None:
    data = read_json(STATUS, "status")
    expected = {
        "schema": "canonical_decision_enum_registry_status.v0.1",
        "status": "installed",
        "version": "1.5.14-canonical-decision-enum-registry",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"CANONICAL DECISION ENUM REGISTRY: FAIL - status {key} expected {value!r}, got {data.get(key)!r}"
            )
    if data.get("surface_labels") != SURFACE_LABELS:
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - status surface labels mismatch")
    if data.get("runtime_transition_decision_values") != RUNTIME_VALUES:
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - status runtime values mismatch")
    if data.get("wiki_governance_decision_values") != WIKI_VALUES:
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - status wiki values mismatch")
    if data.get("interop_failure_posture_values") != POSTURE_VALUES:
        raise SystemExit("CANONICAL DECISION ENUM REGISTRY: FAIL - status posture values mismatch")


def main() -> int:
    page = require_file(PAGE)
    decision_record = require_file(DECISION_RECORD)
    sidebar = require_file(SIDEBAR)
    require_snippets("registry page", page, REQUIRED_PAGE_SNIPPETS)
    require_snippets("decision record", decision_record, REQUIRED_DECISION_RECORD_SNIPPETS)
    require_snippets("sidebar", sidebar, ["governance/canonical-decision-enum-registry"])
    require_registry()
    require_status()
    print("CANONICAL DECISION ENUM REGISTRY: PASS - page, machine registry, status, decision record, and sidebar are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
