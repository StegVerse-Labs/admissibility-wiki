#!/usr/bin/env python3
"""Advance the public-anchor task mesh to a bounded internal fixed point.

The controller repeatedly runs the registry-driven task mesh, snapshots queue reports,
and stops when all queues pass, no further repository-derived state changes are observed,
or the bounded cycle limit is reached. It never waits for external actors and never
converts missing evidence into a global development halt.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MESH_RUNNER = ROOT / "scripts" / "run_wiki_public_anchor_task_mesh.py"
MESH_REPORT = ROOT / "reports" / "wiki-public-anchor-task-mesh-execution.json"
COMPLETION_REPORT = ROOT / "reports" / "wiki-public-anchor-completion-cycle.json"
MAX_CYCLES = 3


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def unresolved_locations(report: dict[str, Any]) -> list[dict[str, Any]]:
    unresolved: list[dict[str, Any]] = []
    for queue in report.get("queues", []):
        if not isinstance(queue, dict) or queue.get("state") == "PASS_INTERNAL":
            continue
        unresolved.append({
            "queue_id": queue.get("queue_id"),
            "state": queue.get("state"),
            "runner": queue.get("runner"),
            "registry": queue.get("registry"),
            "report": queue.get("report"),
            "validator": queue.get("validator"),
            "output_tail": str(queue.get("output", ""))[-4000:],
        })
    return unresolved


def main() -> int:
    structural_failures: list[str] = []
    cycles: list[dict[str, Any]] = []
    prior_fingerprint: str | None = None
    stop_reason = "MAX_CYCLES_REACHED"

    if not MESH_RUNNER.exists():
        print(f"PUBLIC-ANCHOR COMPLETION CYCLES: FAIL - missing {MESH_RUNNER.relative_to(ROOT)}")
        return 1

    for cycle_number in range(1, MAX_CYCLES + 1):
        before = sha256(MESH_REPORT)
        result = subprocess.run(
            [sys.executable, str(MESH_RUNNER)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if not MESH_REPORT.exists():
            structural_failures.append(f"cycle {cycle_number}: missing {MESH_REPORT.relative_to(ROOT)}")
            break

        try:
            report = load_json(MESH_REPORT)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            structural_failures.append(f"cycle {cycle_number}: invalid mesh report: {exc}")
            break

        after = sha256(MESH_REPORT)
        unresolved = unresolved_locations(report)
        fingerprint_source = json.dumps(
            {
                "queues": report.get("queues", []),
                "summary": report.get("summary", {}),
            },
            sort_keys=True,
        ).encode("utf-8")
        fingerprint = hashlib.sha256(fingerprint_source).hexdigest()
        cycles.append({
            "cycle": cycle_number,
            "runner_exit_code": result.returncode,
            "mesh_report_hash_before": before,
            "mesh_report_hash_after": after,
            "state_fingerprint": fingerprint,
            "summary": report.get("summary", {}),
            "unresolved": unresolved,
            "output_tail": result.stdout[-6000:],
        })

        if not unresolved and result.returncode == 0:
            stop_reason = "ALL_REGISTERED_QUEUES_PASS"
            break
        if prior_fingerprint == fingerprint:
            stop_reason = "INTERNAL_FIXED_POINT_REACHED"
            break
        prior_fingerprint = fingerprint

    COMPLETION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "wiki-public-anchor-completion-cycle.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "controller": str(Path(__file__).relative_to(ROOT)),
        "mesh_runner": str(MESH_RUNNER.relative_to(ROOT)),
        "max_cycles": MAX_CYCLES,
        "cycles_executed": len(cycles),
        "stop_reason": stop_reason,
        "development_halted": False,
        "external_tasks_exist": False,
        "cycles": cycles,
        "remaining_internal_work": cycles[-1]["unresolved"] if cycles else [],
        "policy": {
            "continue_after_queue_failure": True,
            "bounded_retry_prevents_infinite_wait": True,
            "fixed_point_is_not_completion": True,
            "missing_evidence_is_non_blocking": True,
            "unresolved_work_requires_exact_repository_locations": True,
        },
        "authority_boundary": {
            "completion_cycle_pass_is_external_validation": False,
            "completion_cycle_grants_certification": False,
            "completion_cycle_grants_execution_authority": False,
        },
        "structural_failures": structural_failures,
    }
    COMPLETION_REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"PUBLIC-ANCHOR COMPLETION CYCLES: {stop_reason} - {len(cycles)} cycle(s)")
    print(f"report: {COMPLETION_REPORT.relative_to(ROOT)}")
    if structural_failures:
        for failure in structural_failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
