#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "external-frameworks"
MODEL_PATH = OUT / "generated-page-state-model.json"


def read_model() -> dict[str, Any]:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def write_json(name: str, data: dict[str, Any]) -> None:
    path = OUT / name
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validation_summary(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_validation_summary",
        "schema_version": "0.2",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "validated_through": "scripts/check_external_framework_page_status.py",
        "surface_inventory": "docs/external-frameworks/generated-page-surfaces.json",
        "surface_handoff": "docs/external-frameworks/GENERATED_PAGE_SURFACES_HANDOFF.md",
        "root_addendum": "docs/GENERATED_PAGE_SURFACES_ROOT_ADDENDUM.md",
        "validators_called_by_page_status": [
            "scripts/check_external_framework_page_analysis_boundary.py",
            "scripts/check_external_framework_page_candidates.py",
            "scripts/check_external_framework_page_surfaces.py",
            "scripts/check_generated_page_surfaces_handoff.py",
            "scripts/check_generated_page_surfaces_root_addendum.py",
            "scripts/check_generated_page_closeout_state_generation.py"
        ],
        "manual_tasks_removed": [
            "generated_surface_discovery",
            "generated_surface_handoff_discovery",
            "generated_surface_root_handoff_discovery",
            "generated_closeout_state_reconstruction"
        ],
        "boundary": {
            "validation_summary_is_authority": False,
            "single_workflow_policy_preserved": True,
            "manual_generated_surface_discovery_required": False
        }
    }


def progress(model: dict[str, Any]) -> dict[str, Any]:
    percent = model["repo_percent_complete"]
    return {
        "artifact_type": "generated_page_progress",
        "schema_version": "0.1",
        "repo": model["repo"],
        "org": model["org"],
        "repo_percent_complete": percent,
        "goal_activation_percent_complete": model["goal_activation_percent_complete"],
        "active_goal": model["active_goal"],
        "current_checkpoint": model["current_checkpoint"],
        "actual_vs_recorded": {
            "actual_percent": percent,
            "recorded_goal_state_percent": model["recorded_goal_state_percent"],
            "reason": model["checkpoint_reason"]
        },
        "active_surfaces": model["active_surfaces"],
        "remaining_tasks": model["remaining_tasks"],
        "boundary": {
            "progress_record_is_authority": False,
            "manual_progress_reconstruction_required": False,
            "single_workflow_policy_preserved": True
        }
    }


def release_readiness(model: dict[str, Any]) -> dict[str, Any]:
    release = model["release"]
    return {
        "artifact_type": "generated_page_release_readiness",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "release_ready": release["release_ready"],
        "readiness_percent": release["readiness_percent"],
        "required_before_tag": release["required_before_tag"],
        "already_satisfied": release["already_satisfied"],
        "boundary": {
            "release_readiness_is_authority": False,
            "tag_without_green_ci_allowed": False,
            "manual_release_readiness_reconstruction_required": False
        }
    }


def downstream_tasks(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_downstream_tasks",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "activation_condition": "after release tag and green public verification",
        "tasks": [
            {"destination": "StegVerse-Labs/Site", "task_id": "site.generated-framework-results-summary", "required_input": "docs/external-frameworks/evaluation-results.md", "status": "pending_release_tag"},
            {"destination": "GCAT-BCAT-Engine/Publisher", "task_id": "publisher.generated-framework-results-import-awareness", "required_input": "docs/external-frameworks/reports/*.compatibility.json", "status": "pending_release_tag"},
            {"destination": "stegguardian-wiki", "task_id": "guardian.execution-authority-boundary-summary", "required_input": "docs/external-frameworks/generated-page-release-readiness.json", "status": "pending_release_tag"}
        ],
        "boundary": {
            "downstream_tasks_are_authority": False,
            "manual_downstream_task_reconstruction_required": False,
            "release_tag_required_before_downstream_install": True
        }
    }


