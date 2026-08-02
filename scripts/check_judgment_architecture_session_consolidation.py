#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/status/judgment-architecture-session-consolidation.json"
DOC = ROOT / "docs/session-consolidation/shaun-ralston-judgment-architecture-session-consolidation.md"
HANDOFF = ROOT / "docs/external-frameworks/JUDGMENT_ARCHITECTURE_MIRROR_HANDOFF.md"
TASK_REGISTRY = ROOT / "static/status/wiki-public-anchor-internal-task-registry.judgment-architecture-extension.json"
OBSERVER = ROOT / "scripts/observe_judgment_architecture_source_locator.py"
OBSERVATION = ROOT / "static/status/judgment-architecture-source-locator-observation.json"


def main() -> int:
    failures: list[str] = []
    for path in [STATUS, DOC, HANDOFF, TASK_REGISTRY, OBSERVER, OBSERVATION]:
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("JUDGMENT ARCHITECTURE SESSION CONSOLIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    registry = json.loads(TASK_REGISTRY.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    if status.get("archive_disposition") != "ARCHIVE":
        failures.append("archive_disposition must be ARCHIVE")
    if status.get("canonical_repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("canonical repository mismatch")
    task = status.get("canonical_task", {})
    if task.get("task_id") != "PA-INT-011" or task.get("state") != "MACHINE_OWNED":
        failures.append("PA-INT-011 must be the machine-owned canonical continuation")

    registry_tasks = registry.get("tasks", [])
    matching = [item for item in registry_tasks if isinstance(item, dict) and item.get("task_id") == "PA-INT-011"]
    if len(matching) != 1:
        failures.append("task registry must contain exactly one PA-INT-011")
    elif matching[0].get("observer") != "scripts/observe_judgment_architecture_source_locator.py":
        failures.append("PA-INT-011 observer mismatch")

    claim = status.get("claim_state", {})
    for key in ["session_implementation_claim", "session_validation_claim", "session_integration_claim"]:
        if claim.get(key) != "RELEASED":
            failures.append(f"{key} must be RELEASED")
    if claim.get("machine_claim") != "ACTIVE":
        failures.append("machine claim must remain ACTIVE")
    if claim.get("duplicate_execution_permitted") is not False:
        failures.append("duplicate execution must remain prohibited")

    loss = status.get("loss_test", {})
    if loss.get("unique_chat_only_requirements_remaining") != 0:
        failures.append("unique chat-only requirements remain")
    if loss.get("session_specific_claims_remaining") != 0:
        failures.append("session-specific claims remain")
    if loss.get("future_execution_requires_chat") is not False:
        failures.append("future execution must not require chat")
    if loss.get("deleting_conversation_impairs_continuation") is not False:
        failures.append("loss test does not support archive")

    boundary = status.get("authority_boundary", {})
    for key in [
        "social_post_is_framework_source",
        "source_observation_grants_endorsement",
        "session_consolidation_grants_execution_authority",
        "archive_disposition_completes_machine_task",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"authority boundary must be false: {key}")

    for text in [
        "MERGED_INTO_CANONICAL_WORKSTREAM",
        "PA-INT-011",
        "session_specific_claims_remaining: 0",
        "unique_chat_only_requirements_remaining: 0",
    ]:
        if text not in doc:
            failures.append(f"consolidation document missing {text!r}")

    if failures:
        print("JUDGMENT ARCHITECTURE SESSION CONSOLIDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("JUDGMENT ARCHITECTURE SESSION CONSOLIDATION: PASS")
    print("archive_disposition=ARCHIVE canonical_task=PA-INT-011 machine_claim=ACTIVE session_claims=RELEASED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
