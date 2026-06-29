#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
REPORT_DIR = ROOT / "docs" / "external-frameworks" / "reports"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    if not REGISTRY.exists():
        failures.append("registry file unavailable")
    if not REPORT_DIR.exists():
        failures.append("report directory unavailable")

    if failures:
        print("EXTERNAL FRAMEWORK REPORT COVERAGE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = load_json(REGISTRY)
    ids = [entry.get("framework_id") for entry in registry.get("entries", [])]

    for framework_id in ids:
        if not isinstance(framework_id, str) or not framework_id:
            failures.append("registry entry has invalid framework_id")
            continue
        report_path = REPORT_DIR / f"{framework_id}.compatibility.json"
        if not report_path.exists():
            failures.append(f"coverage absent for framework: {framework_id}")
            continue
        report = load_json(report_path)
        if report.get("framework_id") != framework_id:
            failures.append(f"coverage id mismatch for framework: {framework_id}")
        if report.get("framework_manifest") != next(entry.get("manifest_path") for entry in registry.get("entries", []) if entry.get("framework_id") == framework_id):
            failures.append(f"coverage manifest mismatch for framework: {framework_id}")

    extra_reports = sorted(REPORT_DIR.glob("*.compatibility.json"))
    known = {framework_id for framework_id in ids if isinstance(framework_id, str)}
    for report_path in extra_reports:
        report = load_json(report_path)
        framework_id = report.get("framework_id")
        if framework_id not in known:
            failures.append(f"coverage report not indexed: {report_path.name}")

    print("EXTERNAL FRAMEWORK REPORT COVERAGE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
