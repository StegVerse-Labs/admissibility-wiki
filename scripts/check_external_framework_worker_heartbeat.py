#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "worker-task-registry.json"
ALLOWED = {"CLAIMED", "ACTIVE", "BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED", "COMPLETE", "SUPERSEDED", "MERGED"}
TERMINAL = {"COMPLETE", "SUPERSEDED", "MERGED"}


def parse_utc(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", default="reports/external-frameworks/worker-heartbeat.json")
    args = parser.parse_args()

    failures: list[str] = []
    if not REGISTRY.exists():
        print("EXTERNAL FRAMEWORK WORKER HEARTBEAT: FAIL")
        print(f"- missing registry: {REGISTRY.relative_to(ROOT)}")
        return 1

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    now = dt.datetime.now(dt.timezone.utc)

    if registry.get("artifact_type") != "stegverse_worker_task_registry":
        failures.append("registry artifact_type mismatch")
    if registry.get("goal_id") != "EXT-FRAMEWORK-SECOND-PAGE-36":
        failures.append("registry goal_id mismatch")
    if registry.get("repository") != "StegVerse-Labs/admissibility-wiki":
        failures.append("registry repository mismatch")

    ttl = int(registry.get("claim_ttl_minutes", 0))
    if ttl <= 0:
        failures.append("claim_ttl_minutes must be positive")

    workers = registry.get("workers")
    if not isinstance(workers, list) or not workers:
        failures.append("workers must be a non-empty list")
        workers = []

    seen_worker_ids: set[str] = set()
    framework_owner: dict[str, str] = {}
    worker_receipts: list[dict[str, object]] = []

    for worker in workers:
        wid = worker.get("worker_id")
        state = worker.get("state")
        issue = worker.get("issue")
        created = worker.get("claim_created_at_utc")
        assigned = worker.get("assigned_frameworks", [])

        if not isinstance(wid, str) or not wid:
            failures.append("worker missing worker_id")
            continue
        if wid in seen_worker_ids:
            failures.append(f"duplicate worker_id: {wid}")
        seen_worker_ids.add(wid)
        if state not in ALLOWED:
            failures.append(f"{wid}: invalid state {state!r}")
        if not isinstance(issue, int):
            failures.append(f"{wid}: issue must be integer")
        if not worker.get("next_executable_action"):
            failures.append(f"{wid}: missing next_executable_action")
        if not worker.get("release_condition"):
            failures.append(f"{wid}: missing release_condition")
        if not worker.get("collision_boundary"):
            failures.append(f"{wid}: missing collision_boundary")

        age_minutes = None
        stale = False
        if not isinstance(created, str):
            failures.append(f"{wid}: missing claim_created_at_utc")
        else:
            try:
                age_minutes = (now - parse_utc(created)).total_seconds() / 60.0
                stale = state not in TERMINAL and age_minutes > ttl
            except Exception as exc:
                failures.append(f"{wid}: invalid claim_created_at_utc: {exc}")

        if stale:
            failures.append(f"{wid}: stale claim age {age_minutes:.1f}m exceeds TTL {ttl}m; renew with evidence or mark BLOCKED with release condition")

        if not isinstance(assigned, list) or not assigned:
            failures.append(f"{wid}: assigned_frameworks must be non-empty list")
            assigned = []
        for framework in assigned:
            if not isinstance(framework, str) or not framework:
                failures.append(f"{wid}: invalid framework assignment")
                continue
            prior = framework_owner.get(framework)
            if prior and prior != wid:
                failures.append(f"framework collision: {framework} owned by {prior} and {wid}")
            framework_owner[framework] = wid

        worker_receipts.append({
            "worker_id": wid,
            "issue": issue,
            "state": state,
            "claim_age_minutes": round(age_minutes, 2) if isinstance(age_minutes, float) else None,
            "stale": stale,
            "assigned_framework_count": len(assigned),
            "next_executable_action": worker.get("next_executable_action"),
            "release_condition": worker.get("release_condition"),
        })

    receipt = {
        "artifact_type": "stegverse_worker_heartbeat_receipt",
        "schema_version": "1.0",
        "goal_id": registry.get("goal_id"),
        "repository": registry.get("repository"),
        "observed_at_utc": now.isoformat().replace("+00:00", "Z"),
        "heartbeat_interval_minutes": registry.get("heartbeat_interval_minutes"),
        "claim_ttl_minutes": ttl,
        "worker_count": len(workers),
        "framework_assignments_observed": len(framework_owner),
        "status": "FAILED" if failures else "ACTIVE",
        "failures": failures,
        "workers": worker_receipts,
        "next_executable_task": next((w.get("next_executable_action") for w in workers if w.get("state") == "ACTIVE"), None),
    }

    output = ROOT / args.receipt
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    print("EXTERNAL FRAMEWORK WORKER HEARTBEAT:", "FAIL" if failures else "ACTIVE")
    print(f"workers={len(workers)} framework_assignments={len(framework_owner)} receipt={output.relative_to(ROOT)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
