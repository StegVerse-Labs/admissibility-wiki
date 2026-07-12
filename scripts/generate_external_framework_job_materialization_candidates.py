#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "reports" / "external-frameworks" / "implementation-automation-readiness.json"
PLANS = ROOT / "reports" / "external-frameworks" / "implementation-execution-plans.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "job-materialization-candidates.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected object: {path}")
    return payload


def main() -> int:
    for path in [READINESS, PLANS]:
        if not path.exists():
            raise SystemExit(f"missing source artifact: {path.relative_to(ROOT)}")

    readiness = load(READINESS)
    plans = load(PLANS)
    readiness_by_id = {
        item.get("framework_id"): item
        for item in readiness.get("frameworks", [])
        if isinstance(item, dict)
    }

    candidates: list[dict[str, Any]] = []
    awaiting_review = 0
    for plan in plans.get("plans", []):
        if not isinstance(plan, dict):
            continue
        framework_id = plan.get("framework_id")
        ready = readiness_by_id.get(framework_id, {})
        eligible = (
            plan.get("plan_state") == "eligible_for_execution_job_materialization"
            and plan.get("job_materialization_allowed") is True
            and ready.get("execution_job_allowed") is True
        )
        if eligible:
            awaiting_review += 1
        candidates.append(
            {
                "artifact_type": "external_framework_job_materialization_candidate",
                "schema_version": "0.1",
                "framework_id": framework_id,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "candidate_state": (
                    "awaiting_authority_and_consequence_review"
                    if eligible
                    else "blocked_plan_ineligible"
                ),
                "source_readiness_sha256": sha256(READINESS),
                "source_execution_plan_sha256": sha256(PLANS),
                "source_plan_state": plan.get("plan_state"),
                "source_execution_job_allowed": ready.get("execution_job_allowed") is True,
                "blockers": list(plan.get("blockers", [])),
                "runtime_job_materialized": False,
                "runtime_execution_requested": False,
                "materialized_job": None,
                "authority_review": {
                    "state": "not_performed",
                    "reviewer_identity": None,
                    "delegation_reference": None,
                    "validity_window": None,
                },
                "consequence_boundary_review": {
                    "state": "not_performed",
                    "target": None,
                    "scope": None,
                    "recoverability_profile": None,
                    "rollback_or_stop_condition": None,
                },
                "required_next_transition": (
                    "attach_authority_and_consequence_boundary_review"
                    if eligible
                    else "satisfy_implementation_selection_and_execution_plan_gates"
                ),
                "authority_boundary": {
                    "candidate_is_executable_job": False,
                    "candidate_is_execution_authority": False,
                    "candidate_may_cause_external_consequence": False,
                    "review_completion_materializes_job": False,
                },
            }
        )

    result = {
        "artifact_type": "external_framework_job_materialization_candidate_matrix",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "github_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "sha": os.environ.get("GITHUB_SHA"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
        },
        "source_readiness": {
            "path": str(READINESS.relative_to(ROOT)),
            "sha256": sha256(READINESS),
        },
        "source_execution_plans": {
            "path": str(PLANS.relative_to(ROOT)),
            "sha256": sha256(PLANS),
        },
        "summary": {
            "framework_count": len(candidates),
            "awaiting_authority_and_consequence_review": awaiting_review,
            "blocked_plan_ineligible": len(candidates) - awaiting_review,
            "runtime_jobs_materialized": 0,
            "runtime_execution_requested": False,
        },
        "candidates": candidates,
        "authority_boundary": {
            "candidate_generation_is_job_materialization": False,
            "candidate_generation_is_execution_authority": False,
            "candidate_generation_may_cause_external_consequence": False,
            "separate_governed_materialization_transition_required": True,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        "JOB MATERIALIZATION CANDIDATES: "
        f"{awaiting_review}/{len(candidates)} awaiting review; "
        f"0 jobs materialized -> {OUTPUT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
