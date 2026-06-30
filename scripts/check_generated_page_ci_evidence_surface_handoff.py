#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDENDUM = ROOT / "docs" / "external-frameworks" / "generated-page-ci-evidence-surface-handoff.json"
SURFACES = ROOT / "docs" / "external-frameworks" / "generated-page-surfaces.json"
SURFACE_ID = "ci_evidence_request"


def main() -> int:
    failures: list[str] = []
    if not ADDENDUM.exists():
        print("GENERATED PAGE CI EVIDENCE SURFACE HANDOFF: FAIL")
        print("- handoff addendum missing")
        return 1
    if not SURFACES.exists():
        print("GENERATED PAGE CI EVIDENCE SURFACE HANDOFF: FAIL")
        print("- surface inventory missing")
        return 1

    data = json.loads(ADDENDUM.read_text(encoding="utf-8"))
    surfaces = json.loads(SURFACES.read_text(encoding="utf-8"))
    active = {item.get("surface_id"): item for item in surfaces.get("active_surfaces", [])}
    surface = active.get(SURFACE_ID)

    if data.get("artifact_type") != "generated_page_ci_evidence_surface_handoff":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("surface_id") != SURFACE_ID:
        failures.append("surface id mismatch")
    if data.get("manual_task_required") is not False:
        failures.append("manual task boundary mismatch")

    if not surface:
        failures.append("surface inventory missing CI evidence request")
    else:
        for key in ["generator", "validator"]:
            if data.get(key) != surface.get(key):
                failures.append(f"{key} mismatch")
            if not (ROOT / str(data.get(key))).exists():
                failures.append(f"referenced {key} missing")

    boundary = data.get("boundary", {})
    if boundary.get("handoff_addendum_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_surface_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("single_workflow_policy_preserved") is not True:
        failures.append("single workflow boundary mismatch")

    print("GENERATED PAGE CI EVIDENCE SURFACE HANDOFF:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
