#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
REPORT_DIR = ROOT / "docs" / "external-frameworks" / "reports"
OUT = ROOT / "docs" / "external-frameworks" / "evaluation-results.md"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    registry = read_json(REGISTRY)
    rows: list[str] = []
    for entry in registry.get("entries", []):
        framework_id = entry.get("framework_id")
        name = entry.get("name")
        page = entry.get("path", "")
        report_path = REPORT_DIR / f"{framework_id}.compatibility.json"
        if report_path.exists():
            report = read_json(report_path)
            result = report.get("result", "MISSING")
            cycle = report.get("cycle_status", "MISSING")
            authority = report.get("boundary", {}).get("execution_authority_claim")
        else:
            result = "MISSING_REPORT_FAIL_CLOSED"
            cycle = "MISSING"
            authority = None
        page_link = page.replace("docs/external-frameworks/", "./")
        report_link = f"./reports/{framework_id}.compatibility.json"
        rows.append(f"| [{name}]({page_link}) | `{result}` | `{cycle}` | `{authority}` | [report]({report_link}) |")

    content = "\n".join([
        "---",
        "title: External Framework Evaluation Results",
        "---",
        "",
        "# External Framework Evaluation Results",
        "",
        "This page is generated from machine-readable compatibility reports.",
        "",
        "A listed result is compatibility evidence only. It is not certification, endorsement, formalism adoption, admissibility proof, or execution authority.",
        "",
        "When an external framework is evaluated, the generated compatibility report is the posting source for this page.",
        "",
        "| Framework | Result | Cycle Status | Execution Authority Claim | Report |",
        "|---|---|---|---|---|",
        *rows,
        "",
    ])
    OUT.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
