#!/usr/bin/env python3
"""Validate peer-preservation publication artifacts before public deployment."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTRINE = ROOT / "docs/formalisms/peer-preservation-inference-boundary.md"
SCHEMA = ROOT / "static/schemas/peer-preservation-observation.schema.json"
FIXTURES = ROOT / "tests/fixtures/peer-preservation-cases.json"
CHECKER = ROOT / "scripts/check_peer_preservation_claims.py"
STATUS = ROOT / "static/status/peer-preservation-inference-boundary-status.json"
RECEIPT = ROOT / "receipts/peer-preservation-claim-validation-receipt.json"
HANDOFF = ROOT / "docs/PEER_PRESERVATION_MIRROR_HANDOFF.md"
SIDEBAR = ROOT / "sidebars.js"

REQUIRED_DOCTRINE_MARKERS = (
    "SHUTDOWN != FAILURE",
    "similar behavior != cross-service conferral",
    "natural-language rationale != proof of internal moral state",
)


def require_file(path: Path, failures: list[str]) -> None:
    if not path.is_file():
        failures.append(f"missing {path.relative_to(ROOT)}")


def main() -> int:
    failures: list[str] = []
    for path in (DOCTRINE, SCHEMA, FIXTURES, CHECKER, STATUS, RECEIPT, HANDOFF, SIDEBAR):
        require_file(path, failures)

    if failures:
        print("PEER PRESERVATION PUBLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doctrine = DOCTRINE.read_text(encoding="utf-8")
    for marker in REQUIRED_DOCTRINE_MARKERS:
        if marker not in doctrine:
            failures.append(f"doctrine missing marker: {marker}")

    sidebar = SIDEBAR.read_text(encoding="utf-8")
    if "formalisms/peer-preservation-inference-boundary" not in sidebar:
        failures.append("peer-preservation formalism is not registered in sidebars.js")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    if status.get("goal_id") != "peer-preservation-inference-boundary":
        failures.append("status goal_id mismatch")
    if status.get("state") not in {
        "IMPLEMENTED_PENDING_CANONICAL_WORKFLOW_VERIFICATION",
        "CANONICAL_WORKFLOW_VERIFIED_PENDING_PUBLIC_OBSERVATION",
        "PUBLICATION_OBSERVED_COMPLETE",
    }:
        failures.append("status state is not an allowed fail-closed activation state")
    if status.get("manual_task_requirement") != "none":
        failures.append("manual task requirement must remain none")
    if status.get("grants_execution_authority") is not False:
        failures.append("status must not grant execution authority")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("result") != "PASS":
        failures.append("claim validation receipt is not PASS")
    if receipt.get("fixture_count") != 6:
        failures.append("claim validation receipt fixture_count must be 6")
    boundaries = receipt.get("boundaries", {})
    if boundaries.get("decides_consciousness_or_personhood") is not False:
        failures.append("receipt must preserve consciousness/personhood boundary")
    if boundaries.get("treats_similarity_as_transfer") is not False:
        failures.append("receipt must not treat similarity as transfer")

    handoff = HANDOFF.read_text(encoding="utf-8")
    for marker in (
        "Canonical validation integration: installed",
        "Public activation observation:",
        "Manual task requirement: none",
    ):
        if marker not in handoff:
            failures.append(f"handoff missing marker: {marker}")

    if failures:
        print("PEER PRESERVATION PUBLICATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PEER PRESERVATION PUBLICATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
