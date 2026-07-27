#!/usr/bin/env python3
"""Validate the bounded ArquivoNulo execution-boundary evaluation chain."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "arquivonulo.md"
EVALUATION = ROOT / "static" / "data" / "framework-evaluations" / "arquivonulo.json"
INDEX = ROOT / "static" / "data" / "framework-evaluations" / "index.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ARQUIVONULO_MIRROR_HANDOFF.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ARQUIVONULO EXECUTION BOUNDARY: FAIL - {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    doc = read(DOC)
    sidebar = read(SIDEBAR)
    handoff = read(HANDOFF)
    evaluation = json.loads(read(EVALUATION))
    index = json.loads(read(INDEX))

    for token in (
        "valid proof != continuing admissibility",
        "interdiction != pre-consequence prevention",
        "anchored state != current reality",
        "S5 Execution",
        "S7 Proof Verification",
        "PUBLICLY_UNRESOLVED",
    ):
        require(token in doc, f"doctrine missing token: {token}")

    require(
        "external-frameworks/arquivonulo" in sidebar,
        "ArquivoNulo route is not exposed in the sidebar",
    )
    require(
        "arquivonulo-execution-boundary-evaluation" in handoff,
        "goal-specific handoff does not own the ArquivoNulo evaluation",
    )

    require(evaluation.get("framework_id") == "arquivonulo", "framework_id must be arquivonulo")
    source = evaluation.get("source_posture", {})
    require(source.get("owner_controlled_public_sources_observed") is True, "public-source observation must be recorded")
    require(source.get("owner_confirmed_frozen_declaration") is False, "owner-confirmed declaration must remain false")
    require(source.get("live_test_run") is False, "live test must remain false")

    boundary = evaluation.get("execution_boundary", {})
    require(boundary.get("status") == "PUBLICLY_UNRESOLVED", "execution boundary must remain PUBLICLY_UNRESOLVED")
    require(boundary.get("commit_bound_prevention_demonstrated") is False, "commit-bound prevention must not be claimed")
    require(boundary.get("post_execution_verification_possible_from_published_sequence") is True, "published sequence ambiguity must be preserved")

    continuing = evaluation.get("continuing_admissibility", {})
    require(continuing.get("status") == "PUBLICLY_UNRESOLVED", "continuing admissibility must remain PUBLICLY_UNRESOLVED")
    required_proxies = {
        "current_authority",
        "applicable_policy",
        "admissible_evidence",
        "environmental_correspondence",
        "recoverability",
        "intervention_capacity",
    }
    require(required_proxies.issubset(set(continuing.get("integrity_proof_is_not_proxy_for", []))), "continuing-admissibility proxy exclusions are incomplete")

    authority = evaluation.get("authority", {})
    for key in ("comparison", "certification", "endorsement", "execution", "custody", "integration"):
        require(authority.get(key) is False, f"authority.{key} must remain false")

    registry_entry = next((item for item in index.get("frameworks", []) if item.get("framework_id") == "arquivonulo"), None)
    require(registry_entry is not None, "framework registry is missing ArquivoNulo")
    require(registry_entry.get("record_path") == "arquivonulo.json", "registry record_path is incorrect")
    require(registry_entry.get("live_test_status") == "NOT_TESTED", "registry live_test_status must remain NOT_TESTED")

    print("ARQUIVONULO EXECUTION BOUNDARY: PASS - doctrine, evaluation, registry, navigation, and handoff agree")


if __name__ == "__main__":
    main()
