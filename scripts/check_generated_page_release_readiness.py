#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READY = ROOT / "docs" / "external-frameworks" / "generated-page-release-readiness.json"

REQUIRED_BEFORE_TAG = [
    "single canonical workflow green after validation summary generation installation",
    "public GitHub Pages verification green",
    "generated external-framework evaluation results reachable on public site",
    "GOAL_STATE promoted after validator update is unblocked",
    "downstream update tasks created for StegVerse-Labs/Site, GCAT-BCAT-Engine/Publisher, and stegguardian-wiki",
]

REQUIRED_SATISFIED = [
    "single workflow policy preserved",
    "generated-page validation summary installed",
    "generated-page validation summary generation check installed",
    "machine-readable progress state installed",
    "downstream task manifest installed",
    "CI evidence request installed",
    "tag candidate gate installed",
    "closeout bundle installed",
]


def main() -> int:
    failures: list[str] = []
    if not READY.exists():
        print("GENERATED PAGE RELEASE READINESS: FAIL")
        print("- readiness file missing")
        return 1

    data = json.loads(READY.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_release_readiness":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("release_ready") is not False:
        failures.append("release readiness must remain false before green CI and downstream tasks")
    if data.get("readiness_percent") != 96:
        failures.append("readiness percent mismatch")

    before_tag = data.get("required_before_tag", [])
    for item in REQUIRED_BEFORE_TAG:
        if item not in before_tag:
            failures.append(f"missing before-tag blocker: {item}")

    satisfied = data.get("already_satisfied", [])
    for item in REQUIRED_SATISFIED:
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
