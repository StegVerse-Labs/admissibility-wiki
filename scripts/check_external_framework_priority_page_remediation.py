#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/external-frameworks/priority-agent-guardrail-page-remediation.v1.json"


def main() -> int:
    failures: list[str] = []
    if not STATUS.exists():
        print("EXTERNAL FRAMEWORK PRIORITY PAGE REMEDIATION: FAIL")
        print(f"- missing status artifact: {STATUS.relative_to(ROOT)}")
        return 1

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    groups = data.get("required_semantic_sections", [])
    counts = data.get("counts", {})
    if data.get("schema") != "external_framework_page_remediation.v1":
        failures.append("unexpected schema")
    if len(entries) != counts.get("cohort_pages"):
        failures.append("cohort page count is stale")

    complete = 0
    pending = 0
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
            for aliases in groups:
                if not any(f"## {alias}" in text for alias in aliases):
                    failures.append(f"missing semantic section for {framework_id}: {' | '.join(aliases)}")
            for boundary in [
                "page_completeness: COMPLETE_WITH_EXTERNAL_GATES",
                "independent_reproduction: false",
                "comparative_testing_claim_allowed: false",
                "execution_authority_claim_allowed: false",
            ]:
                if boundary not in text:
                    failures.append(f"missing boundary for {framework_id}: {boundary}")
            if "Publication does not create standing" not in text:
                failures.append(f"missing publication-standing boundary: {framework_id}")
        elif completeness in {"PENDING_REVIEW", "PARTIAL"}:
            pending += 1
        else:
            failures.append(f"invalid completeness class for {framework_id}: {completeness}")

    if complete != counts.get("complete_with_external_gates"):
        failures.append("complete_with_external_gates count is stale")
    if pending != counts.get("partial_or_pending_review"):
        failures.append("partial_or_pending_review count is stale")
    if complete + pending != len(entries):
        failures.append("completeness totals do not cover cohort")

    print("EXTERNAL FRAMEWORK PRIORITY PAGE REMEDIATION:", "FAIL" if failures else "PASS")
    print(f"cohort_pages={len(entries)}")
    print(f"complete_with_external_gates={complete}")
    print(f"partial_or_pending_review={pending}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
