#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "reports" / "external-frameworks" / "implementation-automation-readiness.json"
OUTPUT = ROOT / "reports" / "external-frameworks" / "implementation-execution-plans.json"
CANDIDATE_GENERATOR = ROOT / "scripts" / "generate_external_framework_job_materialization_candidates.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not READINESS.exists():
        raise SystemExit(f"missing readiness matrix: {READINESS.relative_to(ROOT)}")

    readiness: dict[str, Any] = json.loads(READINESS.read_text(encoding="utf-8"))
    plans: list[dict[str, Any]] = []
    eligible = 0

    for item in readiness.get("frameworks", []):
        allowed = item.get("execution_job_allowed") is True
        if allowed:
            eligible += 1
        blockers = []
        if item.get("selection_state") != "implementation_selected_hash_bound":
            blockers.append("selection_state_not_hash_bound")
        if item.get("missing_required_fields"):
            blockers.append("required_fields_missing")
        if item.get("framework_specific_context_complete") is not True:
            blockers.append("framework_specific_context_incomplete")
        if item.get("hash_evidence_present") is not True:
            blockers.append("hash_evidence_missing")
        if item.get("version_evidence_present") is not True:
            blockers.append("version_or_commit_evidence_missing")
        if item.get("command_evidence_present") is not True:
            blockers.append("command_evidence_missing")
        if item.get("execution_authorized_in_registry") is not True:
            blockers.append("registry_execution_authorization_false")
        if allowed and blockers:
            raise SystemExit(f"unsafe readiness contradiction for {item.get('framework_id')}: {blockers}")

        plans.append(
            {
                "framework_id": item.get("framework_id"),
                "plan_state": "eligible_for_execution_job_materialization" if allowed else "blocked_no_execution_plan",
                "job_materialization_allowed": allowed,
                "runtime_execution_requested": False,
                "blockers": blockers,
                "proposed_job": None,
                "required_next_transition": (
                    "human_or_governed_review_of_hash_bound_selection_before_job_materialization"
                    if allowed
                    else "complete_and_validate_implementation_selection"
                ),
            }
        )

    result = {
        "artifact_type": "external_framework_execution_plan_matrix",
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_readiness": {
            "path": str(READINESS.relative_to(ROOT)),
            "sha256": sha256(READINESS),
        },
        "github_context": {
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "sha": os.environ.get("GITHUB_SHA"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
        },
        "summary": {
            "framework_count": len(plans),
            "eligible_for_execution_job_materialization": eligible,
            "blocked_no_execution_plan": len(plans) - eligible,
            "runtime_jobs_emitted": 0,
            "runtime_execution_requested": False,
        },
        "plans": plans,
        "authority_boundary": {
            "execution_plan_is_execution_authority": False,
            "eligible_plan_may_execute_automatically": False,
            "plan_generation_may_cause_external_consequence": False,
            "blocked_plan_may_emit_runtime_job": False,
            "job_materialization_requires_separate_governed_transition": True,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        "EXTERNAL FRAMEWORK EXECUTION PLANS: "
        f"{eligible}/{len(plans)} eligible; {len(plans) - eligible} blocked; "
        f"0 runtime jobs emitted -> {OUTPUT.relative_to(ROOT)}"
    )

    completed = subprocess.run(
        [sys.executable, str(CANDIDATE_GENERATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
