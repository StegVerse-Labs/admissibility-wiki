#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_wiki_public_anchor_completion_cycles.py"
REPORT = ROOT / "reports" / "wiki-public-anchor-completion-cycle.json"


def main() -> int:
    failures: list[str] = []
    if not RUNNER.exists():
        failures.append(f"missing {RUNNER.relative_to(ROOT)}")
    else:
        result = subprocess.run(
            [sys.executable, str(RUNNER)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        print(result.stdout.rstrip())
        if result.returncode != 0:
            failures.append("completion-cycle runner structural failure")

    if not REPORT.exists():
        failures.append(f"missing {REPORT.relative_to(ROOT)}")
        report = {}
    else:
        try:
            report = json.loads(REPORT.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid completion-cycle report: {exc}")
            report = {}

    if report:
        if report.get("schema_version") != "wiki-public-anchor-completion-cycle.v1":
            failures.append("completion-cycle schema mismatch")
        if report.get("external_tasks_exist") is not False:
            failures.append("external_tasks_exist must be false")
        if report.get("development_halted") is not False:
            failures.append("development_halted must be false")
        if not isinstance(report.get("cycles_executed"), int) or report.get("cycles_executed", 0) < 1:
            failures.append("at least one completion cycle must execute")
        if report.get("stop_reason") not in {
            "ALL_REGISTERED_QUEUES_PASS",
            "INTERNAL_FIXED_POINT_REACHED",
            "MAX_CYCLES_REACHED",
        }:
            failures.append("invalid completion-cycle stop reason")
        policy = report.get("policy", {})
        for key in (
            "continue_after_queue_failure",
            "bounded_retry_prevents_infinite_wait",
            "fixed_point_is_not_completion",
            "missing_evidence_is_non_blocking",
            "unresolved_work_requires_exact_repository_locations",
        ):
            if policy.get(key) is not True:
                failures.append(f"policy {key} must be true")
        for item in report.get("remaining_internal_work", []):
            if not isinstance(item, dict):
                failures.append("remaining_internal_work entries must be objects")
                continue
            for key in ("queue_id", "runner", "registry", "report", "validator"):
                if not item.get(key):
                    failures.append(f"remaining work missing {key}")
        boundary = report.get("authority_boundary", {})
        for key in (
            "completion_cycle_pass_is_external_validation",
            "completion_cycle_grants_certification",
            "completion_cycle_grants_execution_authority",
        ):
            if boundary.get(key) is not False:
                failures.append(f"authority boundary {key} must be false")

    if failures:
        print("WIKI PUBLIC-ANCHOR COMPLETION CYCLES CHECK: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("WIKI PUBLIC-ANCHOR COMPLETION CYCLES CHECK: PASS - bounded progress, fixed-point detection, and exact unresolved locations preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
