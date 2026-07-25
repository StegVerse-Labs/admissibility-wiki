#!/usr/bin/env python3
"""Run canonical pre-scan generators and validators without hiding later failures."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "canonical-prescan-report.json"

COMMANDS = [
    ("validate-inference-window-governance", [sys.executable, "scripts/validate_inference_window_governance.py"]),
    ("test-inference-window-governance", [sys.executable, "-m", "unittest", "tests.test_inference_window_governance"]),
    ("generate-external-framework-reports", [sys.executable, "scripts/generate_external_framework_reports.py"]),
    ("generate-external-framework-results", [sys.executable, "scripts/generate_external_framework_results.py"]),
    ("generate-external-framework-page-metadata", [sys.executable, "scripts/generate_external_framework_page_metadata.py"]),
    ("generate-external-framework-page-mapping", [sys.executable, "scripts/generate_external_framework_page_mapping.py"]),
    ("generate-external-framework-page-status", [sys.executable, "scripts/generate_external_framework_page_status.py"]),
    ("generate-external-framework-automation-readiness", [sys.executable, "scripts/generate_external_framework_automation_readiness.py"]),
    ("validate-external-framework-automation-readiness", [sys.executable, "scripts/check_external_framework_automation_readiness.py"]),
]


def append_summary(report: dict[str, object]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    results = report["results"]
    lines = [
        "## Canonical pre-scan",
        "",
        f"**Result:** `{report['overall_status']}`  ",
        f"**Commands:** {report['passed_commands']}/{report['total_commands']} passed; {report['failed_commands']} failed",
        "",
        "| Command | Status | Exit | Duration |",
        "|---|---:|---:|---:|",
    ]
    for result in results:
        lines.append(
            f"| `{result['id']}` | `{result['status']}` | `{result['return_code']}` | `{result['duration_seconds']}s` |"
        )
    failures = [result for result in results if result["status"] == "FAIL"]
    if failures:
        lines.extend(["", "### Pre-scan failure details", ""])
        for failure in failures:
            lines.extend([
                f"#### `{failure['id']}`",
                "",
                f"Command: `{' '.join(failure['command'])}`",
                "",
                "```text",
                str(failure.get("output") or "(no output)")[-4000:],
                "```",
                "",
            ])
    with Path(summary_path).open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main() -> int:
    started = time.time()
    results: list[dict[str, object]] = []
    for command_id, command in COMMANDS:
        command_started = time.time()
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        status = "PASS" if completed.returncode == 0 else "FAIL"
        output = completed.stdout.rstrip()
        result = {
            "id": command_id,
            "command": command,
            "status": status,
            "return_code": completed.returncode,
            "duration_seconds": round(time.time() - command_started, 3),
            "output": output[-12000:],
        }
        results.append(result)
        print(f"{command_id}: {status}")
        if output:
            print(output)
        if status == "FAIL" and os.environ.get("GITHUB_ACTIONS"):
            annotation = output.replace("\r", " ").replace("\n", "%0A")[-2000:] or "no output"
            print(f"::error title=Canonical pre-scan failure ({command_id})::{annotation}")

    failed = sum(result["status"] == "FAIL" for result in results)
    report = {
        "schema": "admissibility_wiki.canonical_prescan_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": "FAIL" if failed else "PASS",
        "total_commands": len(results),
        "passed_commands": len(results) - failed,
        "failed_commands": failed,
        "duration_seconds": round(time.time() - started, 3),
        "results": results,
        "authority_boundary": "This diagnostic pre-scan receipt grants no deployment, execution, certification, release, admissibility, standing, publication, or downstream mutation authority.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    append_summary(report)
    print(f"CANONICAL PRE-SCAN: {report['overall_status']}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