def ci_request(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_ci_evidence_request",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "requested_evidence": [
            "single canonical workflow conclusion",
            "generated page status validation conclusion",
            "generated page progress validation conclusion",
            "generated page release readiness validation conclusion",
            "generated page downstream task validation conclusion",
            "generated page tag candidate validation conclusion",
            "generated page closeout bundle validation conclusion",
            "generated page validation summary generation conclusion",
            "public GitHub Pages verification conclusion"
        ],
        "current_state": "pending_next_workflow_run",
        "release_gate": "blocked_until_green_ci_and_public_verification",
        "manual_tasks_removed": [
            "manual_ci_evidence_reconstruction",
            "manual_public_verification_reconstruction"
        ],
        "boundary": {
            "ci_request_is_authority": False,
            "missing_ci_fails_closed": True,
            "single_workflow_policy_preserved": True
        }
    }


def tag_candidate(model: dict[str, Any]) -> dict[str, Any]:
    tag = model["tag"]
    return {
        "artifact_type": "generated_page_tag_candidate",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "tag_candidate": tag["tag_candidate"],
        "tag_ready": tag["tag_ready"],
        "blocked_by": tag["blocked_by"],
        "required_artifacts": [
            "docs/external-frameworks/generated-page-progress.json",
            "docs/external-frameworks/generated-page-release-readiness.json",
            "docs/external-frameworks/generated-page-downstream-tasks.json",
            "docs/external-frameworks/generated-page-ci-evidence-request.json"
        ],
        "boundary": {
            "tag_candidate_is_authority": False,
            "tag_ready_without_green_ci_allowed": False,
            "manual_tag_readiness_reconstruction_required": False
        }
    }


def closeout_bundle(model: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_closeout_bundle",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "closeout_ready": False,
        "closeout_percent": model["repo_percent_complete"],
        "required_artifacts": [
            "docs/external-frameworks/generated-page-validation-summary.json",
            "docs/external-frameworks/generated-page-progress.json",
            "docs/external-frameworks/generated-page-release-readiness.json",
            "docs/external-frameworks/generated-page-downstream-tasks.json",
            "docs/external-frameworks/generated-page-ci-evidence-request.json",
            "docs/external-frameworks/generated-page-tag-candidate.json",
            "docs/external-frameworks/generated-page-activation-gate.json"
        ],
        "blocked_by": tag_candidate(model)["blocked_by"],
        "next_integration_goal_candidate": "post-release downstream generated-framework-results propagation",
        "boundary": {
            "closeout_bundle_is_authority": False,
            "manual_closeout_reconstruction_required": False,
            "thread_archive_ready": model["boundary"]["thread_archive_ready"]
        }
    }


def activation_gate(model: dict[str, Any]) -> dict[str, Any]:
    activation = model["activation"]
    return {
        "artifact_type": "generated_page_activation_gate",
        "schema_version": "0.1",
        "repo": model["repo"],
        "active_goal": model["active_goal"],
        "activation_ready": activation["activation_ready"],
        "activation_percent": activation["activation_percent"],
        "required_to_activate": activation["required_to_activate"],
        "fail_closed_until": activation["fail_closed_until"],
        "boundary": {
            "activation_gate_is_authority": False,
            "missing_evidence_blocks_activation": True,
            "manual_activation_reconstruction_required": False,
            "thread_archive_ready": model["boundary"]["thread_archive_ready"]
        }
    }


def main() -> int:
    model = read_model()
    write_json("generated-page-validation-summary.json", validation_summary(model))
    write_json("generated-page-progress.json", progress(model))
    write_json("generated-page-release-readiness.json", release_readiness(model))
    write_json("generated-page-downstream-tasks.json", downstream_tasks(model))
    write_json("generated-page-ci-evidence-request.json", ci_request(model))
    write_json("generated-page-tag-candidate.json", tag_candidate(model))
    write_json("generated-page-closeout-bundle.json", closeout_bundle(model))
    write_json("generated-page-activation-gate.json", activation_gate(model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
