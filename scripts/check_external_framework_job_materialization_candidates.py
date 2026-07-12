#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_external_framework_job_materialization_candidates.py"
READINESS = ROOT / "reports" / "external-frameworks" / "implementation-automation-readiness.json"
PLANS = ROOT / "reports" / "external-frameworks" / "implementation-execution-plans.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "job-materialization-candidates.json"
EXPECTED = ["cedar-policy", "mcp", "a2a", "guardrails-ai", "llama-guard", "neMo-guardrails"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        failures.append(f"missing generator: {GENERATOR.relative_to(ROOT)}")
    else:
        completed = subprocess.run(
            [sys.executable, str(GENERATOR)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.returncode != 0:
            failures.append(f"generator returned {completed.returncode}")

    for path in [READINESS, PLANS, OUTPUT]:
        if not path.exists():
            failures.append(f"missing artifact: {path.relative_to(ROOT)}")

    payload: dict[str, Any] = {}
    plans: dict[str, Any] = {}
    if not failures:
        try:
            payload = load(OUTPUT)
            plans = load(PLANS)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failures.append(str(exc))

    if payload:
        if payload.get("artifact_type") != "external_framework_job_materialization_candidate_matrix":
            failures.append("artifact_type mismatch")
        candidates = payload.get("candidates", [])
        ids = [item.get("framework_id") for item in candidates if isinstance(item, dict)]
        if ids != EXPECTED:
            failures.append(f"framework order mismatch: {ids}")
        if payload.get("source_readiness", {}).get("sha256") != sha256(READINESS):
            failures.append("source readiness hash mismatch")
        if payload.get("source_execution_plans", {}).get("sha256") != sha256(PLANS):
            failures.append("source execution plan hash mismatch")

        plan_by_id = {
            item.get("framework_id"): item
            for item in plans.get("plans", [])
            if isinstance(item, dict)
        }
        awaiting = 0
        for item in candidates:
            if not isinstance(item, dict):
                failures.append("candidate entry must be object")
                continue
            framework_id = item.get("framework_id")
            plan = plan_by_id.get(framework_id, {})
            eligible = plan.get("plan_state") == "eligible_for_execution_job_materialization"
            expected_state = (
                "awaiting_authority_and_consequence_review"
                if eligible
                else "blocked_plan_ineligible"
            )
            if item.get("candidate_state") != expected_state:
                failures.append(f"{framework_id}: candidate_state mismatch")
            if expected_state == "awaiting_authority_and_consequence_review":
                awaiting += 1
            if item.get("runtime_job_materialized") is not False:
                failures.append(f"{framework_id}: runtime job must remain unmaterialized")
            if item.get("runtime_execution_requested") is not False:
                failures.append(f"{framework_id}: runtime execution must remain false")
            if item.get("materialized_job") is not None:
                failures.append(f"{framework_id}: materialized_job must be null")
            if item.get("source_readiness_sha256") != sha256(READINESS):
                failures.append(f"{framework_id}: readiness hash mismatch")
            if item.get("source_execution_plan_sha256") != sha256(PLANS):
                failures.append(f"{framework_id}: plan hash mismatch")
            if item.get("authority_review", {}).get("state") != "not_performed":
                failures.append(f"{framework_id}: authority review unexpectedly performed")
            if item.get("consequence_boundary_review", {}).get("state") != "not_performed":
                failures.append(f"{framework_id}: consequence review unexpectedly performed")
            for key in [
                "candidate_is_executable_job",
                "candidate_is_execution_authority",
                "candidate_may_cause_external_consequence",
                "review_completion_materializes_job",
            ]:
                if item.get("authority_boundary", {}).get(key) is not False:
                    failures.append(f"{framework_id}: authority_boundary.{key} must be false")

        summary = payload.get("summary", {})
        if summary.get("awaiting_authority_and_consequence_review") != awaiting:
            failures.append("summary awaiting review count mismatch")
        if summary.get("runtime_jobs_materialized") != 0:
            failures.append("runtime_jobs_materialized must be zero")
        if summary.get("runtime_execution_requested") is not False:
            failures.append("summary runtime_execution_requested must be false")
        boundary = payload.get("authority_boundary", {})
        if boundary.get("separate_governed_materialization_transition_required") is not True:
            failures.append("separate governed materialization transition must be required")
        for key in [
            "candidate_generation_is_job_materialization",
            "candidate_generation_is_execution_authority",
            "candidate_generation_may_cause_external_consequence",
        ]:
            if boundary.get(key) is not False:
                failures.append(f"authority_boundary.{key} must be false")

    print("JOB MATERIALIZATION CANDIDATES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
