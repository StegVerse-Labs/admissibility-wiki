#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "docs" / "external-frameworks" / "generated-page-closeout-bundle.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"
GENERATION_CHECK = ROOT / "scripts" / "check_generated_page_closeout_state_generation.py"
ACTIVATION_GATE_CHECK = ROOT / "scripts" / "check_generated_page_activation_gate.py"


def run_optional_check(path: Path, label: str, failures: list[str]) -> None:
    if path.exists():
        result = subprocess.run(["python", str(path)], check=False)
        if result.returncode != 0:
            failures.append(f"{label} failed")


def main() -> int:
    failures: list[str] = []
    if not BUNDLE.exists():
        print("GENERATED PAGE CLOSEOUT BUNDLE: FAIL")
        print("- closeout bundle missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE CLOSEOUT BUNDLE: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(BUNDLE.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    tag = model.get("tag", {})

    if data.get("artifact_type") != "generated_page_closeout_bundle":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("closeout_ready") is not False:
        failures.append("closeout must remain blocked before release authorization")
    if data.get("closeout_percent") != model.get("repo_percent_complete"):
        failures.append("closeout percent mismatch")

    declared_outputs = set(model.get("generated_outputs", []))
    required_artifacts = data.get("required_artifacts", [])
    for artifact in required_artifacts:
        if artifact not in declared_outputs:
            failures.append(f"required artifact not declared by state model: {artifact}")
        elif not (ROOT / artifact).exists():
            failures.append(f"required artifact file missing: {artifact}")
    for artifact in declared_outputs:
        if artifact not in required_artifacts:
            failures.append(f"declared generated output missing from closeout: {artifact}")

    blocked_by = data.get("blocked_by", [])
    for item in tag.get("blocked_by", []):
        if item not in blocked_by:
            failures.append(f"missing closeout blocker: {item}")

    if data.get("next_integration_goal_candidate") != "post-release downstream generated-framework-results propagation":
        failures.append("next integration goal mismatch")

    boundary = data.get("boundary", {})
    if boundary.get("closeout_bundle_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_closeout_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("thread_archive_ready") != model.get("boundary", {}).get("thread_archive_ready"):
        failures.append("archive boundary mismatch")

    run_optional_check(GENERATION_CHECK, "closeout state generation check", failures)
    run_optional_check(ACTIVATION_GATE_CHECK, "activation gate check", failures)

    print("GENERATED PAGE CLOSEOUT BUNDLE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
