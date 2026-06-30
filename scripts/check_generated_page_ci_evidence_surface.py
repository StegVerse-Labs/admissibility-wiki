#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACES = ROOT / "docs" / "external-frameworks" / "generated-page-surfaces.json"
GENERATOR = "scripts/generate_generated_page_ci_evidence_request.py"
VALIDATOR = "scripts/check_generated_page_ci_evidence_request.py"
SURFACE_ID = "ci_evidence_request"


def main() -> int:
    failures: list[str] = []
    if not SURFACES.exists():
        print("GENERATED PAGE CI EVIDENCE SURFACE: FAIL")
        print("- surface inventory missing")
        return 1

    data = json.loads(SURFACES.read_text(encoding="utf-8"))
    active = {item.get("surface_id"): item for item in data.get("active_surfaces", [])}
    item = active.get(SURFACE_ID)
    if not item:
        failures.append("CI evidence request surface missing")
    else:
        if item.get("generator") != GENERATOR:
            failures.append("CI evidence request generator mismatch")
        if item.get("validator") != VALIDATOR:
            failures.append("CI evidence request validator mismatch")
        if item.get("manual_task_required") is not False:
            failures.append("CI evidence request manual task boundary mismatch")

    for path in [GENERATOR, VALIDATOR]:
        if not (ROOT / path).exists():
            failures.append(f"referenced file missing: {path}")

    print("GENERATED PAGE CI EVIDENCE SURFACE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
