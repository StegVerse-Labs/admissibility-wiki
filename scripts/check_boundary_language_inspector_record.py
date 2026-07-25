#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "external-frameworks" / "boundary-language-inspector.md"
RECORD = ROOT / "docs" / "external-frameworks" / "boundary-language-inspector.json"
HANDOFF = ROOT / "docs" / "BOUNDARY_LANGUAGE_INSPECTOR_MIRROR_HANDOFF.md"

REQUIRED_DOC_MARKERS = (
    "Boundary Language Inspector",
    "Replayability",
    "Reconstructability",
    "Full reality reformulation",
    "Every conclusion remains bounded by the evidence surface",
)

EXPECTED_LEVELS = {
    1: "replayability",
    2: "reconstructability",
    3: "full reality reformulation",
}


def main() -> int:
    failures: list[str] = []

    for path in (DOC, RECORD, HANDOFF):
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    if DOC.exists():
        text = DOC.read_text(encoding="utf-8")
        for marker in REQUIRED_DOC_MARKERS:
            if marker.lower() not in text.lower():
                failures.append(f"missing doctrine marker: {marker}")

    if RECORD.exists():
        try:
            data = json.loads(RECORD.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON: {exc}")
            data = {}

        if data.get("record_type") != "external-framework-observatory-record":
            failures.append("record_type must be external-framework-observatory-record")

        framework = data.get("framework") or {}
        if framework.get("name") != "Boundary Language Inspector":
            failures.append("framework.name mismatch")
        if framework.get("primary_pattern") != "bounded-public-contract":
            failures.append("framework.primary_pattern mismatch")

        levels = data.get("public_validation_levels") or []
        if len(levels) != 3:
            failures.append("public_validation_levels must contain exactly three levels")
        else:
            observed = {item.get("level"): item.get("name") for item in levels if isinstance(item, dict)}
            if observed != EXPECTED_LEVELS:
                failures.append(f"public validation levels mismatch: {observed}")

        authority = data.get("authority_boundary") or {}
        for key in ("execution_authority_inherited", "certification", "ontology_adoption"):
            if authority.get(key) is not False:
                failures.append(f"authority_boundary.{key} must be false")
        if authority.get("admissibility_status") != "not established":
            failures.append("authority_boundary.admissibility_status must be not established")

    print("BOUNDARY LANGUAGE INSPECTOR RECORD:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
