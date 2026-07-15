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
COVERAGE = ROOT / "static" / "external-frameworks" / "terminology-reconciliation-coverage.v1.json"

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
ALLOWED_CLASSES = {"synonymous", "adjacent", "new", "unresolved"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def page_has_inline_reconciliation(text: str) -> bool:
    return all(marker in text for marker in REQUIRED_PAGE_MARKERS) and any(
        f"| {classification.lower()} |" in text.lower()
        for classification in REQUIRED_CLASSES
    )


def main() -> int:
    failures: list[str] = []

    for path in [REGISTRY, RULE, GLOSSARY, GLOSSARY_INDEX, COVERAGE]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK TERMINOLOGY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = load_json(REGISTRY)
    coverage = load_json(COVERAGE)
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

    coverage_entries = coverage.get("entries", [])
    coverage_by_id: dict[str, dict[str, Any]] = {}
    for item in coverage_entries:
        framework_id = item.get("framework_id")
        if not isinstance(framework_id, str) or framework_id in coverage_by_id:
            failures.append(f"invalid or duplicate coverage framework id: {framework_id}")
            continue
        coverage_by_id[framework_id] = item
        if item.get("reconciliation_class") not in ALLOWED_CLASSES:
            failures.append(f"invalid reconciliation class: {framework_id}")
        if item.get("authority_effect") != "NONE":
            failures.append(f"terminology coverage authority effect must be NONE: {framework_id}")
        if not isinstance(item.get("native_terms"), list) or not item.get("native_terms"):
            failures.append(f"terminology coverage missing native terms: {framework_id}")
        relationship = item.get("admissibility_relationship")
        if not isinstance(relationship, str) or not relationship.strip():
            failures.append(f"terminology coverage missing admissibility relationship: {framework_id}")

    entries = registry.get("entries", [])
    if not entries:
        failures.append("registry has no entries")

    inline_count = 0
    governed_count = 0
    registry_ids: set[str] = set()
    for entry in entries:
        framework_id = entry.get("framework_id", "UNKNOWN")
        if isinstance(framework_id, str):
            registry_ids.add(framework_id)
        path_value = entry.get("path")
        if not isinstance(path_value, str):
            failures.append(f"{framework_id} missing markdown path")
            continue

        page_path = ROOT / path_value
        if not page_path.exists():
            failures.append(f"{framework_id} markdown path missing: {path_value}")
            continue

        text = page_path.read_text(encoding="utf-8")
        if "execution authority" not in text:
            failures.append(f"{framework_id} missing execution-authority boundary text")

        if page_has_inline_reconciliation(text):
            inline_count += 1
            continue

        governed = coverage_by_id.get(str(framework_id))
        if governed is None:
            failures.append(f"{framework_id} lacks inline terminology reconciliation and governed coverage")
            continue
        if governed.get("page_path") != path_value:
            failures.append(f"terminology coverage page mismatch: {framework_id}")
        governed_count += 1

    unknown_coverage = sorted(set(coverage_by_id) - registry_ids)
    for framework_id in unknown_coverage:
        failures.append(f"terminology coverage framework not found in registry: {framework_id}")

    counts = coverage.get("counts", {})
    if counts.get("records") != len(coverage_entries):
        failures.append("terminology coverage records count is stale")
    class_counts = {
        key: sum(1 for item in coverage_entries if item.get("reconciliation_class") == key)
        for key in ALLOWED_CLASSES
    }
    for key, count in class_counts.items():
        if counts.get(key) != count:
            failures.append(f"terminology coverage {key} count is stale")
    if class_counts["synonymous"] != 0:
        failures.append("terminology coverage may not establish synonymy without a decision record")
    if "does not create synonymy" not in coverage.get("boundary", ""):
        failures.append("terminology coverage boundary must prohibit synonymy creation")

    print("EXTERNAL FRAMEWORK TERMINOLOGY:", "FAIL" if failures else "PASS")
    print(f"registry_frameworks={len(registry_ids)}")
    print(f"inline_reconciliation={inline_count}")
    print(f"governed_coverage={governed_count}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
