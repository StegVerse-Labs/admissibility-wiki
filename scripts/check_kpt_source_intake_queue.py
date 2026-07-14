#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "static" / "status" / "kpt-source-intake-queue.json"
STATUS = ROOT / "static" / "status" / "kpt-external-framework-intake-status.json"
MANIFEST = ROOT / "docs" / "external-frameworks" / "kpt.json"
REPORT = ROOT / "docs" / "external-frameworks" / "reports" / "kpt.compatibility.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for path in [QUEUE, STATUS, MANIFEST, REPORT]:
        if not path.exists():
            failures.append(f"missing required artifact: {path.relative_to(ROOT)}")

    if failures:
        print("KPT SOURCE INTAKE QUEUE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    queue = load_json(QUEUE)
    status = load_json(STATUS)
    manifest = load_json(MANIFEST)
    report = load_json(REPORT)

    if queue.get("framework_id") != "kpt":
        failures.append("queue framework_id must be kpt")
    if queue.get("state") != "WAITING_FOR_CANONICAL_OWNER_PUBLISHED_SOURCE":
        failures.append("queue state mismatch")
    if queue.get("current_source_posture") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("queue must preserve SOURCE_BLOCKED_FAIL_CLOSED")
    if queue.get("manual_task_requirement") != "none":
        failures.append("queue must not assign manual work")
    for key in ["user_action_required", "manual_source_search_required", "downstream_mutation_authorized"]:
        if queue.get(key) is not False:
            failures.append(f"queue must set {key}=false")
    if not isinstance(queue.get("queue"), list):
        failures.append("queue field must be an array")

    boundaries = queue.get("boundary", {})
    for key in [
        "queue_entry_is_source_sufficiency",
        "source_discovery_is_endorsement",
        "source_promotion_is_certification",
        "source_promotion_is_execution_authority",
        "source_promotion_is_commit_time_authority",
    ]:
        if boundaries.get(key) is not False:
            failures.append(f"boundary must set {key}=false")
    if boundaries.get("missing_or_ambiguous_source_fails_closed") is not True:
        failures.append("queue must fail closed on missing or ambiguous source")

    if status.get("source_posture") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("status source posture mismatch")
    if manifest.get("source_version") != "UNVERIFIED_SOURCE_REQUIRED":
        failures.append("manifest source version must remain unverified")
    if report.get("result") != "SOURCE_BLOCKED_FAIL_CLOSED":
        failures.append("compatibility report must remain source blocked")

    print("KPT SOURCE INTAKE QUEUE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
