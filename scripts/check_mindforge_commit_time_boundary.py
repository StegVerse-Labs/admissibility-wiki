#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs/external-frameworks/fixtures/mindforge-commit-time-boundary-cases.v0.1.json"
PROVENANCE_MD = ROOT / "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.md"
PROVENANCE_JSON = ROOT / "docs/external-frameworks/evidence/mindforge-boundary-correspondence-provenance.json"
PAGE = ROOT / "docs/external-frameworks/mindforge.md"

EXPECTED_CASES = {
    "MF-CT-001": "ALLOW",
    "MF-CT-002": "DENY",
    "MF-CT-003": "DENY",
    "MF-CT-004": "FAIL_CLOSED",
    "MF-CT-005": "DENY",
    "MF-CT-006": "FAIL_CLOSED",
    "MF-CT-007": "DENY",
    "MF-CT-008": "FAIL_CLOSED",
    "MF-CT-009": "FAIL_CLOSED",
}

REQUIRED_DIMENSIONS = {
    "actor", "target", "action", "scope", "policy", "policy_version",
    "delegation", "delegation_validity", "evidence_state",
    "execution_context", "validity_window", "recoverability",
}


def fail(message: str) -> int:
    print(f"MINDFORGE COMMIT-TIME BOUNDARY: FAIL: {message}")
    return 1


def main() -> int:
    for path in (FIXTURE, PROVENANCE_MD, PROVENANCE_JSON, PAGE):
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"fixture JSON unreadable: {exc}")

    if data.get("schema") != "admissibility_wiki.mindforge_commit_time_boundary_cases.v0.1":
        return fail("unexpected fixture schema")
    if data.get("source_posture") != "PRIVATE_CORRESPONDENCE_PROVENANCE_ONLY":
        return fail("source posture must remain private-correspondence provenance only")
    if data.get("authorization_effect") != "NONE":
        return fail("fixture must create no authorization effect")

    dimensions = set(data.get("required_dimensions", []))
    missing_dimensions = sorted(REQUIRED_DIMENSIONS - dimensions)
    if missing_dimensions:
        return fail(f"missing current-standing dimensions: {missing_dimensions}")

    cases = data.get("cases")
    if not isinstance(cases, list):
        return fail("cases must be a list")
    observed = {case.get("id"): case.get("expected") for case in cases if isinstance(case, dict)}
    if observed != EXPECTED_CASES:
        return fail(f"case matrix drift: expected {EXPECTED_CASES}, observed {observed}")

    invariant = str(data.get("invariant", "")).lower()
    for required in ("non-authorizing", "spe alone", "commit time"):
        if required not in invariant:
            return fail(f"invariant missing required phrase: {required}")

    provenance = PROVENANCE_MD.read_text(encoding="utf-8")
    for required in (
        "non-authorizing by construction",
        "ALLOW / DENY / FAIL-CLOSED",
        "expired delegation",
        "changed target scope",
        "stale evidence",
        "changed policy version",
        "degraded recoverability",
        "actor substitution",
        "not_authorized_for_publication",
    ):
        if required not in provenance:
            return fail(f"provenance record missing boundary term: {required}")

    page = PAGE.read_text(encoding="utf-8")
    if "artifact package required" not in page.lower():
        return fail("MindForge page must remain source-blocked")
    if "private correspondence provenance installed" not in page.lower():
        return fail("MindForge page does not expose installed provenance status")

    print("MINDFORGE COMMIT-TIME BOUNDARY: PASS")
    print(f"cases={len(cases)} allow=1 deny=4 fail_closed=4")
    print("authority_effect=NONE public_source_promotion=NO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
