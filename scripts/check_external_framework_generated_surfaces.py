#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
RESULTS = ROOT / "docs" / "external-frameworks" / "evaluation-results.md"
STATUS_START = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:START -->"
STATUS_END = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:END -->"
REQUIRED_STATUS_LABELS = [
    "- Evidence class:",
    "- Independently reproducible:",
    "- Comparative-testing claim allowed:",
    "- Missing reproducibility gates:",
    "- Evaluation result:",
    "- Cycle status:",
    "- Execution authority claim:",
    "- Next bounded action:",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    if not REGISTRY.exists():
        failures.append("missing canonical registry")
    if not RESULTS.exists():
        failures.append("missing generated evaluation results")
    if failures:
        print("EXTERNAL FRAMEWORK GENERATED SURFACES: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    registry = read_json(REGISTRY)
    entries = registry.get("entries", [])
    if not isinstance(entries, list):
        failures.append("registry entries must be an array")
        entries = []

    results_text = RESULTS.read_text(encoding="utf-8")
    result_ids = re.findall(r"\[report\]\(\./reports/([a-z0-9-]+)\.compatibility\.json\)", results_text)
    registry_ids = [str(entry.get("framework_id", "")) for entry in entries]

    if len(result_ids) != len(registry_ids):
        failures.append(f"evaluation row count mismatch: rows={len(result_ids)} registry={len(registry_ids)}")
    if set(result_ids) != set(registry_ids):
        missing = sorted(set(registry_ids) - set(result_ids))
        extra = sorted(set(result_ids) - set(registry_ids))
        if missing:
            failures.append("evaluation results missing IDs: " + ", ".join(missing))
        if extra:
            failures.append("evaluation results contain unknown IDs: " + ", ".join(extra))
    duplicates = sorted({item for item in result_ids if result_ids.count(item) > 1})
    if duplicates:
        failures.append("duplicate evaluation result rows: " + ", ".join(duplicates))

    if "Current independently reproducible comparative evaluations:" not in results_text:
        failures.append("evaluation results missing reproducible-count disclosure")
    if "compatibility evidence != execution authority" not in results_text:
        failures.append("evaluation results missing authority boundary")

    for entry in entries:
        framework_id = entry.get("framework_id")
        page_path = entry.get("path")
        if not isinstance(framework_id, str) or not isinstance(page_path, str):
            failures.append("registry entry missing framework_id or path")
            continue
        page = ROOT / page_path
        if not page.exists():
            failures.append(f"missing framework page: {framework_id}")
            continue
        text = page.read_text(encoding="utf-8")
        if STATUS_START not in text or STATUS_END not in text:
            failures.append(f"missing generated evaluation status block: {framework_id}")
            continue
        block = text.split(STATUS_START, 1)[1].split(STATUS_END, 1)[0]
        for label in REQUIRED_STATUS_LABELS:
            if label not in block:
                failures.append(f"generated status missing {label} {framework_id}")

    print("EXTERNAL FRAMEWORK GENERATED SURFACES:", "FAIL" if failures else "PASS")
    print(f"registry_records={len(registry_ids)}")
    print(f"evaluation_rows={len(result_ids)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
