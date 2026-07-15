#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/external-frameworks/all-navigated-framework-page-completeness.v1.json"
ASSOCIATIONS = ROOT / "static/external-frameworks/sidebar-page-associations.v1.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    if not STATUS.exists() or not ASSOCIATIONS.exists():
        print("ALL NAVIGATED EXTERNAL FRAMEWORK PAGE COMPLETENESS: FAIL")
        return 1

    status = read_json(STATUS)
    associations = read_json(ASSOCIATIONS)
    cohort_ids: set[str] = set()
    cohort_total = 0

    for source in status.get("cohort_sources", []):
        path = ROOT / source.get("path", "")
        if not path.exists():
            failures.append(f"missing cohort source: {source.get('path')}")
            continue
        data = read_json(path)
        entries = data.get("entries", [])
        if len(entries) != source.get("page_count"):
            failures.append(f"cohort count mismatch: {source.get('path')}")
        cohort_total += len(entries)
        for entry in entries:
            framework_id = entry.get("framework_id")
            if not isinstance(framework_id, str) or framework_id in cohort_ids:
                failures.append(f"invalid or duplicate cohort framework id: {framework_id}")
                continue
            cohort_ids.add(framework_id)
            if entry.get("completeness") != "COMPLETE_WITH_EXTERNAL_GATES":
                failures.append(f"framework not complete: {framework_id}")

    sidebar_ids = {
        entry.get("framework_id")
        for entry in associations.get("entries", [])
        if entry.get("page_type") == "framework"
    }
    counts = status.get("counts", {})
    if cohort_ids != sidebar_ids:
        failures.append("cohort union does not exactly match navigated framework IDs")
    if cohort_total != counts.get("navigated_framework_pages"):
        failures.append("navigated framework count is stale")
    if counts.get("complete_with_external_gates") != cohort_total:
        failures.append("complete count is stale")
    if counts.get("partial") != 0:
        failures.append("partial count must be zero")

    print("ALL NAVIGATED EXTERNAL FRAMEWORK PAGE COMPLETENESS:", "FAIL" if failures else "PASS")
    print(f"navigated_framework_pages={len(sidebar_ids)}")
    print(f"complete_with_external_gates={cohort_total}")
    print(f"partial={counts.get('partial')}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
