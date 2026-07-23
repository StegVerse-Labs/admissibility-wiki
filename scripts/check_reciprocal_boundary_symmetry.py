#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "static" / "data" / "framework-evaluations"


def main() -> int:
    failures: list[str] = []
    record = json.loads((BASE / "asro.json").read_text(encoding="utf-8"))
    manifest = json.loads((BASE / "asro" / "correspondence-manifest.json").read_text(encoding="utf-8"))
    declaration = json.loads((BASE / "asro" / "stegverse-companion-layer-declaration.json").read_text(encoding="utf-8"))
    reviewer = json.loads((BASE / "asro" / "reviewer-profile.json").read_text(encoding="utf-8"))

    if declaration.get("canonical_status") != "CONTROLLING_SOURCE_DECLARATION":
        failures.append("source declaration must remain controlling")
    if reviewer.get("provenance", {}).get("derivation_status") != "DERIVATIVE":
        failures.append("reviewer profile must remain derivative")
    if reviewer.get("issuer") != "unresolved":
        failures.append("reviewer issuer must remain unresolved")

    determination = manifest.get("determination", {})
    prohibited = {
        "truth_established": False,
        "sufficiency_established": False,
        "validity_established": False,
        "admissibility_established": False,
        "authority_inherited": False,
    }
    for field, expected in prohibited.items():
        if determination.get(field) is not expected:
            failures.append(f"asymmetric authority promotion at {field}")

    for det in record.get("determinations", []):
        if det.get("parentage_claim") not in ("NOT_CLAIMED", "INCONCLUSIVE"):
            failures.append("bounded comparison must not establish parentage")

    if failures:
        print("RECIPROCAL BOUNDARY SYMMETRY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("RECIPROCAL BOUNDARY SYMMETRY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
