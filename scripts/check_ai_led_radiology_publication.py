#!/usr/bin/env python3
"""Validate local and optional live publication surfaces for AI-led radiology."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static" / "status" / "ai-led-radiology-execution-status.json"
FORMALISM = ROOT / "docs" / "formalisms" / "ai-led-radiology-execution-boundary.md"
SCHEMA = ROOT / "static" / "schemas" / "ai-led-radiology-execution-case.schema.json"
SIDEBAR = ROOT / "sidebars.js"
INDEX = ROOT / "docs" / "formalisms" / "index.md"

PUBLIC_PATHS = (
    "formalisms/ai-led-radiology-execution-boundary",
    "schemas/ai-led-radiology-execution-case.schema.json",
    "status/ai-led-radiology-execution-status.json",
)


def check_url(url: str) -> str | None:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.status != 200:
                return f"{url}: HTTP {response.status}"
    except (urllib.error.URLError, TimeoutError) as exc:
        return f"{url}: {exc}"
    return None


def main() -> int:
    failures: list[str] = []
    for path in (STATUS, FORMALISM, SCHEMA, SIDEBAR, INDEX):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if not failures:
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        if status.get("manual_task_requirement") != "NONE":
            failures.append("status must declare manual_task_requirement NONE")
        if status.get("user_manual_action_required") is not False:
            failures.append("status must declare user_manual_action_required false")

        sidebar = SIDEBAR.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        slug = "formalisms/ai-led-radiology-execution-boundary"
        if slug not in sidebar:
            failures.append("formalism missing from sidebar")
        if "AI-Led Radiology Execution-Boundary Admissibility" not in index:
            failures.append("formalism missing from index")

    base_url = os.environ.get("AI_RADIOLOGY_PUBLIC_BASE_URL", "").rstrip("/")
    live_results: list[dict[str, str]] = []
    if base_url:
        for relative in PUBLIC_PATHS:
            url = f"{base_url}/{relative}"
            error = check_url(url)
            live_results.append({"url": url, "result": "PASS" if error is None else "FAIL"})
            if error:
                failures.append(error)

    result = {
        "validator": "check_ai_led_radiology_publication.py",
        "result": "FAIL" if failures else "PASS",
        "local_surfaces_checked": 5,
        "live_verification_enabled": bool(base_url),
        "live_results": live_results,
        "manual_action_required": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    if failures:
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
