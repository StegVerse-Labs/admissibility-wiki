#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDICATES = ROOT / "static/data/standards/gsdp/conformance/gsdp-conformance-predicates.v0.1.json"
INVENTORY = ROOT / "static/data/standards/gsdp/inventory/stegverse-ecosystem.inventory.pending.v0.1.json"
STATUS = ROOT / "static/status/gsdp-semantic-conformance-status.json"
FIXTURES = ROOT / "static/data/standards/gsdp/fixtures"
EXPECTED_CLASSES = [
    "GSDP-DISCOVERABLE",
    "GSDP-GOVERNED",
    "GSDP-EVIDENCED",
    "GSDP-RECONSTRUCTABLE",
    "GSDP-INTEROPERABLE",
    "GSDP-CERTIFIABLE",
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    required = [
        PREDICATES,
        INVENTORY,
        STATUS,
        FIXTURES / "stale-record.defer.v0.1.json",
        FIXTURES / "unresolved-reference.defer.v0.1.json",
        FIXTURES / "authority-contradiction.fail.v0.1.json",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        print("GSDP semantic conformance: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    predicates = load(PREDICATES)
    inventory = load(INVENTORY)
    status = load(STATUS)
    classes = predicates.get("classes", [])
    ids = [item.get("id") for item in classes]
    if ids != EXPECTED_CLASSES:
        errors.append("conformance classes must preserve canonical additive order")
    seen: set[str] = set()
    for item in classes:
        class_id = item.get("id")
        if not item.get("predicates"):
            errors.append(f"{class_id} lacks predicates")
        if any(req not in seen for req in item.get("requires", [])):
            errors.append(f"{class_id} requires a class not previously satisfied in additive order")
        seen.add(class_id)

    if inventory.get("conformance", {}).get("inventory_completeness") != "PARTIAL":
        errors.append("current inventory must remain PARTIAL")
    if not inventory.get("unresolved"):
        errors.append("current bounded evaluation expects unresolved coordinates to remain explicit")

    results = status.get("evaluation_result", {})
    if list(results) != EXPECTED_CLASSES:
        errors.append("status must evaluate every class in canonical order")
    if any(results.get(name) != "DEFER" for name in EXPECTED_CLASSES):
        errors.append("partial inventory and unobserved public discovery require every class to remain DEFER")
    if status.get("claimed_conformance_classes"):
        errors.append("no conformance class may be claimed")
    if status.get("certification_authority") is not False or status.get("execution_authority") is not False:
        errors.append("semantic evaluation grants no certification or execution authority")

    expected_fixture_results = {
        "stale-record.defer.v0.1.json": "DEFER",
        "unresolved-reference.defer.v0.1.json": "DEFER",
        "authority-contradiction.fail.v0.1.json": "FAIL",
    }
    for filename, expected in expected_fixture_results.items():
        fixture = load(FIXTURES / filename)
        if fixture.get("expected_result") != expected:
            errors.append(f"fixture {filename} must expect {expected}")
        if fixture.get("authority_effect") != "NONE":
            errors.append(f"fixture {filename} must preserve authority_effect=NONE")

    if errors:
        print("GSDP semantic conformance: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GSDP semantic conformance: PASS")
    for name in EXPECTED_CLASSES:
        print(f"{name}: DEFER")
    print("claimed conformance classes: none")
    print("authority effect: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
