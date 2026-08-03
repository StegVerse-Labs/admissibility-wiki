#!/usr/bin/env python3
"""Validate the admissible structural invariants literature comparison artifacts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "research" / "admissible-structural-invariants-literature-matrix.md"
RECORD = ROOT / "static" / "research" / "admissible-structural-invariants-literature-matrix.v0.1.json"
ALLOWED = {"PARTIAL_ANALOGUE", "CLOSE_PARTIAL_ANALOGUE", "EXACT_PRECEDENT", "NO_MATERIAL_OVERLAP"}
REQUIRED_FIELDS = {
    "formal_verification", "refinement_and_simulation", "dynamical_systems", "category_theory",
    "runtime_assurance", "authorization_systems", "constitutional_change", "distributed_systems",
    "provenance_and_audit", "multi_agent_governance"
}


def fail(message: str) -> None:
    raise SystemExit(f"ADMISSIBLE INVARIANT LITERATURE: FAIL - {message}")


def main() -> None:
    if not PAGE.is_file() or not RECORD.is_file():
        fail("required page or record is missing")
    page = PAGE.read_text(encoding="utf-8")
    if "No exact precedent is asserted" not in page or "novelty_status: NOT_DETERMINED" not in page:
        fail("page must preserve non-novelty posture")
    try:
        data = json.loads(RECORD.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if data.get("novelty_status") != "NOT_DETERMINED":
        fail("novelty status changed without primary-source review")
    if data.get("execution_authority") is not False:
        fail("research comparison must not claim execution authority")
    rows = data.get("rows", [])
    fields = {row.get("field") for row in rows if isinstance(row, dict)}
    if fields != REQUIRED_FIELDS:
        fail(f"field coverage mismatch: {sorted(fields)}")
    for row in rows:
        if row.get("classification") not in ALLOWED:
            fail(f"invalid classification for {row.get('field')}")
        if not row.get("contribution") or not row.get("gap"):
            fail(f"incomplete comparison row for {row.get('field')}")
    if data.get("primary_sources") != []:
        fail("v0.1 baseline must not imply completed primary-source intake")
    print("ADMISSIBLE INVARIANT LITERATURE: PASS - comparison coverage and non-novelty posture validated")


if __name__ == "__main__":
    main()
