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
    reproducible_count = 0
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
            gate = report.get("evidence_gate", {})
            evidence_class = gate.get("evidence_class", "UNCLASSIFIED_FAIL_CLOSED")
            reproducible = bool(gate.get("independently_reproducible", False))
            missing_count = len(gate.get("missing_fields", []))
            if reproducible:
                reproducible_count += 1
        else:
            result = "MISSING_REPORT_FAIL_CLOSED"
            cycle = "MISSING"
            authority = None
            evidence_class = "MENTION_ONLY"
            reproducible = False
            missing_count = 8
        page_link = page.replace("docs/external-frameworks/", "./")
        report_link = f"./reports/{framework_id}.compatibility.json"
        rows.append(
            f"| [{name}]({page_link}) | `{evidence_class}` | `{reproducible}` | `{missing_count}` | `{result}` | `{cycle}` | `{authority}` | [report]({report_link}) |"
        )

    content = "\n".join([
        "---",
        "title: External Framework Evaluation Results",
        "---",
        "",
        "# External Framework Evaluation Results",
        "",
        "This page is generated from machine-readable compatibility reports.",
        "",
        "No external framework may be described as comparatively tested unless its report reaches `REPRODUCIBLE_COMPARATIVE_TEST` and records shared vectors, pinned source identity, raw outputs, runtime configuration, declared expected outcomes, replay commands, timestamps, hashes, and an independent rerun.",
        "",
        f"Current independently reproducible comparative evaluations: **{reproducible_count}**.",
        "",
        "A listed result is evidence only. It is not certification, endorsement, formalism adoption, admissibility proof, execution authority, or a ranking of framework value.",
        "",
        "Evidence classes, from weakest to strongest:",
        "",
        "```text",
        "MENTION_ONLY",
        "AUTHOR_COMMENTARY",
        "SOURCE_REVIEWED",
        "ARTIFACT_REVIEWED",
        "PARAMETERIZED_OBSERVATION",
        "REPRODUCIBLE_COMPARATIVE_TEST",
        "```",
        "",
        "| Framework | Evidence Class | Independently Reproducible | Missing Gate Fields | Result | Cycle Status | Execution Authority Claim | Report |",
        "|---|---|---:|---:|---|---|---|---|",
        *rows,
        "",
        "## Boundary",
        "",
        "```text",
        "source review != implementation test",
        "artifact review != independent reproduction",
        "parameterized observation != comparative testing",
        "framework commentary != test result",
        "compatibility evidence != execution authority",
        "```",
        "",
    ])
    OUT.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
