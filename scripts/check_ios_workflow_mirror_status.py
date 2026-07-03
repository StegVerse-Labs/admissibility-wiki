#!/usr/bin/env python3
"""Check whether the iOS-safe workflow mirror is synchronized or explicitly patched.

The mirror is a usability copy for clients that cannot create leading-period paths.
It is not activation evidence. This guard fails only when the canonical workflow
changes and neither a synced mirror nor a patch note records the delta.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"
PATCH = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.patch.md"
STATUS = ROOT / "static" / "status" / "ios-workflow-mirror-status.json"

REQUIRED_PATCH_MARKERS = (
    "Validate governed LLM public pages",
    "Validate governed LLM demo docs",
    "Verify governed LLM route set",
    "not activation evidence",
)

REQUIRED_STATUS = {
    "schema": "ios_workflow_mirror_status.v1",
    "repository": "StegVerse-Labs/admissibility-wiki",
    "canonical_workflow": ".github/workflows/validate-chain-continuation.yml",
    "ios_safe_mirror": "iosnoperiod/github/workflows/validate-chain-continuation.yml",
    "patch_note": "iosnoperiod/github/workflows/validate-chain-continuation.patch.md",
    "status": "patched_delta_recorded",
    "guard": "scripts/check_ios_workflow_mirror_status.py",
    "npm_script": "validate:ios-workflow-mirror",
    "main_validation_chain": "included",
}


def check_status_file(failures: list[str]) -> None:
    if not STATUS.exists():
        failures.append("missing iOS workflow mirror status artifact")
        return
    data = json.loads(STATUS.read_text(encoding="utf-8"))
    for key, expected in REQUIRED_STATUS.items():
        if data.get(key) != expected:
            failures.append(f"status artifact mismatch: {key}")
    boundary = data.get("boundary", {})
    if boundary.get("mirror_is_activation_evidence") is not False:
        failures.append("status boundary mismatch: mirror_is_activation_evidence")
    if boundary.get("patch_note_is_activation_evidence") is not False:
        failures.append("status boundary mismatch: patch_note_is_activation_evidence")
    if boundary.get("canonical_workflow_remains_source_of_truth") is not True:
        failures.append("status boundary mismatch: canonical_workflow_remains_source_of_truth")


def main() -> int:
    failures: list[str] = []

    if not CANONICAL.exists():
        failures.append("missing canonical workflow")
    if not MIRROR.exists():
        failures.append("missing iOS workflow mirror")

    check_status_file(failures)

    if failures:
        print("IOS WORKFLOW MIRROR: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    canonical_text = CANONICAL.read_text(encoding="utf-8")
    mirror_text = MIRROR.read_text(encoding="utf-8")

    if canonical_text == mirror_text:
        print("IOS WORKFLOW MIRROR: PASS - mirror synchronized with canonical workflow")
        return 0

    if not PATCH.exists():
        print("IOS WORKFLOW MIRROR: FAIL")
        print("- mirror differs from canonical workflow and no patch note exists")
        return 1

    patch_text = PATCH.read_text(encoding="utf-8")
    missing_markers = [marker for marker in REQUIRED_PATCH_MARKERS if marker not in patch_text]
    if missing_markers:
        print("IOS WORKFLOW MIRROR: FAIL")
        for marker in missing_markers:
            print(f"- patch note missing marker: {marker}")
        return 1

    print("IOS WORKFLOW MIRROR: PATCHED - mirror differs from canonical workflow; controlled patch note present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
