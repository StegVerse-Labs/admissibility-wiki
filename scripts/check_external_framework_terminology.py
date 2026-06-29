#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
RULE = ROOT / "docs" / "external-frameworks" / "terminology-reconciliation-rule.md"
GLOSSARY = ROOT / "docs" / "glossary" / "terminology-reconciliation.md"
GLOSSARY_INDEX = ROOT / "docs" / "glossary" / "index.md"

REQUIRED_CLASSES = ["Synonymous", "Adjacent", "New", "Unresolved"]
REQUIRED_PAGE_MARKERS = [
    "## Framework-Term Definitions",
    "Reconciliation Class",
    "Admissibility Relationship",
]
REQUIRED_BOUNDARY_MARKERS = [
    "execution authority",
    "admissibility",
    "standing",
    "certification",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [REGISTRY, RULE, GLOSSARY, GLOSSARY_INDEX]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK TERMINOLOGY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = load_json(REGISTRY)
    rule_text = RULE.read_text(encoding="utf-8")
    glossary_text = GLOSSARY.read_text(encoding="utf-8")
    glossary_index_text = GLOSSARY_INDEX.read_text(encoding="utf-8")

    for required_class in REQUIRED_CLASSES:
        if required_class not in rule_text:
            failures.append(f"rule missing class: {required_class}")
        if required_class not in glossary_text:
            failures.append(f"glossary entry missing class: {required_class}")
        if required_class not in glossary_index_text:
            failures.append(f"glossary index missing class: {required_class}")

    for marker in REQUIRED_BOUNDARY_MARKERS:
        if marker not in rule_text:
            failures.append(f"rule missing boundary marker: {marker}")
        if marker not in glossary_text:
            failures.append(f"glossary entry missing boundary marker: {marker}")

    entries = registry.get("entries", [])
    if not entries:
        failures.append("registry has no entries")

    for entry in entries:
        framework_id = entry.get("framework_id", "UNKNOWN")
        path_value = entry.get("path")
        if not isinstance(path_value, str):
            failures.append(f"{framework_id} missing markdown path")
            continue

        page_path = ROOT / path_value
        if not page_path.exists():
            failures.append(f"{framework_id} markdown path missing: {path_value}")
            continue

        text = page_path.read_text(encoding="utf-8")
        for marker in REQUIRED_PAGE_MARKERS:
            if marker not in text:
                failures.append(f"{framework_id} missing terminology marker: {marker}")

        if not any(f"| {classification.lower()} |" in text.lower() for classification in REQUIRED_CLASSES):
            failures.append(f"{framework_id} has no reconciliation class row")

        if "execution authority" not in text:
            failures.append(f"{framework_id} missing execution-authority boundary text")

    print("EXTERNAL FRAMEWORK TERMINOLOGY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
