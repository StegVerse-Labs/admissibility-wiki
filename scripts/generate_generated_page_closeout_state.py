#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "external-frameworks"


def write_json(name: str, data: dict[str, Any]) -> None:
    path = OUT / name
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def progress() -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_progress",
        "schema_version": "0.1",
        "repo": "StegVerse-Labs/admissibility-wiki",
        "org": "StegVerse-Labs",
        "repo_percent_complete": 84,
        "goal_activation_percent_complete": 84,
        "active_goal": "declarative-external-framework-generation-pipeline",
        "current_checkpoint": "CLOSEOUT_BUNDLE_RECORDED",
        "actual_vs_recorded": {
            "actual_percent": 84,
            "recorded_goal_state_percent": 44,
            "reason": "Generated page state artifacts are now consolidated behind a generator and machine-checked through the existing validation chain."
        },
        "active_surfaces": [
            "metadata",
            "mapping",
            "page_status",
            "analysis_boundary",
            "surface_inventory",
            "surface_handoff",
            "root_addendum",
            "validation_summary",
            "release_readiness",
            "downstream_tasks",
            "ci_evidence_request",
            "tag_candidate",
            "closeout_bundle"
        ],
        "remaining_tasks": [
            {"destination": "StegVerse-Labs/admissibility-wiki", "task": "CI run confirms generated-page closeout state remains green"},
            {"destination": "StegVerse-Labs/admissibility-wiki", "task": "Promote recorded GOAL_STATE once validator update is unblocked"},
            {"destination": "StegVerse-Labs/Site", "task": "Mirror generated external-framework evaluation results after release/tag"},
            {"destination": "GCAT-BCAT-Engine/Publisher", "task": "Add publication/import awareness for generated external-framework result artifacts after release/tag"},
            {"destination": "stegguardian-wiki", "task": "Add downstream execution-authority boundary summary after release/tag"}
        ],
        "boundary": {
            "progress_record_is_authority": False,
            "manual_progress_reconstruction_required": False,
            "single_workflow_policy_preserved": True
        }
    }


def release_readiness() -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_release_readiness",
        "schema_version": "0.1",
        "repo": "StegVerse-Labs/admissibility-wiki",
        "active_goal": "declarative-external-framework-generation-pipeline",
        "release_ready": False,
        "readiness_percent": 84,
        "required_before_tag": [
            "single canonical workflow green after closeout bundle installation",
            "public GitHub Pages verification green",
            "generated external-framework evaluation results reachable on public site",
            "GOAL_STATE promoted after validator update is unblocked",
            "downstream update tasks created for StegVerse-Labs/Site, GCAT-BCAT-Engine/Publisher, and stegguardian-wiki"
        ],
        "already_satisfied": [
            "single workflow policy preserved",
            "generated-page validation summary installed",
            "machine-readable progress state installed",
            "downstream task manifest installed",
            "CI evidence request installed",
            "tag candidate gate installed",
            "closeout bundle installed"
        ],
        "boundary": {
            "release_readiness_is_authority": False,
            "tag_without_green_ci_allowed": False,
            "manual_release_readiness_reconstruction_required": False
        }
    }


def downstream_tasks() -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_downstream_tasks",
        "schema_version": "0.1",
        "repo": "StegVerse-Labs/admissibility-wiki",
        "active_goal": "declarative-external-framework-generation-pipeline",
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


def ci_request() -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_ci_evidence_request",
        "schema_version": "0.1",
        "repo": "StegVerse-Labs/admissibility-wiki",
        "active_goal": "declarative-external-framework-generation-pipeline",
        "requested_evidence": [
            "single canonical workflow conclusion",
            "generated page status validation conclusion",
            "generated page progress validation conclusion",
            "generated page release readiness validation conclusion",
            "generated page downstream task validation conclusion",
            "generated page tag candidate validation conclusion",
            "generated page closeout bundle validation conclusion",
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


def tag_candidate() -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_tag_candidate",
        "schema_version": "0.1",
        "repo": "StegVerse-Labs/admissibility-wiki",
        "active_goal": "declarative-external-framework-generation-pipeline",
        "tag_candidate": "v0.1.0-generated-framework-pages",
        "tag_ready": False,
        "blocked_by": [
            "green CI evidence not yet recorded after closeout bundle installation",
            "public generated evaluation results verification not yet recorded after closeout bundle installation",
            "release readiness remains false until CI and public verification pass"
        ],
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


def closeout_bundle() -> dict[str, Any]:
    return {
        "artifact_type": "generated_page_closeout_bundle",
        "schema_version": "0.1",
        "repo": "StegVerse-Labs/admissibility-wiki",
        "active_goal": "declarative-external-framework-generation-pipeline",
        "closeout_ready": False,
        "closeout_percent": 84,
        "required_artifacts": [
            "docs/external-frameworks/generated-page-progress.json",
            "docs/external-frameworks/generated-page-release-readiness.json",
            "docs/external-frameworks/generated-page-downstream-tasks.json",
            "docs/external-frameworks/generated-page-ci-evidence-request.json",
            "docs/external-frameworks/generated-page-tag-candidate.json"
        ],
        "blocked_by": [
            "green CI evidence after closeout bundle installation not yet recorded",
            "public generated evaluation results verification after closeout bundle installation not yet recorded",
            "release readiness remains false",
            "tag candidate remains blocked"
        ],
        "next_integration_goal_candidate": "post-release downstream generated-framework-results propagation",
        "boundary": {
            "closeout_bundle_is_authority": False,
            "manual_closeout_reconstruction_required": False,
            "thread_archive_ready": False
        }
    }


def main() -> int:
    write_json("generated-page-progress.json", progress())
    write_json("generated-page-release-readiness.json", release_readiness())
    write_json("generated-page-downstream-tasks.json", downstream_tasks())
    write_json("generated-page-ci-evidence-request.json", ci_request())
    write_json("generated-page-tag-candidate.json", tag_candidate())
    write_json("generated-page-closeout-bundle.json", closeout_bundle())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
