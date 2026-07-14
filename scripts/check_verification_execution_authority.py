#!/usr/bin/env python3
"""Validate the verification-versus-execution-authority doctrine and status artifact."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/governance/verification-vs-execution-authority.md"
STATUS = ROOT / "static/status/verification-execution-authority-status.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
DEPLOYMENT_CHECK = ROOT / "scripts/check_governed_llm_deployment_status.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"VERIFICATION EXECUTION AUTHORITY: FAIL - {message}")


def main() -> None:
    require(DOC.is_file(), f"missing doctrine page: {DOC.relative_to(ROOT)}")
    require(STATUS.is_file(), f"missing status artifact: {STATUS.relative_to(ROOT)}")
    require(DEPLOYMENT_CHECK.is_file(), f"missing deployment checker: {DEPLOYMENT_CHECK.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    deployment_check = DEPLOYMENT_CHECK.read_text(encoding="utf-8")
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    required_doc_phrases = (
        "Verification Is Not Execution Authority",
        "Who or what was authorized to let this specific consequential decision become real?",
        "Show where the workflow can still say \"NO.\"",
        "independent verification != execution authority",
        "ALLOW`, `DENY`, or `FAIL_CLOSED",
        "organization-issued public announcement",
    )
    for phrase in required_doc_phrases:
        require(phrase in doc, f"doctrine page missing required boundary text: {phrase}")

    require(
        "governance/verification-vs-execution-authority" in sidebar,
        "doctrine page is not present in sidebars.js",
    )
    require(
        "verification-execution-authority-status.json" in handoff,
        "mirror handoff does not reference the status artifact",
    )

    required_public_routes = (
        "verification_execution_authority_doctrine",
        "verification_execution_authority_status",
        "/governance/verification-vs-execution-authority",
        "/status/verification-execution-authority-status.json",
    )
    for marker in required_public_routes:
        require(marker in deployment_check, f"deployment checker missing publication marker: {marker}")

    require(status.get("goal_id") == "verification-vs-execution-authority", "unexpected goal_id")
    require(status.get("manual_task_requirement") == "none", "manual task requirement must remain none")
    require(status.get("user_manual_action_required") is False, "user manual action must remain false")
    require(status.get("downstream_mutation_authority") == "none_granted", "downstream authority must remain ungranted")

    boundary = status.get("governance_boundary", {})
    require(boundary.get("verification_is_execution_authority") is False, "verification must not be promoted to execution authority")
    require(boundary.get("certification_grants_action_level_admissibility") is False, "certification must not grant action-level admissibility")
    require(boundary.get("independent_review_is_evidence_input") is True, "independent review must be represented as evidence input")
    require(boundary.get("commit_time_denial_point_required_for_high_risk_execution") is True, "commit-time denial point requirement missing")
    require(boundary.get("allowed_decisions") == ["ALLOW", "DENY", "FAIL_CLOSED"], "unexpected decision set")

    source = status.get("source", {})
    require(source.get("published_date") == "2026-04-13", "unexpected source publication date")
    require(source.get("classification") == "organization_issued_public_announcement", "unexpected source classification")

    publication = status.get("publication_verification", {})
    require(publication.get("execution_surface") == ".github/workflows/validate-chain-continuation.yml", "unexpected publication execution surface")
    require(publication.get("job") == "verify-public-pages", "unexpected publication verification job")
    require(publication.get("checker") == "scripts/check_governed_llm_deployment_status.py", "unexpected publication checker")
    require(publication.get("manual_tasks_required") == [], "publication verification must not create manual tasks")

    print("VERIFICATION EXECUTION AUTHORITY: PASS")


if __name__ == "__main__":
    main()