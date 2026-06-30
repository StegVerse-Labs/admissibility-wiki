#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READY = ROOT / "docs" / "external-frameworks" / "generated-page-release-readiness.json"
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"


def main() -> int:
    failures: list[str] = []
    if not READY.exists():
        print("GENERATED PAGE RELEASE READINESS: FAIL")
        print("- readiness file missing")
        return 1
    if not MODEL.exists():
        print("GENERATED PAGE RELEASE READINESS: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(READY.read_text(encoding="utf-8"))
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    release = model.get("release", {})

    if data.get("artifact_type") != "generated_page_release_readiness":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != model.get("repo"):
        failures.append("repo mismatch")
    if data.get("active_goal") != model.get("active_goal"):
        failures.append("active goal mismatch")
    if data.get("release_ready") != release.get("release_ready"):
        failures.append("release readiness mismatch")
    if data.get("readiness_percent") != release.get("readiness_percent"):
        failures.append("readiness percent mismatch")

    before_tag = data.get("required_before_tag", [])
    for item in release.get("required_before_tag", []):
        if item not in before_tag:
            failures.append(f"missing before-tag blocker: {item}")

    satisfied = data.get("already_satisfied", [])
    for item in release.get("already_satisfied", []):
        if item not in satisfied:
            failures.append(f"missing satisfied item: {item}")

    boundary = data.get("boundary", {})
    if boundary.get("release_readiness_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("tag_without_green_ci_allowed") is not False:
        failures.append("tag boundary mismatch")
    if boundary.get("manual_release_readiness_reconstruction_required") is not False:
        failures.append("manual reconstruction boundary mismatch")

    print("GENERATED PAGE RELEASE READINESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
