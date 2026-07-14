#!/usr/bin/env python3
"""Fail closed when AI-led radiology activation records drift apart."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_POINTER = ROOT / "ADMISSIBILITY_MIRROR_HANDOFF.md"
REPO_HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
ACTIVATION_HANDOFF = ROOT / "docs" / "AI_LED_RADIOLOGY_MIRROR_HANDOFF.md"
STATUS = ROOT / "static" / "status" / "ai-led-radiology-execution-status.json"

REQUIRED_ACTIVATION_MARKERS = (
    "Goal id: ai-led-radiology-execution-boundary",
    "Manual task requirement: NONE",
    "User manual action required: false",
    "scripts/check_ai_led_radiology_execution.py",
    "scripts/check_ai_led_radiology_publication.py",
    "scripts/check_ai_led_radiology_handoff_sync.py",
    "reports/ai-led-radiology-execution-receipt.json",
    "The complete thread is ready for archiving",
)

REQUIRED_STATUS_VALUES = {
    "goal_id": "ai-led-radiology-execution-boundary",
    "manual_task_requirement": "NONE",
    "user_manual_action_required": False,
    "additional_active_workflow_created": False,
}


def main() -> int:
    failures: list[str] = []

    for path in (ROOT_POINTER, REPO_HANDOFF, ACTIVATION_HANDOFF, STATUS):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if failures:
        print("AI-LED RADIOLOGY HANDOFF SYNC: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    pointer_text = ROOT_POINTER.read_text(encoding="utf-8")
    if "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md" not in pointer_text:
        failures.append("root pointer does not preserve overall repository handoff")
    if "docs/AI_LED_RADIOLOGY_MIRROR_HANDOFF.md" not in pointer_text:
        failures.append("root pointer does not reference radiology activation handoff")

    activation_text = ACTIVATION_HANDOFF.read_text(encoding="utf-8")
    for marker in REQUIRED_ACTIVATION_MARKERS:
        if marker not in activation_text:
            failures.append(f"activation handoff missing marker: {marker}")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    for key, expected in REQUIRED_STATUS_VALUES.items():
        if status.get(key) != expected:
            failures.append(f"status {key!r} expected {expected!r}, got {status.get(key)!r}")

    automation = status.get("automation")
    if not isinstance(automation, dict):
        failures.append("status automation must be an object")
    else:
        if automation.get("receipt_generation_automatic") is not True:
            failures.append("receipt generation is not marked automatic")
        if automation.get("public_navigation_installed") is not True:
            failures.append("public navigation is not marked installed")
        if automation.get("handoff_sync_validation") is not True:
            failures.append("handoff sync validation is not marked active")

    remaining_owner = status.get("remaining_owner")
    if remaining_owner != "CANONICAL_AUTOMATION_AND_FUTURE_HANDOFF_RECONCILIATION":
        failures.append("remaining ownership is not assigned to canonical automation")

    if failures:
        print("AI-LED RADIOLOGY HANDOFF SYNC: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("AI-LED RADIOLOGY HANDOFF SYNC: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
