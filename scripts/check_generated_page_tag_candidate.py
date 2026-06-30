#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = ROOT / "docs" / "external-frameworks" / "generated-page-tag-candidate.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"
CLOSEOUT_CHECK = ROOT / "scripts" / "check_generated_page_closeout_bundle.py"

REQUIRED_ARTIFACTS = [
    "docs/external-frameworks/generated-page-progress.json",
    "docs/external-frameworks/generated-page-release-readiness.json",
    "docs/external-frameworks/generated-page-downstream-tasks.json",
    "docs/external-frameworks/generated-page-ci-evidence-request.json",
]


def main() -> int:
    failures: list[str] = []
    if not TAG.exists():
        print("GENERATED PAGE TAG CANDIDATE: FAIL")
        print("- tag candidate missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE TAG CANDIDATE: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(TAG.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    tag = model.get("tag", {})

    if data.get("artifact_type") != "generated_page_tag_candidate":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("tag_candidate") != tag.get("tag_candidate"):
        failures.append("tag candidate mismatch")
    if data.get("tag_ready") != tag.get("tag_ready"):
        failures.append("tag ready mismatch")

    for artifact in REQUIRED_ARTIFACTS:
        if artifact not in data.get("required_artifacts", []):
            failures.append(f"missing required artifact: {artifact}")
        elif not (ROOT / artifact).exists():
            failures.append(f"required artifact file missing: {artifact}")

    blocked_by = data.get("blocked_by", [])
    for item in tag.get("blocked_by", []):
        if item not in blocked_by:
            failures.append(f"missing blocker: {item}")

    boundary = data.get("boundary", {})
    if boundary.get("tag_candidate_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("tag_ready_without_green_ci_allowed") is not False:
        failures.append("green CI boundary mismatch")
    if boundary.get("manual_tag_readiness_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")

    if CLOSEOUT_CHECK.exists():
        result = subprocess.run(["python", str(CLOSEOUT_CHECK)], check=False)
        if result.returncode != 0:
            failures.append("closeout bundle check failed")

    print("GENERATED PAGE TAG CANDIDATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
