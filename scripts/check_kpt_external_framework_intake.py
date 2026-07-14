#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "kpt-external-framework-intake-status.json"
SOURCE_QUEUE = ROOT / "static" / "status" / "kpt-source-intake-queue.json"
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
INDEX_PAGE = ROOT / "docs" / "external-frameworks" / "index.md"
MANIFEST = ROOT / "docs" / "external-frameworks" / "kpt.json"
REPORT = ROOT / "docs" / "external-frameworks" / "reports" / "kpt.compatibility.json"
PAGE = ROOT / "docs" / "external-frameworks" / "kpt.md"
SIDEBAR = ROOT / "sidebars.js"
RECEIPT = ROOT / "receipts" / "kpt-source-blocked-intake-2026-07-14.json"
AUTOMATION_RECEIPT = ROOT / "receipts" / "kpt-automation-binding-2026-07-14.json"

REQUIRED_FILES = [STATUS, SOURCE_QUEUE, REGISTRY, INDEX_PAGE, MANIFEST, REPORT, PAGE, SIDEBAR, RECEIPT, AUTOMATION_RECEIPT]
FALSE_BOUNDARIES = {
    "certification_claim",
    "endorsement_claim",
    "execution_authority_claim",
    "commit_time_authority_claim",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            failures.append(f"missing required KPT artifact: {path.relative_to(ROOT)}")
    if failures:
        print("KPT EXTERNAL FRAMEWORK INTAKE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    status = load_json(STATUS)
    source_queue = load_json(SOURCE_QUEUE)
    registry = load_json(REGISTRY)
    manifest = load_json(MANIFEST)
    report = load_json(REPORT)
    receipt = load_json(RECEIPT)
    automation_receipt = load_json(AUTOMATION_RECEIPT)
    page = PAGE.read_text(encoding="utf-8")
    index_page = INDEX_PAGE.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")

    if status.get("framework_id") != "kpt":
        failures.append("status framework_id must be kpt")
    if status.get("source_posture") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("status source posture must remain SOURCE_BLOCKED_FAIL_CLOSED")
    if status.get("manual_task_requirement") != "none":
        failures.append("status must not assign a manual task")
    for key in [
        "manual_validation_required",
        "manual_deployment_required",
        "manual_publication_check_required",
        "manual_source_search_required",
    ]:
        if status.get(key) is not False:
            failures.append(f"status must set {key}=false")
    if status.get("downstream_mutation_authorized") is not False:
        failures.append("status must deny downstream mutation authority")
    source_observation = status.get("source_discovery_observation", {})
    if source_observation.get("result") != "NO_INDEXED_OFFICIAL_SOURCE_IDENTIFIED":
        failures.append("source discovery observation must preserve the no-official-source result")
    if source_observation.get("manual_follow_up_required") is not False:
        failures.append("source discovery observation must not assign manual follow-up")

    if source_queue.get("framework_id") != "kpt":
        failures.append("source queue framework_id must be kpt")
    if source_queue.get("state") != "WAITING_FOR_CANONICAL_OWNER_PUBLISHED_SOURCE":
        failures.append("source queue state mismatch")
    if source_queue.get("manual_task_requirement") != "none":
        failures.append("source queue must not assign manual work")
    if source_queue.get("user_action_required") is not False:
        failures.append("source queue must not require user action")
    if source_queue.get("manual_source_search_required") is not False:
        failures.append("source queue must not require manual source search")

    entries = [entry for entry in registry.get("entries", []) if entry.get("framework_id") == "kpt"]
    if len(entries) != 1:
        failures.append(f"registry must contain exactly one KPT entry, found {len(entries)}")
    else:
        entry = entries[0]
        if entry.get("testbench_state") != "SOURCE_BLOCKED_FAIL_CLOSED":
            failures.append("registry KPT testbench_state must remain SOURCE_BLOCKED_FAIL_CLOSED")
        if entry.get("manifest_path") != "docs/external-frameworks/kpt.json":
            failures.append("registry KPT manifest path mismatch")
        for key in ["claims_certification", "claims_endorsement", "claims_execution_authority"]:
            if entry.get(key) is not False:
                failures.append(f"registry boundary must set {key}=false")

    if manifest.get("framework_id") != "kpt":
        failures.append("manifest framework_id must be kpt")
    if manifest.get("source_version") != "UNVERIFIED_SOURCE_REQUIRED":
        failures.append("manifest source_version must remain UNVERIFIED_SOURCE_REQUIRED")
    if manifest.get("transition_table_mapping", {}).get("execution_authority_claim") is not False:
        failures.append("manifest must deny execution authority")
    for key in FALSE_BOUNDARIES:
        if manifest.get("boundary", {}).get(key) is not False:
            failures.append(f"manifest boundary must set {key}=false")
    if manifest.get("boundary", {}).get("official_source_required_for_completion") is not True:
        failures.append("manifest must require an official source for completion")

    if report.get("framework_id") != "kpt":
        failures.append("report framework_id must be kpt")
    if report.get("result") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("report result must remain SOURCE_BLOCKED_FAIL_CLOSED")
    if report.get("cycle_status") != "SOURCE_BLOCKED_CYCLE_RECORDED":
        failures.append("report cycle status mismatch")
    for key in FALSE_BOUNDARIES:
        if report.get("boundary", {}).get(key) is not False:
            failures.append(f"report boundary must set {key}=false")
    if report.get("boundary", {}).get("official_source_required_for_completion") is not True:
        failures.append("report must require an official source for completion")

    if receipt.get("framework_id") != "kpt":
        failures.append("receipt framework_id must be kpt")
    if receipt.get("intake_state") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("receipt intake state mismatch")

    if automation_receipt.get("framework_id") != "kpt":
        failures.append("automation receipt framework_id must be kpt")
    if automation_receipt.get("source_posture") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("automation receipt source posture mismatch")
    if automation_receipt.get("manual_task_requirement") != "none":
        failures.append("automation receipt must not assign a manual task")
    for key in ["manual_validation_required", "manual_deployment_required", "manual_publication_check_required"]:
        if automation_receipt.get(key) is not False:
            failures.append(f"automation receipt must set {key}=false")

    for phrase in [
        "A KPT decision may become evidence inside a StegVerse Commitment Candidate.",
        "It does not become execution authority by itself.",
        "Result: SOURCE_BLOCKED_FAIL_CLOSED",
    ]:
        if phrase not in page:
            failures.append(f"KPT page missing required boundary text: {phrase}")

    for phrase in [
        "[KPT](./kpt.md)",
        "official source required",
        "KPT -> source-blocked runtime decision state before downstream consequence",
    ]:
        if phrase not in index_page:
            failures.append(f"external framework index missing KPT observatory text: {phrase}")

    if "'external-frameworks/kpt'" not in sidebar:
        failures.append("KPT page is missing from the External Frameworks sidebar")

    print("KPT EXTERNAL FRAMEWORK INTAKE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
