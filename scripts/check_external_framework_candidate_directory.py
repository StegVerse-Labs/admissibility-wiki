#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs" / "external-frameworks" / "candidate-directory.md"
INTAKE = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.json"
INTAKE_DOC = ROOT / "docs" / "external-frameworks" / "expanded-framework-intake.md"
SIDEBAR = ROOT / "sidebars.js"


def main() -> int:
    failures: list[str] = []

    for path in [DIRECTORY, INTAKE, INTAKE_DOC, SIDEBAR]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK CANDIDATE DIRECTORY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    directory = DIRECTORY.read_text(encoding="utf-8")
    intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    intake_doc = INTAKE_DOC.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")

    candidates = [item for item in intake.get("candidates", []) if isinstance(item, dict)]
    if len(candidates) != 42:
        failures.append(f"expected 42 intake candidates, found {len(candidates)}")

    missing_names: list[str] = []
    for candidate in candidates:
        name = candidate.get("name")
        if not name or name not in directory:
            missing_names.append(str(name or candidate.get("candidate_id")))

    for name in missing_names:
        failures.append(f"candidate missing from directory: {name}")

    for phrase in [
        "registered framework and crosswalk entries: 19",
        "additional source-required candidates: 42",
        "total visible observatory entries: 61",
        "candidate visibility != validation",
        "No candidate is promoted solely because it appears in this directory.",
    ]:
        if phrase not in directory:
            failures.append(f"directory missing phrase: {phrase}")

    if "External Framework Candidate Directory" not in intake_doc:
        failures.append("expanded intake page missing candidate directory link")
    if "total visible observatory entries: 61" not in intake_doc:
        failures.append("expanded intake page missing total observatory count")
    if "external-frameworks/candidate-directory" not in sidebar:
        failures.append("sidebar missing candidate directory")

    print("EXTERNAL FRAMEWORK CANDIDATE DIRECTORY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
