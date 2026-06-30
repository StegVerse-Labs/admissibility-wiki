#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs" / "external-frameworks" / "generated-page-state-model.json"

REQUIRED_SURFACES = [
    "metadata",
    "mapping",
    "page_status",
    "analysis_boundary",
    "surface_inventory",
    "surface_handoff",
    "root_addendum",
    "validation_summary",
    "validation_summary_generation",
    "release_readiness",
    "downstream_tasks",
    "ci_evidence_request",
    "tag_candidate",
    "closeout_bundle",
    "activation_gate",
]

REQUIRED_DESTINATIONS = [
    "StegVerse-Labs/admissibility-wiki",
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "stegguardian-wiki",
]

REQUIRED_DOWNSTREAM_DESTINATIONS = [
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "stegguardian-wiki",
]


def require_bool(boundary: dict[str, Any], key: str, expected: bool, failures: list[str]) -> None:
    if boundary.get(key) is not expected:
        failures.append(f"boundary mismatch: {key}")


def main() -> int:
    failures: list[str] = []
    if not MODEL.exists():
        print("GENERATED PAGE STATE MODEL: FAIL")
        print("- state model missing")
        return 1

    data = json.loads(MODEL.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_state_model":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("org") != "StegVerse-Labs":
        failures.append("org mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("current_checkpoint") != "CANONICAL_VALIDATION_GREEN":
        failures.append("checkpoint mismatch")
    if data.get("repo_percent_complete") != 99:
        failures.append("repo percent mismatch")
    if data.get("goal_activation_percent_complete") != 99:
        failures.append("activation percent mismatch")
    if data.get("recorded_goal_state_percent") != 99:
        failures.append("recorded percent mismatch")

    surfaces = data.get("active_surfaces", [])
    for surface in REQUIRED_SURFACES:
        if surface not in surfaces:
            failures.append(f"missing surface: {surface}")

    destinations = {item.get("destination") for item in data.get("remaining_tasks", [])}
    for destination in REQUIRED_DESTINATIONS:
        if destination not in destinations:
            failures.append(f"missing destination: {destination}")

    downstream = data.get("downstream", {})
    if downstream.get("activation_condition") != "after release tag and green public verification":
        failures.append("downstream activation condition mismatch")
    downstream_tasks = {item.get("destination"): item for item in downstream.get("tasks", [])}
    for destination in REQUIRED_DOWNSTREAM_DESTINATIONS:
        task = downstream_tasks.get(destination)
        if not task:
            failures.append(f"missing downstream task: {destination}")
            continue
        if not task.get("task_id"):
            failures.append(f"downstream task id missing: {destination}")
        if not task.get("required_input"):
            failures.append(f"downstream required input missing: {destination}")
        if task.get("status") != "pending_release_tag":
            failures.append(f"downstream task status mismatch: {destination}")

    release = data.get("release", {})
    if release.get("release_ready") is not False:
        failures.append("release must remain fail-closed before authorization")
    if release.get("readiness_percent") != 99:
        failures.append("release percent mismatch")
    for item in ["canonical validation green", "page-status generator idempotence installed"]:
        if item not in release.get("already_satisfied", []):
            failures.append(f"missing satisfied release item: {item}")

    tag = data.get("tag", {})
    if tag.get("tag_candidate") != "v0.1.0-generated-framework-pages":
        failures.append("tag candidate mismatch")
    if tag.get("tag_ready") is not False:
        failures.append("tag must remain blocked before release authorization")
    if not tag.get("blocked_by"):
        failures.append("tag blockers missing")

    activation = data.get("activation", {})
    if activation.get("activation_ready") is not False:
        failures.append("activation must remain blocked before release authorization")
    if activation.get("activation_percent") != 99:
        failures.append("activation percent mismatch")
    if not activation.get("required_to_activate"):
        failures.append("activation requirements missing")
    if not activation.get("fail_closed_until"):
        failures.append("activation fail-closed list missing")

    boundary = data.get("boundary", {})
    require_bool(boundary, "state_model_is_authority", False, failures)
    require_bool(boundary, "generated_outputs_are_authority", False, failures)
    require_bool(boundary, "release_without_authorization_allowed", False, failures)
    require_bool(boundary, "missing_public_evidence_blocks_activation", True, failures)
    require_bool(boundary, "manual_state_reconstruction_required", False, failures)
    require_bool(boundary, "thread_archive_ready", False, failures)

    print("GENERATED PAGE STATE MODEL:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
