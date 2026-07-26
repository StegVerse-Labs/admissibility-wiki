#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "admissibility-orchestration-state.json"


def fail(message: str) -> None:
    raise SystemExit(f"ADMISSIBILITY ORCHESTRATION STATE: FAIL: {message}")


def main() -> int:
    if not STATE.exists():
        fail("missing data/admissibility-orchestration-state.json")
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0.0":
        fail("unsupported schema_version")
    if payload.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if payload.get("heartbeat_mode") != "TRANSITION_DRIVEN":
        fail("heartbeat must be transition-driven")
    if payload.get("time_role") != "WATCHDOG_ONLY":
        fail("time role must remain watchdog-only")
    authority = payload.get("authority")
    if not isinstance(authority, dict) or any(authority.values()):
        fail("orchestration state must not grant authority")
    queued = payload.get("queued_parallel_safe_tasks")
    if not isinstance(queued, list):
        fail("queued_parallel_safe_tasks must be a list")
    for task in queued:
        if task.get("execution_class") != "PARALLEL_SAFE":
            fail("queued task is not PARALLEL_SAFE")
        if task.get("state") not in {"QUEUED", "QUEUED_DEPENDENCY_BLOCKED"}:
            fail("queued task has invalid state")
    print("ADMISSIBILITY ORCHESTRATION STATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
