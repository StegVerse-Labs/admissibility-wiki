#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_external_framework_automation_readiness.py"
OUTPUT = ROOT / "reports" / "external-frameworks" / "implementation-automation-readiness.json"
PLANS = ROOT / "reports" / "external-frameworks" / "implementation-execution-plans.json"
EXPECTED = ["cedar-policy", "mcp", "a2a", "guardrails-ai", "llama-guard", "neMo-guardrails"]


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("automation readiness output must be a JSON object")
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

    payload: dict[str, Any] = {}
    if not OUTPUT.exists():
        failures.append(f"missing output: {OUTPUT.relative_to(ROOT)}")
    else:
        try:
            payload = load(OUTPUT)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failures.append(str(exc))

    if not PLANS.exists():
        failures.append(f"chained execution plan output missing: {PLANS.relative_to(ROOT)}")

    if payload:
        if payload.get("artifact_type") != "external_framework_automation_readiness_matrix":
            failures.append("artifact_type mismatch")
        frameworks = payload.get("frameworks", [])
        ids = [item.get("framework_id") for item in frameworks if isinstance(item, dict)]
        if ids != EXPECTED:
            failures.append(f"framework order mismatch: {ids}")

        for item in frameworks:
            if not isinstance(item, dict):
                failures.append("framework entry must be an object")
                continue
            framework_id = item.get("framework_id")
            if item.get("selection_state") == "selection_required":
                if item.get("execution_job_allowed") is not False:
                    failures.append(f"{framework_id}: selection_required must block execution job")
                if item.get("automation_state") != "blocked_selection_required":
                    failures.append(f"{framework_id}: blocked state mismatch")
            if item.get("execution_job_allowed") is True:
                required_true = [
                    "framework_specific_context_complete",
                    "hash_evidence_present",
                    "version_evidence_present",
                    "command_evidence_present",
                    "selection_complete",
                    "execution_authorized_in_registry",
                ]
                for key in required_true:
                    if item.get(key) is not True:
                        failures.append(f"{framework_id}: execution allowed without {key}")

        summary = payload.get("summary", {})
        allowed_count = sum(1 for item in frameworks if isinstance(item, dict) and item.get("execution_job_allowed") is True)
        if summary.get("ready_for_execution_job_review") != allowed_count:
            failures.append("summary ready count mismatch")
        if summary.get("execution_jobs_may_be_added") is not (allowed_count > 0):
            failures.append("summary execution_jobs_may_be_added mismatch")
        if summary.get("execution_plan_generation_chained") is not True:
            failures.append("execution plan generation must be chained")

        boundary = payload.get("authority_boundary", {})
        for key in [
            "automation_readiness_is_execution_authority",
            "selection_completion_is_certification",
            "selection_completion_is_compatibility",
            "selection_completion_creates_standing",
            "readiness_matrix_may_cause_external_consequence",
        ]:
            if boundary.get(key) is not False:
                failures.append(f"authority_boundary.{key} must be false")

    print("EXTERNAL FRAMEWORK AUTOMATION READINESS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
