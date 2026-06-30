#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = ROOT / "docs" / "external-frameworks" / "generated-page-tag-candidate.json"
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

    data = json.loads(TAG.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_tag_candidate":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("tag_candidate") != "v0.1.0-generated-framework-pages":
        failures.append("tag candidate mismatch")
    if data.get("tag_ready") is not False:
        failures.append("tag must remain blocked before green CI evidence")

    for artifact in REQUIRED_ARTIFACTS:
        if artifact not in data.get("required_artifacts", []):
            failures.append(f"missing required artifact: {artifact}")
        elif not (ROOT / artifact).exists():
            failures.append(f"required artifact file missing: {artifact}")

    if len(data.get("blocked_by", [])) < 3:
        failures.append("blocked-by list incomplete")

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
