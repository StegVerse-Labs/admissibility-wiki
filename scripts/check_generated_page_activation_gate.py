#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "docs" / "external-frameworks" / "generated-page-activation-gate.json"

REQUIRED_TO_ACTIVATE = [
    "current single canonical workflow conclusion is success",
    "public GitHub Pages root verification is success",
    "public generated evaluation results page verification is success",
    "GOAL_STATE is promoted to the current generated closeout-state checkpoint",
]

REQUIRED_FAIL_CLOSED = [
    "green CI evidence is recorded after the validation summary generation checkpoint",
    "public verification evidence is recorded after the validation summary generation checkpoint",
]


def main() -> int:
    failures: list[str] = []
    if not GATE.exists():
        print("GENERATED PAGE ACTIVATION GATE: FAIL")
        print("- activation gate missing")
        return 1

    data = json.loads(GATE.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_activation_gate":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("activation_ready") is not False:
        failures.append("activation must remain false until CI/public evidence is recorded")
    if data.get("activation_percent") != 98:
        failures.append("activation percent mismatch")

    required = data.get("required_to_activate", [])
    for item in REQUIRED_TO_ACTIVATE:
        if item not in required:
            failures.append(f"missing activation requirement: {item}")

    fail_closed = data.get("fail_closed_until", [])
    for item in REQUIRED_FAIL_CLOSED:
        if item not in fail_closed:
            failures.append(f"missing fail-closed condition: {item}")

    boundary = data.get("boundary", {})
    if boundary.get("activation_gate_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("missing_evidence_blocks_activation") is not True:
        failures.append("missing evidence boundary mismatch")
    if boundary.get("manual_activation_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("thread_archive_ready") is not False:
        failures.append("archive boundary mismatch")

    print("GENERATED PAGE ACTIVATION GATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
