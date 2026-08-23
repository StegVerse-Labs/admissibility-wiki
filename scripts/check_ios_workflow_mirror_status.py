#!/usr/bin/env python3
"""Validate the iOS-safe workflow mirror against the canonical workflow.

The mirror is a usability copy for clients that cannot create leading-period paths.
It is never activation evidence. A synchronized mirror must match the canonical
workflow byte-for-byte; a divergent mirror is permitted only when the status and
controlled patch record both describe the delta explicitly.
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
    "Validate ASRO commitment candidate",
    "Validate governed LLM public pages",
    "Validate governed LLM demo docs",
    "Validate iOS workflow mirror status",
    "Validate admissibility automation handoff",
    "Verify governed LLM route set",
    "Verify ASRO external framework page",
    "not activation evidence",
)

COMMON_STATUS = {
    "schema": "ios_workflow_mirror_status.v1",
    "repository": "StegVerse-Labs/admissibility-wiki",
    "canonical_workflow": ".github/workflows/validate-chain-continuation.yml",
    "ios_safe_mirror": "iosnoperiod/github/workflows/validate-chain-continuation.yml",
    "patch_note": "iosnoperiod/github/workflows/validate-chain-continuation.patch.md",
    "guard": "scripts/check_ios_workflow_mirror_status.py",
    "npm_script": "validate:ios-workflow-mirror",
    "main_validation_chain": "included",
}


def load_status(failures: list[str]) -> dict:
    if not STATUS.exists():
        failures.append("missing iOS workflow mirror status artifact")
        return {}
    try:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"unreadable iOS workflow mirror status artifact: {exc}")
        return {}
    for key, expected in COMMON_STATUS.items():
        if data.get(key) != expected:
            failures.append(f"status artifact mismatch: {key}")
    boundary = data.get("boundary", {})
    if boundary.get("mirror_is_activation_evidence") is not False:
        failures.append("status boundary mismatch: mirror_is_activation_evidence")
    if boundary.get("patch_note_is_activation_evidence") is not False:
        failures.append("status boundary mismatch: patch_note_is_activation_evidence")
    if boundary.get("canonical_workflow_remains_source_of_truth") is not True:
        failures.append("status boundary mismatch: canonical_workflow_remains_source_of_truth")
    return data


def main() -> int:
    failures: list[str] = []
    if not CANONICAL.exists():
        failures.append("missing canonical workflow")
    if not MIRROR.exists():
        failures.append("missing iOS workflow mirror")

    status = load_status(failures)
    if failures:
        print("IOS WORKFLOW MIRROR: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    canonical_text = CANONICAL.read_text(encoding="utf-8")
    mirror_text = MIRROR.read_text(encoding="utf-8")
    boundary = status.get("boundary", {})

    if canonical_text == mirror_text:
        if status.get("status") != "synchronized":
            failures.append("mirror content is synchronized but status is not synchronized")
        if status.get("expected_result") != "IOS WORKFLOW MIRROR: PASS - mirror synchronized with canonical workflow":
            failures.append("synchronized expected_result mismatch")
        if boundary.get("mirror_must_not_be_used_as_current_workflow_until_synced") is not False:
            failures.append("synchronized mirror must clear stale-use prohibition")
        if failures:
            print("IOS WORKFLOW MIRROR: FAIL")
            for failure in failures:
                print(f"- {failure}")
            return 1
        print("IOS WORKFLOW MIRROR: PASS - mirror synchronized with canonical workflow")
        return 0

    if status.get("status") != "patched_delta_recorded":
        failures.append("mirror differs from canonical workflow but status is not patched_delta_recorded")
    if boundary.get("mirror_must_not_be_used_as_current_workflow_until_synced") is not True:
        failures.append("divergent mirror must preserve stale-use prohibition")
    if not PATCH.exists():
        failures.append("mirror differs from canonical workflow and no patch note exists")
    else:
        patch_text = PATCH.read_text(encoding="utf-8")
        for marker in REQUIRED_PATCH_MARKERS:
            if marker not in patch_text:
                failures.append(f"patch note missing marker: {marker}")

    if failures:
        print("IOS WORKFLOW MIRROR: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("IOS WORKFLOW MIRROR: PATCHED - mirror differs from canonical workflow; controlled patch note present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
