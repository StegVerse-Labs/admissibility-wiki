#!/usr/bin/env python3
"""Run all known Wiki public-anchor task queues without global stalling."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "wiki-public-anchor-task-mesh-execution.json"

QUEUES = (
    {
        "queue_id": "public-anchor-internal",
        "runner": "scripts/run_wiki_public_anchor_internal_tasks.py",
        "registry": "static/status/wiki-public-anchor-internal-task-registry.json",
        "report": "reports/wiki-public-anchor-internal-task-execution.json",
    },
    {
        "queue_id": "ta14-gap-review-v2",
        "runner": "scripts/run_ta14_stegverse_gap_review_v2_tasks.py",
        "registry": "static/data/governed-framework-reviews/ta-14.stegverse-gap-review-v2.task-registry.json",
        "report": "static/status/ta-14-stegverse-gap-review-v2.execution-status.json",
    },
)


def main() -> int:
    results = []
    structural_failures = []
    for queue in QUEUES:
        runner = ROOT / queue["runner"]
        registry = ROOT / queue["registry"]
        if not runner.exists() or not registry.exists():
            missing = [str(path.relative_to(ROOT)) for path in (runner, registry) if not path.exists()]
            results.append({**queue, "state": "BLOCKED_MISSING_QUEUE_ARTIFACT", "missing": missing})
            structural_failures.extend(missing)
            continue
        result = subprocess.run(
            [sys.executable, str(runner)], cwd=ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        report_exists = (ROOT / queue["report"]).exists()
        results.append({
            **queue,
            "state": "PASS_INTERNAL" if result.returncode == 0 else "FAIL_INTERNAL_CONTINUABLE",
            "exit_code": result.returncode,
            "report_exists": report_exists,
            "output": result.stdout[-12000:],
        })

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "wiki-public-anchor-task-mesh-execution.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_policy": {
            "external_tasks_exist": False,
            "continue_after_queue_failure": True,
            "failed_queue_blocks_unrelated_queue": False,
            "evidence_gap_halts_development": False,
        },
        "queues": results,
        "summary": {
            "total": len(results),
            "pass": sum(item["state"] == "PASS_INTERNAL" for item in results),
            "fail_continuable": sum(item["state"] == "FAIL_INTERNAL_CONTINUABLE" for item in results),
            "blocked_structural": sum(item["state"] == "BLOCKED_MISSING_QUEUE_ARTIFACT" for item in results),
        },
        "authority_boundary": {
            "task_mesh_pass_is_external_validation": False,
            "task_mesh_pass_grants_certification": False,
            "task_mesh_pass_grants_execution_authority": False,
        },
    }
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for item in results:
        print(f"{item['queue_id']}: {item['state']} ({item['runner']})")
    if structural_failures:
        print("WIKI PUBLIC-ANCHOR TASK MESH: FAIL - missing queue artifacts")
        return 1
    print(f"WIKI PUBLIC-ANCHOR TASK MESH: PASS - report written to {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
