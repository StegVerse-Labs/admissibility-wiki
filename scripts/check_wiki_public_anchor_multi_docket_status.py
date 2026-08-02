#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "wiki-public-anchor-multi-docket-status.json"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
SELF_REVIEW = ROOT / "static" / "data" / "governed-framework-reviews" / "stegverse-public-anchor.self-review.v1.json"
MANIFEST_CHECK = ROOT / "scripts" / "check_public_anchor_reconstruction_manifest.py"
PUBLIC_ROUTE_CHECK = ROOT / "scripts" / "check_wiki_public_anchor_public_routes.py"
INDEPENDENT_RECONSTRUCTION_INVITATION_CHECK = ROOT / "scripts" / "check_public_anchor_independent_reconstruction_invitation.py"
SESSION_CONSOLIDATION_CHECK = ROOT / "scripts" / "check_session_consolidation_one_world_ai_public_anchor.py"
INTERNAL_TASK_CHECK = ROOT / "scripts" / "check_wiki_public_anchor_internal_tasks.py"
TASK_MESH_CHECK = ROOT / "scripts" / "check_wiki_public_anchor_task_mesh.py"
TASK_MESH_REPORT = ROOT / "reports" / "wiki-public-anchor-task-mesh-execution.json"
COMPLETION_CYCLE_CHECK = ROOT / "scripts" / "check_wiki_public_anchor_completion_cycles.py"
COMPLETION_CYCLE_REPORT = ROOT / "reports" / "wiki-public-anchor-completion-cycle.json"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def load(path: Path, failures: list[str]) -> dict:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object", failures)
    return value if isinstance(value, dict) else {}


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        return
    result = subprocess.run(
        [sys.executable, str(path)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    print(result.stdout.rstrip())
    if result.returncode != 0:
        failures.append(f"{label} validation failed")


def main() -> int:
    failures: list[str] = []
    status = load(STATUS, failures)
    self_review = load(SELF_REVIEW, failures)
    handoff = HANDOFF.read_text(encoding="utf-8") if HANDOFF.exists() else ""

    require(status.get("schema_version") == "wiki-public-anchor-multi-docket-status.v1", "status schema version mismatch", failures)
    require(status.get("state") == "THREE_DOCKETS_IMPLEMENTED_PENDING_CANONICAL_VALIDATION", "multi-docket state mismatch", failures)

    dockets = status.get("dockets", [])
    require(isinstance(dockets, list) and len(dockets) == 3, "status must list exactly three current dockets", failures)
    ids = {item.get("review_id") for item in dockets if isinstance(item, dict)}
    require("review-ta14-reference-docket-2026-07-27" in ids, "TA-14 docket missing", failures)
    require("review-asro-reference-docket-2026-07-27" in ids, "ASRO docket missing", failures)
    require("review-stegverse-public-anchor-self-2026-07-27" in ids, "StegVerse self-review docket missing", failures)

    for item in dockets if isinstance(dockets, list) else []:
        if not isinstance(item, dict):
            continue
        require(item.get("verified_capabilities") == 0, f"{item.get('review_id')} must not claim verified capabilities", failures)
        require(item.get("reconstruction_status") == "PARTIAL", f"{item.get('review_id')} reconstruction must remain PARTIAL", failures)

    boundary = status.get("authority_boundary", {})
    for key in (
        "certification_granted",
        "execution_authority_granted",
        "government_recognition_claimed",
        "internal_validation_establishes_substantive_truth",
        "self_review_establishes_independence",
    ):
        require(boundary.get(key) is False, f"authority boundary {key} must be false", failures)

    require(self_review.get("current_standing") == "PROVISIONAL", "self-review must remain PROVISIONAL", failures)
    require(self_review.get("verified_capabilities") == [], "self-review must have no verified capabilities", failures)
    require("wiki-public-anchor-independent-reconstruction-activation" in handoff, "handoff missing current independent-reconstruction activation goal", failures)
    require("Manual task requirement: none" in handoff, "handoff must preserve no-manual-task posture", failures)

    run_check(MANIFEST_CHECK, "public-anchor reconstruction manifest", failures)
    run_check(PUBLIC_ROUTE_CHECK, "public-anchor route observation receipt", failures)
    run_check(INDEPENDENT_RECONSTRUCTION_INVITATION_CHECK, "independent reconstruction invitation", failures)
    run_check(SESSION_CONSOLIDATION_CHECK, "session consolidation inventory", failures)
    run_check(INTERNAL_TASK_CHECK, "non-halting internal task registry", failures)
    run_check(TASK_MESH_CHECK, "non-halting public-anchor task mesh", failures)
    run_check(COMPLETION_CYCLE_CHECK, "bounded public-anchor completion cycles", failures)

    if TASK_MESH_REPORT.exists():
        report = load(TASK_MESH_REPORT, failures)
        policy = report.get("execution_policy", {})
        require(policy.get("continue_after_queue_failure") is True, "task mesh must continue after queue failure", failures)
        require(policy.get("external_tasks_exist") is False, "task mesh must deny external tasks", failures)
        require(policy.get("failed_queue_blocks_unrelated_queue") is False, "task mesh must not block unrelated queues", failures)
        require(policy.get("evidence_gap_halts_development") is False, "evidence gaps must not halt development", failures)
        require(len(report.get("queues", [])) >= 2, "task mesh must observe public-anchor and TA-14 queues", failures)
    else:
        failures.append(f"missing {TASK_MESH_REPORT.relative_to(ROOT)} after task-mesh execution")

    if COMPLETION_CYCLE_REPORT.exists():
        completion = load(COMPLETION_CYCLE_REPORT, failures)
        require(completion.get("external_tasks_exist") is False, "completion controller must deny external tasks", failures)
        require(completion.get("development_halted") is False, "completion controller must not halt development", failures)
        require(completion.get("policy", {}).get("bounded_retry_prevents_infinite_wait") is True, "completion controller must prevent infinite waiting", failures)
        require(completion.get("policy", {}).get("fixed_point_is_not_completion") is True, "fixed point must not be mislabeled completion", failures)
    else:
        failures.append(f"missing {COMPLETION_CYCLE_REPORT.relative_to(ROOT)} after completion-cycle execution")

    if failures:
        print("WIKI PUBLIC ANCHOR MULTI-DOCKET STATUS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("WIKI PUBLIC ANCHOR MULTI-DOCKET STATUS: PASS - dockets, reconstruction controls, session consolidation, task mesh, and bounded completion cycles remain aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
