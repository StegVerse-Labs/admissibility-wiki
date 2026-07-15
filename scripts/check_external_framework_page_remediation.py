#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/external-frameworks/policy-identity-provenance-page-remediation.v1.json"


def has_any_heading(text: str, aliases: list[str]) -> bool:
    return any(f"## {alias}" in text for alias in aliases)


def has_any_marker(text: str, markers: list[str]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def main() -> int:
    failures: list[str] = []
    if not STATUS.exists():
        print("EXTERNAL FRAMEWORK PAGE REMEDIATION: FAIL")
        print(f"- missing status artifact: {STATUS.relative_to(ROOT)}")
        return 1

    data = json.loads(STATUS.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    required_groups = data.get("required_section_groups", [])
    counts = data.get("counts", {})

    if data.get("schema") != "external_framework_page_remediation.v1":
        failures.append("unexpected schema")
    if len(entries) != counts.get("cohort_pages"):
        failures.append("cohort page count is stale")
    if not required_groups or not all(isinstance(group, list) and group for group in required_groups):
        failures.append("required_section_groups must be a non-empty list of alias groups")

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
            for aliases in required_groups:
                if not has_any_heading(text, aliases):
                    failures.append(
                        f"missing required section group for {framework_id}: " + " | ".join(aliases)
                    )
            if not has_any_marker(text, ["evidence_class: SOURCE_REVIEWED", "Evidence class: SOURCE_REVIEWED"]):
                failures.append(f"missing SOURCE_REVIEWED boundary: {framework_id}")
            if not has_any_marker(
                text,
                ["comparative_testing_claim_allowed: false", "Comparative testing claim allowed: false"],
            ):
                failures.append(f"missing comparative-claim boundary: {framework_id}")
            if not has_any_marker(
                text,
                ["execution_authority_claim_allowed: false", "Execution authority claim allowed: false"],
            ):
                failures.append(f"missing execution-authority boundary: {framework_id}")
            if "Publication does not create standing" not in text:
                failures.append(f"missing publication-standing boundary: {framework_id}")
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
    if counts.get("partial") == 0 and complete != len(entries):
        failures.append("closed cohort must classify every page COMPLETE_WITH_EXTERNAL_GATES")

    print("EXTERNAL FRAMEWORK PAGE REMEDIATION:", "FAIL" if failures else "PASS")
    print(f"cohort_pages={len(entries)}")
    print(f"complete_with_external_gates={complete}")
    print(f"partial={partial}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
