#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "reports" / "external-frameworks" / "implementation-automation-readiness.json"
PLANS = ROOT / "reports" / "external-frameworks" / "implementation-execution-plans.json"
EXPECTED = ["cedar-policy", "mcp", "a2a", "guardrails-ai", "llama-guard", "neMo-guardrails"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    for path in [READINESS, PLANS]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK EXECUTION PLANS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    plans = json.loads(PLANS.read_text(encoding="utf-8"))

    if plans.get("artifact_type") != "external_framework_execution_plan_matrix":
        failures.append("artifact_type mismatch")
    if plans.get("source_readiness", {}).get("sha256") != sha256(READINESS):
        failures.append("readiness hash mismatch")

    plan_items = plans.get("plans", [])
    ids = [item.get("framework_id") for item in plan_items]
    if ids != EXPECTED:
        failures.append(f"framework order mismatch: {ids}")

    readiness_by_id = {item.get("framework_id"): item for item in readiness.get("frameworks", [])}
    for item in plan_items:
        framework_id = item.get("framework_id")
        ready = readiness_by_id.get(framework_id, {})
        allowed = ready.get("execution_job_allowed") is True
        if item.get("job_materialization_allowed") is not allowed:
            failures.append(f"job materialization mismatch: {framework_id}")
        if item.get("runtime_execution_requested") is not False:
            failures.append(f"runtime execution must remain false: {framework_id}")
        if item.get("proposed_job") is not None:
            failures.append(f"proposed_job must remain null before governed materialization: {framework_id}")
        if allowed:
            if item.get("plan_state") != "eligible_for_execution_job_materialization":
                failures.append(f"eligible plan state mismatch: {framework_id}")
            if item.get("blockers"):
                failures.append(f"eligible plan retains blockers: {framework_id}")
        else:
            if item.get("plan_state") != "blocked_no_execution_plan":
                failures.append(f"blocked plan state mismatch: {framework_id}")
            if not item.get("blockers"):
                failures.append(f"blocked plan missing blockers: {framework_id}")
            if item.get("job_materialization_allowed") is not False:
                failures.append(f"blocked plan allows job materialization: {framework_id}")

    summary = plans.get("summary", {})
    if summary.get("runtime_jobs_emitted") != 0:
        failures.append("runtime_jobs_emitted must be zero")
    if summary.get("runtime_execution_requested") is not False:
        failures.append("runtime_execution_requested must be false")

    boundary = plans.get("authority_boundary", {})
    required_false = [
        "execution_plan_is_execution_authority",
        "eligible_plan_may_execute_automatically",
        "plan_generation_may_cause_external_consequence",
        "blocked_plan_may_emit_runtime_job",
    ]
    for key in required_false:
        if boundary.get(key) is not False:
            failures.append(f"authority_boundary.{key} must be false")
    if boundary.get("job_materialization_requires_separate_governed_transition") is not True:
        failures.append("separate governed transition must be required")

    print("EXTERNAL FRAMEWORK EXECUTION PLANS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
