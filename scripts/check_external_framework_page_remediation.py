#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/external-frameworks/policy-identity-provenance-page-remediation.v1.json"


def main() -> int:
    failures: list[str] = []
    if not STATUS.exists():
        print("EXTERNAL FRAMEWORK PAGE REMEDIATION: FAIL")
        print(f"- missing status artifact: {STATUS.relative_to(ROOT)}")
        return 1

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    required_sections = data.get("required_sections", [])
    counts = data.get("counts", {})

    if data.get("schema") != "external_framework_page_remediation.v1":
        failures.append("unexpected schema")
    if len(entries) != counts.get("cohort_pages"):
        failures.append("cohort page count is stale")

    complete = 0
    partial = 0
    seen: set[str] = set()
    for entry in entries:
        framework_id = entry.get("framework_id")
        page_path = entry.get("page_path")
        completeness = entry.get("completeness")
        if not isinstance(framework_id, str) or framework_id in seen:
            failures.append(f"invalid or duplicate framework id: {framework_id}")
            continue
        seen.add(framework_id)
        if not isinstance(page_path, str):
            failures.append(f"missing page path: {framework_id}")
            continue
        page = ROOT / page_path
        if not page.exists():
            failures.append(f"missing page: {page_path}")
            continue
        text = page.read_text(encoding="utf-8")
        if completeness == "COMPLETE_WITH_EXTERNAL_GATES":
            complete += 1
            for section in required_sections:
                if f"## {section}" not in text:
                    failures.append(f"missing required section for {framework_id}: {section}")
            if "evidence_class: SOURCE_REVIEWED" not in text:
                failures.append(f"missing SOURCE_REVIEWED boundary: {framework_id}")
            if "comparative_testing_claim_allowed: false" not in text:
                failures.append(f"missing comparative-claim boundary: {framework_id}")
            if "execution_authority_claim_allowed: false" not in text:
                failures.append(f"missing execution-authority boundary: {framework_id}")
        elif completeness == "PARTIAL":
            partial += 1
        else:
            failures.append(f"invalid completeness class for {framework_id}: {completeness}")

    if complete != counts.get("complete_with_external_gates"):
        failures.append("complete_with_external_gates count is stale")
    if partial != counts.get("partial"):
        failures.append("partial count is stale")
    if complete + partial != len(entries):
        failures.append("completeness totals do not cover cohort")

    print("EXTERNAL FRAMEWORK PAGE REMEDIATION:", "FAIL" if failures else "PASS")
    print(f"cohort_pages={len(entries)}")
    print(f"complete_with_external_gates={complete}")
    print(f"partial={partial}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
