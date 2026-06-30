#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs" / "external-frameworks" / "generated-page-workflow-entrypoint-migration.json"
ENTRYPOINT = "python scripts/run_canonical_validation.py"


def main() -> int:
    failures: list[str] = []
    if not RECORD.exists():
        print("GENERATED PAGE WORKFLOW ENTRYPOINT MIGRATION: FAIL")
        print("- migration record missing")
        return 1

    data = json.loads(RECORD.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_workflow_entrypoint_migration":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("local_entrypoint") != ENTRYPOINT:
        failures.append("local entrypoint mismatch")
    if not (ROOT / "scripts" / "run_canonical_validation.py").exists():
        failures.append("local entrypoint script missing")

    completed_paths = {item.get("path") for item in data.get("completed", [])}
    for path in ["scripts/run_canonical_validation.py", "workflow_manifest.json", "scripts/check_workflow_manifest.py"]:
        if path not in completed_paths:
            failures.append(f"completed install missing: {path}")

    pending = data.get("pending_install", [])
    if len(pending) != 2:
        failures.append("pending install count mismatch")
    for item in pending:
        if item.get("state") != "connector_blocked":
            failures.append("pending install state mismatch")
        if not item.get("display_path"):
            failures.append("pending install display path missing")

    boundary = data.get("boundary", {})
    if boundary.get("migration_record_is_authority") is not False:
        failures.append("migration record authority boundary mismatch")
    if boundary.get("workflow_replacement_complete") is not False:
        failures.append("workflow replacement boundary mismatch")
    if boundary.get("manual_workflow_install_required") is not False:
        failures.append("manual workflow boundary mismatch")
    if boundary.get("connector_block_blocks_goal_activation") is not True:
        failures.append("connector block activation boundary mismatch")
    if boundary.get("local_entrypoint_is_authority") is not False:
        failures.append("local entrypoint authority boundary mismatch")
    if boundary.get("missing_ci_fails_closed") is not True:
        failures.append("missing CI boundary mismatch")

    print("GENERATED PAGE WORKFLOW ENTRYPOINT MIGRATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
