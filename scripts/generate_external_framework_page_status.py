#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
REPORT_DIR = ROOT / "docs" / "external-frameworks" / "reports"
ANALYSIS_BOUNDARY = ROOT / "scripts" / "generate_external_framework_page_analysis_boundary.py"
START = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:START -->"
END = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:END -->"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def block_for(entry: dict[str, Any]) -> str:
    framework_id = entry["framework_id"]
    report_path = REPORT_DIR / f"{framework_id}.compatibility.json"
    if report_path.exists():
        report = read_json(report_path)
        result = report.get("result", "MISSING_REPORT_FAIL_CLOSED")
        cycle_status = report.get("cycle_status", "MISSING")
        authority = report.get("boundary", {}).get("execution_authority_claim")
        manifest = report.get("framework_manifest", entry.get("manifest_path", ""))
    else:
        result = "MISSING_REPORT_FAIL_CLOSED"
        cycle_status = "MISSING"
        authority = False
        manifest = entry.get("manifest_path", "")

    report_rel = f"./reports/{framework_id}.compatibility.json"
    return "\n".join([
        START,
        "",
        "## Generated Evaluation Status",
        "",
        "This section is generated from the framework manifest and compatibility report. Do not edit it manually.",
        "",
        f"- Framework ID: `{framework_id}`",
        f"- Manifest: `{manifest}`",
        f"- Compatibility report: `{report_rel}`",
        f"- Evaluation result: `{result}`",
        f"- Cycle status: `{cycle_status}`",
        f"- Execution authority claim: `{authority}`",
        "- Posting source: generated compatibility report",
        "- Generated status is descriptive compatibility evidence only.",
        "",
        END,
    ])


def insert_block(text: str, block: str) -> str:
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    lines = text.splitlines()
    insert_at = 0
    if lines and lines[0] == "---":
        for index in range(1, len(lines)):
            if lines[index] == "---":
                insert_at = index + 1
                break
    for index, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = index + 1
            break
    new_lines = lines[:insert_at] + ["", block, ""] + lines[insert_at:]
    return "\n".join(new_lines).rstrip() + "\n"


def main() -> int:
    registry = read_json(REGISTRY)
    for entry in registry.get("entries", []):
        path = ROOT / entry["path"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        updated = insert_block(text, block_for(entry))
        path.write_text(updated, encoding="utf-8")
    if ANALYSIS_BOUNDARY.exists():
        subprocess.run(["python", str(ANALYSIS_BOUNDARY)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
