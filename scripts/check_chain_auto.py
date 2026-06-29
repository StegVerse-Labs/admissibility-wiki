#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTO = ROOT / "docs" / "CHAIN_AUTO.json"

REQUIRED_COMMANDS = [
    "python scripts/check_chain_status_continuation.py",
    "python scripts/check_continuation_bundle.py",
    "python scripts/check_chain_snapshot.py",
    "python scripts/check_chain_snapshot_receipt.py",
    "python scripts/check_chain_auto.py",
    "python scripts/check_blocked_destination_record.py",
    "python scripts/check_goal_state.py",
    "python scripts/check_workflow_manifest.py",
    "python scripts/check_external_frameworks_index.py",
    "python scripts/check_external_framework_manifests.py",
    "python scripts/check_external_framework_terminology.py",
    "python scripts/check_external_framework_reports.py",
    "python scripts/check_external_framework_report_coverage.py",
    "python scripts/check_external_framework_report_generation.py",
    "python scripts/check_external_framework_expansion_policy.py",
    "python scripts/check_ci_evidence.py",
    "python scripts/check_guardian_destination.py",
]

REQUIRED_TESTBENCH_REPORTS = [
    "docs/external-frameworks/reports/admissible-existence-seed-cycle.compatibility.json",
    "docs/external-frameworks/reports/care-runtime.compatibility.json",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    if not AUTO.exists():
        print("CHAIN AUTO: FAIL")
        print("- missing docs/CHAIN_AUTO.json")
        return 1

    data = load_json(AUTO)

    if data.get("artifact_type") != "chain_auto_state":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "1.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("canonical_workflow") != ".github/workflows/validate-chain-continuation.yml":
        failures.append("canonical workflow mismatch")
    if data.get("mirror_workflow") != "iosnoperiod/github/workflows/validate-chain-continuation.yml":
        failures.append("mirror workflow mismatch")
    if data.get("schedule") != "17 9 * * *":
        failures.append("schedule mismatch")
    if data.get("remaining_state") != "WAITING_FOR_DOWNSTREAM_REPO_EXTERNAL_FRAMEWORK_SOURCES_AND_CI_EVIDENCE":
        failures.append("remaining state mismatch")
    if data.get("generator") != "scripts/generate_external_framework_reports.py":
        failures.append("generator mismatch")
    elif not (ROOT / data["generator"]).exists():
        failures.append("generator file missing")
    if data.get("ci_evidence") != "docs/CI_EVIDENCE.json":
        failures.append("CI evidence path mismatch")
    elif not (ROOT / data["ci_evidence"]).exists():
        failures.append("CI evidence file missing")

    for path_key in ["canonical_workflow", "mirror_workflow"]:
        path = data.get(path_key)
        if not isinstance(path, str) or not (ROOT / path).exists():
            failures.append(f"missing referenced path: {path_key}")

    commands = data.get("commands", [])
    for command in REQUIRED_COMMANDS:
        if command not in commands:
            failures.append(f"missing command: {command}")

    reports = data.get("testbench_reports", [])
    for report in REQUIRED_TESTBENCH_REPORTS:
        if report not in reports:
            failures.append(f"missing testbench report: {report}")
        elif not (ROOT / report).exists():
            failures.append(f"testbench report missing from repo: {report}")

    removed = data.get("manual_tasks_removed", [])
    for task in ["workflow_install", "repeat_destination_search"]:
        if task not in removed:
            failures.append(f"manual task not removed: {task}")

    print("CHAIN AUTO:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
