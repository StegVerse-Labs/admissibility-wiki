#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "external-frameworks" / "legacy-priority-page-remediation.v1.json"
UNION = ROOT / "static" / "external-frameworks" / "canonical-union-inventory.v1.json"
BINDINGS = ROOT / "static" / "external-frameworks" / "sidebar-framework-artifact-bindings.v1.json"


def heading_present(text: str, alternatives: list[str]) -> bool:
    return any(f"## {heading}" in text for heading in alternatives)


def main() -> int:
    failures: list[str] = []
    for required in (STATUS, UNION, BINDINGS):
        if not required.exists():
            failures.append(f"missing artifact: {required.relative_to(ROOT)}")
    if failures:
        print("EXTERNAL FRAMEWORK LEGACY PRIORITY PAGE REMEDIATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    union = json.loads(UNION.read_text(encoding="utf-8"))
    bindings = json.loads(BINDINGS.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    groups = data.get("semantic_requirements", {})
    counts = data.get("counts", {})

    union_ids = {entry.get("record_id") for entry in union.get("entries", [])}
    binding_ids = {entry.get("framework_id") for entry in bindings.get("entries", [])}
    seen: set[str] = set()
    complete = 0

    if data.get("schema") != "external_framework_legacy_priority_page_remediation.v1":
        failures.append("unexpected schema")
    if len(entries) != counts.get("cohort_pages"):
        failures.append("cohort page count is stale")

    for entry in entries:
        framework_id = entry.get("framework_id")
        page_path = entry.get("page_path")
        if not isinstance(framework_id, str) or framework_id in seen:
            failures.append(f"invalid or duplicate framework id: {framework_id}")
            continue
        seen.add(framework_id)
        if framework_id not in union_ids:
            failures.append(f"framework missing from canonical union: {framework_id}")
        if framework_id not in binding_ids:
            failures.append(f"framework missing from artifact bindings: {framework_id}")
        if entry.get("completeness") != "COMPLETE_WITH_EXTERNAL_GATES":
            failures.append(f"framework not complete with external gates: {framework_id}")
            continue
        complete += 1
        if not isinstance(page_path, str):
            failures.append(f"missing page path: {framework_id}")
            continue
        page = ROOT / page_path
        if not page.exists():
            failures.append(f"missing page: {page_path}")
            continue
        text = page.read_text(encoding="utf-8")
        for group_name, alternatives in groups.items():
            if not heading_present(text, alternatives):
                failures.append(f"missing semantic group {group_name}: {framework_id}")
        if "execution authority" not in text.lower():
            failures.append(f"missing execution-authority boundary: {framework_id}")
        if "Publication does not create standing" not in text and "does not establish" not in text:
            failures.append(f"missing publication or standing boundary: {framework_id}")

    if complete != counts.get("complete_with_external_gates"):
        failures.append("complete_with_external_gates count is stale")
    if counts.get("partial") != 0:
        failures.append("partial count must be zero")

    print("EXTERNAL FRAMEWORK LEGACY PRIORITY PAGE REMEDIATION:", "FAIL" if failures else "PASS")
    print(f"cohort_pages={len(entries)}")
    print(f"complete_with_external_gates={complete}")
    print(f"partial={counts.get('partial')}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
