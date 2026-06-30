#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "external-frameworks" / "generated-page-candidates.json"


def main() -> int:
    failures: list[str] = []
    if not STATE.exists():
        print("EXTERNAL FRAMEWORK PAGE CANDIDATES: FAIL")
        print("- generated-page-candidates.json missing")
        return 1

    data = json.loads(STATE.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_candidates":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.2":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")

    surfaces = data.get("active_generated_page_surfaces", [])
    for surface in ["metadata", "mapping", "page_status", "analysis_boundary"]:
        if surface not in surfaces:
            failures.append(f"missing active surface: {surface}")

    active = data.get("active_via_existing_generators", [])
    if not any(item.get("surface_id") == "external_framework_page_analysis_boundary" for item in active):
        failures.append("analysis boundary active record missing")

    removed = data.get("manual_tasks_removed", [])
    if "external_framework_analysis_boundary_wiring" not in removed:
        failures.append("manual wiring task not removed")

    print("EXTERNAL FRAMEWORK PAGE CANDIDATES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
