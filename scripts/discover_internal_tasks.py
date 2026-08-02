#!/usr/bin/env python3
"""Discover internal repository work without converting evidence gaps into external tasks."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/internal-task-discovery.json"
REGISTRY = ROOT / "static/status/internal-task-registry.json"

CHECKS = [
    {
        "task_id": "DISC-TA14-PUBLICATION",
        "title": "Complete TA-14 determination publication",
        "owner_record": "docs/external-frameworks/TA14_PUBLICATION_ACTIVATION_COORDINATION.md",
        "work_locations": [
            "docs/external-frameworks/ta-14-testing-support-determination-2026-08-01.md",
            "scripts/observe_ta14_determination_publication.py",
            "reports/ta14-determination-publication-observation.json",
            ".github/workflows/validate-chain-continuation.yml",
        ],
        "completion_path": "reports/ta14-determination-publication-observation.json",
        "completion_field": "public_state",
        "completion_value": "PASS_PUBLIC_CONTENT_VERIFIED",
        "priority": "HIGH",
    },
    {
        "task_id": "DISC-TASK-MESH",
        "title": "Execute and validate the public-anchor task mesh",
        "owner_record": "docs/WIKI_PUBLIC_ANCHOR_TASK_MESH_HANDOFF.md",
        "work_locations": [
            "scripts/run_wiki_public_anchor_task_mesh.py",
            "scripts/check_wiki_public_anchor_task_mesh.py",
            "reports/wiki-public-anchor-task-mesh-execution.json",
        ],
        "completion_path": "reports/wiki-public-anchor-task-mesh-execution.json",
        "completion_field": "overall_state",
        "completion_value": "PASS_INTERNAL",
        "priority": "HIGH",
    },
]


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def main() -> int:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    tasks = []
    for spec in CHECKS:
        completion_path = ROOT / spec["completion_path"]
        observed = read_json(completion_path)
        complete = observed.get(spec["completion_field"]) == spec["completion_value"]
        missing_locations = [p for p in spec["work_locations"] if not (ROOT / p).exists()]
        tasks.append({
            **spec,
            "state": "COMPLETE_INTERNAL" if complete else "READY_INTERNAL",
            "missing_locations": missing_locations,
            "blocking": False,
            "external_task": False,
            "last_observed": now,
            "completion_predicate": f"{spec['completion_path']} contains {spec['completion_field']}={spec['completion_value']}",
            "fallback": "record the exact unresolved state and continue unrelated READY_INTERNAL tasks",
        })

    payload = {
        "schema_version": "internal-task-discovery.v1",
        "generated_at": now,
        "state": "ACTIVE_INTERNAL_DISCOVERY",
        "external_tasks_exist": False,
        "policy": {
            "missing_evidence_is_external_task": False,
            "discovered_failure_blocks_unrelated_work": False,
            "every_task_requires_locations": True,
            "every_task_requires_completion_predicate": True,
        },
        "tasks": tasks,
        "summary": {
            "total": len(tasks),
            "ready": sum(t["state"] == "READY_INTERNAL" for t in tasks),
            "complete": sum(t["state"] == "COMPLETE_INTERNAL" for t in tasks),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"INTERNAL TASK DISCOVERY: PASS - {payload['summary']['ready']} ready task(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
