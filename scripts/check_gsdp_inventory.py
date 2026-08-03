#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "static/data/standards/gsdp/inventory/stegverse-ecosystem.inventory.pending.v0.1.json"
STATUS = ROOT / "static/status/gsdp-inventory-status.json"
SOURCE = ROOT / "docs/governance/governed-ecosystem-index.md"
SOURCE_STATUS = ROOT / "static/status/governed-ecosystem-index-status.json"
ALLOWED = {"verified", "pending", "deprecated", "unresolved"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for path in (INVENTORY, STATUS, SOURCE, SOURCE_STATUS):
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1

    inventory = load(INVENTORY)
    status = load(STATUS)
    source_status = load(SOURCE_STATUS)

    if source_status.get("status") != "GOVERNED_ECOSYSTEM_INDEX_PRESENT":
        errors.append("source ecosystem index status is not present")
    if inventory.get("state") != "PROVENANCE_BOUND_PARTIAL_INVENTORY":
        errors.append("inventory must remain provenance-bound and partial")

    organizations = inventory.get("organizations", [])
    components = inventory.get("components", [])
    unresolved = inventory.get("unresolved", [])
    deprecated = inventory.get("deprecated", [])
    if not organizations or not components:
        errors.append("inventory requires organizations and components")

    org_ids = [item.get("id") for item in organizations]
    component_ids = [item.get("id") for item in components]
    all_ids = component_ids + [item.get("id") for item in unresolved] + [item.get("id") for item in deprecated]
    if len(org_ids) != len(set(org_ids)):
        errors.append("organization ids must be unique")
    if len(all_ids) != len(set(all_ids)):
        errors.append("component, unresolved, and deprecated ids must be unique")

    known_orgs = set(org_ids)
    for collection_name, collection in (("organization", organizations), ("component", components), ("unresolved", unresolved), ("deprecated", deprecated)):
        for item in collection:
            if item.get("record_status") not in ALLOWED:
                errors.append(f"{collection_name} {item.get('id')} has invalid record_status")
            if not item.get("provenance_refs"):
                errors.append(f"{collection_name} {item.get('id')} lacks provenance")
            if not item.get("last_verified"):
                errors.append(f"{collection_name} {item.get('id')} lacks last_verified")

    for component in components:
        if component.get("organization_ref") not in known_orgs:
            errors.append(f"component {component.get('id')} has unresolved organization_ref")
        if component.get("authority_inferred") is not False:
            errors.append(f"component {component.get('id')} must preserve authority_inferred=false")
        if component.get("record_status") != "verified":
            errors.append(f"listed source-bound component {component.get('id')} must use record_status=verified")

    conformance = inventory.get("conformance", {})
    if conformance.get("claimed_classes"):
        errors.append("partial inventory must claim zero conformance classes")
    if conformance.get("semantic_evaluation") != "NOT_RUN":
        errors.append("semantic conformance evaluation must remain NOT_RUN")
    if conformance.get("inventory_completeness") != "PARTIAL":
        errors.append("inventory completeness must remain PARTIAL")

    expected_status = {
        "standard_id": "GSDP",
        "state": "PARTIAL_PROVENANCE_BOUND_INVENTORY_INSTALLED",
        "inventory_validation": "BOUND_INTO_CANONICAL_AGGREGATE",
        "semantic_conformance": "NOT_RUN",
        "claimed_conformance_classes": [],
        "certification_authority": False,
        "execution_authority": False,
    }
    for key, expected in expected_status.items():
        if status.get(key) != expected:
            errors.append(f"status {key} must equal {expected!r}")

    if errors:
        print("GSDP ecosystem inventory validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GSDP ecosystem inventory validation: PASS")
    print(f"organizations: {len(organizations)}")
    print(f"source-bound components: {len(components)}")
    print(f"unresolved coordinates: {len(unresolved)}")
    print("inventory completeness: PARTIAL")
    print("claimed conformance classes: none")
    print("authority effect: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
