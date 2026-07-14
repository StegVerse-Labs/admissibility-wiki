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
WRITER = ROOT / "scripts" / "write-public-activation-receipt.mjs"
WRITER_CHECK = ROOT / "scripts" / "check-public-activation-receipt-writer.mjs"

REQUIRED_ACTIVATION_MARKERS = (
    "Goal id: ai-led-radiology-execution-boundary",
    "Manual task requirement: NONE",
    "User manual action required: false",
    "scripts/check_ai_led_radiology_execution.py",
    "scripts/check_ai_led_radiology_publication.py",
    "scripts/check_ai_led_radiology_handoff_sync.py",
    "reports/ai-led-radiology-execution-receipt.json",
    "activation_closures.ai_led_radiology",
    "ai_led_radiology_activation_closure.v1",
    "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE",
    "handoff_reconciliation_required_for_continuation == false",
    "The complete thread is ready for archiving",
)

REQUIRED_STATUS_VALUES = {
    "goal_id": "ai-led-radiology-execution-boundary",
    "manual_task_requirement": "NONE",
    "user_manual_action_required": False,
    "additional_active_workflow_created": False,
    "activation_closure_schema": "ai_led_radiology_activation_closure.v1",
}


def main() -> int:
    failures: list[str] = []

    for path in (ROOT_POINTER, REPO_HANDOFF, ACTIVATION_HANDOFF, STATUS, WRITER, WRITER_CHECK):
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
        required_true = (
            "receipt_generation_automatic",
            "public_navigation_installed",
            "handoff_sync_validation",
            "live_evidence_uploaded_by_existing_workflow",
            "closure_evaluation_automatic",
            "closure_embedded_in_uploaded_receipt",
        )
        for key in required_true:
            if automation.get(key) is not True:
                failures.append(f"status automation {key!r} is not true")
        if automation.get("handoff_reconciliation_required_for_continuation") is not False:
            failures.append("handoff reconciliation is incorrectly required for continuation")

    if status.get("remaining_owner") != "CANONICAL_AUTOMATION":
        failures.append("remaining ownership is not assigned exclusively to canonical automation")

    completion_rule = status.get("completion_rule", "")
    for marker in (
        "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE",
        "all_required_public_routes_verified == true",
        "without a follow-up handoff edit",
    ):
        if marker not in completion_rule:
            failures.append(f"completion rule missing marker: {marker}")

    writer_text = WRITER.read_text(encoding="utf-8")
    for marker in (
        "ai_led_radiology_activation_closure.v1",
        "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE",
        "handoff_reconciliation_required_for_continuation: false",
        "activation_closures",
    ):
        if marker not in writer_text:
            failures.append(f"receipt writer missing closure marker: {marker}")

    writer_check_text = WRITER_CHECK.read_text(encoding="utf-8")
    for marker in (
        "missing AI-led radiology activation closure",
        "SIMULATED_VALIDATOR_PASS",
        "handoff_reconciliation_required_for_continuation",
    ):
        if marker not in writer_check_text:
            failures.append(f"receipt writer validator missing marker: {marker}")

    if failures:
        print("AI-LED RADIOLOGY HANDOFF SYNC: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("AI-LED RADIOLOGY HANDOFF SYNC: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())