#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "docs" / "external-frameworks" / "generated-page-closeout-bundle.json"
GENERATION_CHECK = ROOT / "scripts" / "check_generated_page_closeout_state_generation.py"
ACTIVATION_GATE_CHECK = ROOT / "scripts" / "check_generated_page_activation_gate.py"

REQUIRED_ARTIFACTS = [
    "docs/external-frameworks/generated-page-validation-summary.json",
    "docs/external-frameworks/generated-page-progress.json",
    "docs/external-frameworks/generated-page-release-readiness.json",
    "docs/external-frameworks/generated-page-downstream-tasks.json",
    "docs/external-frameworks/generated-page-ci-evidence-request.json",
    "docs/external-frameworks/generated-page-tag-candidate.json",
]


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

    data = json.loads(BUNDLE.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_closeout_bundle":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("closeout_ready") is not False:
        failures.append("closeout must remain blocked before green CI evidence")
    if data.get("closeout_percent") != 96:
        failures.append("closeout percent mismatch")

    for artifact in REQUIRED_ARTIFACTS:
        if artifact not in data.get("required_artifacts", []):
            failures.append(f"missing required artifact: {artifact}")
        elif not (ROOT / artifact).exists():
            failures.append(f"required artifact file missing: {artifact}")

    if len(data.get("blocked_by", [])) < 4:
        failures.append("blocked-by list incomplete")
    if data.get("next_integration_goal_candidate") != "post-release downstream generated-framework-results propagation":
        failures.append("next integration goal mismatch")

    boundary = data.get("boundary", {})
    if boundary.get("closeout_bundle_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("manual_closeout_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")
    if boundary.get("thread_archive_ready") is not False:
        failures.append("archive boundary mismatch")

    run_optional_check(GENERATION_CHECK, "closeout state generation check", failures)
    run_optional_check(ACTIVATION_GATE_CHECK, "activation gate check", failures)

    print("GENERATED PAGE CLOSEOUT BUNDLE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
