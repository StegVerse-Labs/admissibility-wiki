#!/usr/bin/env python3
"""Validate the bounded AGCP Registry assessment record.

This validator checks structure and required non-claims only. It does not
verify AGCP, certify an implementation, or grant authority.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "static/external-frameworks/agcp-registry-assessment.v0.1.json"
PAGE = ROOT / "docs/external-frameworks/agcp-registry.md"
HANDOFF = ROOT / "docs/external-frameworks/AGCP_REGISTRY_MIRROR_HANDOFF.md"

EXPECTED_FALSE_CLAIMS = {
    "conformance_implies_specification_completeness",
    "conformance_implies_independent_reconstruction",
    "conformance_implies_commit_time_validity",
    "conformance_implies_admissibility",
    "conformance_implies_execution_authority",
    "conformance_implies_consequence_authority",
}

EXPECTED_FALSE_AUTHORITY = {
    "certification",
    "endorsement",
    "admissibility",
    "execution",
    "publication",
    "release",
    "cross_repository_mutation",
}

REQUIRED_DIMENSIONS = {
    "public_specification_identity",
    "requirement_inventory",
    "applicability_transparency",
    "evidence_accessibility",
    "deterministic_assessment",
    "evaluator_independence",
    "time_t_reconstruction",
    "commit_time_validity",
    "dispute_and_correction",
    "conformance_claim",
    "admissibility",
    "execution_authority",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AGCP assessment validation failed: {message}")


def main() -> None:
    for path in (ASSESSMENT, PAGE, HANDOFF):
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}")

    data = json.loads(ASSESSMENT.read_text(encoding="utf-8"))

    require(data.get("record_type") == "external_framework_assessment", "record_type")
    require(data.get("framework_id") == "agcp-registry", "framework_id")
    require(data.get("review_state") == "SOURCE_CAPTURED_REVIEW_ACTIVE", "review_state")

    capture = data.get("source_capture", {})
    require(capture.get("independently_verified") is False, "source must remain unverified")
    require(capture.get("scope_qualification_present") is True, "scope qualification")
    require(capture.get("planned_release_observed") is False, "future release cannot be observed")

    dimensions = data.get("dimensions", {})
    require(REQUIRED_DIMENSIONS.issubset(dimensions), "missing assessment dimensions")
    require(dimensions.get("admissibility") == "NOT_ESTABLISHED", "admissibility boundary")
    require(dimensions.get("execution_authority") == "NOT_ESTABLISHED", "execution boundary")

    boundaries = data.get("claim_boundaries", {})
    require(EXPECTED_FALSE_CLAIMS.issubset(boundaries), "missing claim boundaries")
    require(all(boundaries[key] is False for key in EXPECTED_FALSE_CLAIMS), "claim boundary weakened")

    task = data.get("task_control", {})
    require(task.get("task_id") == "ADMISSIBILITY-AGCP-001", "task identity")
    require(task.get("execution_class") == "PARALLEL_SAFE", "execution class")
    require(task.get("owner") == "repository_canonical_workflow", "repository ownership")
    require(task.get("external_tasks_allowed") is False, "external tasks prohibited")
    require(task.get("manual_user_tasks_required") == [], "manual tasks prohibited")

    authority = data.get("authority", {})
    require(EXPECTED_FALSE_AUTHORITY.issubset(authority), "missing authority boundaries")
    require(all(authority[key] is False for key in EXPECTED_FALSE_AUTHORITY), "authority boundary weakened")

    page = PAGE.read_text(encoding="utf-8")
    for phrase in (
        "AGCP full conformance",
        "!= admissibility",
        "No user-operated or external task is required",
        "AGCP_REGISTRY_MIRROR_HANDOFF.md",
    ):
        require(phrase in page, f"page missing required phrase: {phrase}")

    handoff = HANDOFF.read_text(encoding="utf-8")
    require("ADMISSIBILITY-AGCP-001" in handoff, "handoff task missing")
    require("no external tasks" in handoff.lower(), "handoff external-task boundary missing")

    print("AGCP Registry assessment: PASS")


if __name__ == "__main__":
    main()
