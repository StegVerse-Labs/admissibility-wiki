#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "static/status/agcp-session-consolidation.json"
HANDOFF = ROOT / "docs/external-frameworks/AGCP_REGISTRY_MIRROR_HANDOFF.md"
REQUIRED_GOALS = {
    "AGCP-LAYER-DETERMINATION",
    "AGCP-PUBLIC-ASSESSMENT",
    "AGCP-MACHINE-READABLE-BOUNDARY",
    "AGCP-DETERMINISTIC-VALIDATION",
    "AGCP-NONHALTING-CONTINUATION",
    "AGCP-CANONICAL-WORKFLOW-OBSERVATION",
    "AGCP-PUBLIC-ROUTE-OBSERVATION",
    "AGCP-PROPAGATION-REVIEW",
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    require(RECORD.is_file(), f"missing {RECORD.relative_to(ROOT)}", failures)
    require(HANDOFF.is_file(), f"missing {HANDOFF.relative_to(ROOT)}", failures)
    if failures:
        for item in failures:
            print(f"- {item}")
        return 1

    data = json.loads(RECORD.read_text(encoding="utf-8"))
    require(data.get("schema_version") == "agcp-session-consolidation.v1", "schema mismatch", failures)
    canonical = data.get("canonical_continuation", {})
    require(canonical.get("repository") == "StegVerse-Labs/admissibility-wiki", "canonical repository mismatch", failures)
    require(canonical.get("handoff") == "docs/external-frameworks/AGCP_REGISTRY_MIRROR_HANDOFF.md", "canonical handoff mismatch", failures)
    require(canonical.get("task_id") == "ADMISSIBILITY-AGCP-001", "canonical task mismatch", failures)

    goals = data.get("session_goals", [])
    observed = {item.get("goal_id") for item in goals if isinstance(item, dict)}
    require(REQUIRED_GOALS.issubset(observed), "session goal inventory incomplete", failures)
    for item in goals:
        if not isinstance(item, dict):
            failures.append("goal entries must be objects")
            continue
        require(item.get("state") in {"COMPLETE", "MACHINE_OWNED", "BLOCKED", "SUPERSEDED", "MERGED"}, f"invalid goal state for {item.get('goal_id')}", failures)
        if item.get("state") == "BLOCKED":
            require(bool(item.get("release_condition")), f"blocked goal lacks release condition: {item.get('goal_id')}", failures)

    claim = data.get("claim", {})
    require(claim.get("claim_state") == "MACHINE_OWNED", "claim must be machine owned", failures)
    require(bool(claim.get("release_condition")), "claim release condition missing", failures)
    require(bool(claim.get("collision_boundary")), "claim collision boundary missing", failures)

    convergence = data.get("duplicate_and_convergence", {})
    require(convergence.get("merged_into_canonical_workstream") is True, "canonical merge not recorded", failures)
    require(convergence.get("duplicate_implementation_allowed") is False, "duplicate implementation must be denied", failures)

    archival = data.get("session_archival", {})
    require(archival.get("unique_requirements_transferred") is True, "unique requirements not transferred", failures)
    require(archival.get("unassigned_work_exists") is False, "unassigned work remains", failures)
    require(archival.get("machine_owned_continuation_installed") is True, "machine continuation missing", failures)
    require(archival.get("conversation_required_for_continuation") is False, "conversation still required", failures)

    boundary = data.get("authority_boundary", {})
    for key in (
        "consolidation_is_certification",
        "consolidation_is_admissibility",
        "consolidation_grants_execution_authority",
        "consolidation_grants_release_authority",
    ):
        require(boundary.get(key) is False, f"authority boundary weakened: {key}", failures)

    if failures:
        print("AGCP SESSION CONSOLIDATION: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("AGCP SESSION CONSOLIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
