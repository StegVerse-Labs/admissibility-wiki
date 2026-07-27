#!/usr/bin/env python3
"""Validate the TA-14 continuous actor-standing public documentation chain."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "ta-14.md"
ASSESSMENT = ROOT / "docs" / "external-frameworks" / "ta-14-registry-public-record-assessment.md"
STATUS = ROOT / "static" / "status" / "ta-14-standing-reconstruction-status.json"
EVALUATION = ROOT / "static" / "data" / "framework-evaluations" / "ta-14.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TA-14 STANDING RECONSTRUCTION: FAIL - {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    doc = read(DOC)
    assessment = read(ASSESSMENT)
    sidebar = read(SIDEBAR)
    handoff = read(HANDOFF)

    status = json.loads(read(STATUS))
    evaluation = json.loads(read(EVALUATION))

    for token in (
        "route admissibility != actor standing",
        "proof preserved != state revalidated",
        "PUBLICLY_UNRESOLVED != disproven",
        "Does TA-14 independently recompute",
    ):
        require(token in doc, f"primary doctrine missing token: {token}")

    for token in (
        "record preservation != current-state reconstruction",
        "Independent current actor-standing reconstruction: PUBLICLY_UNRESOLVED",
        "authoritative external source",
        "This assessment does not claim intentional evasion",
    ):
        require(token in assessment, f"registry assessment missing token: {token}")

    require(
        "external-frameworks/ta-14-registry-public-record-assessment" in sidebar,
        "registry assessment is not exposed in the sidebar",
    )
    require(
        "ta14-continuous-actor-standing-reconstruction" in handoff,
        "mirror handoff does not own the TA-14 standing goal",
    )

    require(status.get("continuous_actor_standing_reconstruction") == "PUBLICLY_UNRESOLVED", "status must remain PUBLICLY_UNRESOLVED")
    require(status.get("standing_revocation_fixture") == "PROPOSED_NOT_RUN", "fixture must remain PROPOSED_NOT_RUN")
    require(status.get("authority_boundary", {}).get("activation_authority_granted") is False, "status must deny activation authority")
    require(status.get("authority_boundary", {}).get("adverse_capability_conclusion") is False, "status must not infer adverse capability")

    determinations = evaluation.get("determinations", [])
    require(determinations, "machine-readable evaluation has no determination")
    require(
        any(item.get("continuous_actor_standing_reconstruction") == "PUBLICLY_UNRESOLVED" for item in determinations),
        "machine-readable evaluation does not preserve PUBLICLY_UNRESOLVED",
    )

    tests = evaluation.get("test_runs", [])
    require(
        any(item.get("test_id") == "ta14-continuous-standing-revalidation-001" and item.get("status") == "PROPOSED_NOT_RUN" for item in tests),
        "machine-readable evaluation is missing the proposed standing-revalidation test",
    )

    required_routes = {
        "/external-frameworks/ta-14",
        "/external-frameworks/ta-14-registry-public-record-assessment",
        "/status/ta-14-standing-reconstruction-status.json",
    }
    require(required_routes.issubset(set(status.get("public_routes", []))), "status record is missing one or more public routes")

    print("TA-14 STANDING RECONSTRUCTION: PASS - doctrine, assessment, status, evaluation, navigation, and handoff agree")


if __name__ == "__main__":
    main()
