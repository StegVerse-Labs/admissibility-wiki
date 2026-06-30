#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "docs" / "external-frameworks" / "generated-page-activation-gate.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"


def main() -> int:
    failures: list[str] = []
    if not GATE.exists():
        print("GENERATED PAGE ACTIVATION GATE: FAIL")
        print("- activation gate missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE ACTIVATION GATE: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(GATE.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    activation = model.get("activation", {})

    if data.get("artifact_type") != "generated_page_activation_gate":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("activation_ready") != activation.get("activation_ready"):
        failures.append("activation readiness mismatch")
    if data.get("activation_percent") != activation.get("activation_percent"):
        failures.append("activation percent mismatch")

    required = data.get("required_to_activate", [])
    for item in activation.get("required_to_activate", []):
        if item not in required:
            failures.append(f"missing activation requirement: {item}")

    fail_closed = data.get("fail_closed_until", [])
    for item in activation.get("fail_closed_until", []):
        if item not in fail_closed:
            failures.append(f"missing fail-closed condition: {item}")

    boundary = data.get("boundary", {})
    model_boundary = model.get("boundary", {})
    if boundary.get("activation_gate_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("missing_evidence_blocks_activation") != model_boundary.get("missing_public_evidence_blocks_activation"):
        failures.append("missing evidence boundary mismatch")
    if boundary.get("manual_activation_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("thread_archive_ready") != model_boundary.get("thread_archive_ready"):
        failures.append("archive boundary mismatch")

    print("GENERATED PAGE ACTIVATION GATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
