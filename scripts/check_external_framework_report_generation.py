#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_external_framework_reports.py"
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
REPORT_DIR = ROOT / "docs" / "external-frameworks" / "reports"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_external_framework_reports", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [GENERATOR, REGISTRY, REPORT_DIR]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK REPORT GENERATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    generator = load_generator()
    registry = read_json(REGISTRY)

    for entry in registry.get("entries", []):
        framework_id = entry.get("framework_id")
        manifest_path = entry.get("manifest_path")
        if not isinstance(framework_id, str):
            failures.append("entry missing framework id")
            continue
        if not isinstance(manifest_path, str):
            failures.append(f"entry missing manifest path: {framework_id}")
            continue

        manifest_file = ROOT / manifest_path
        report_file = REPORT_DIR / f"{framework_id}.compatibility.json"
        if not manifest_file.exists():
            failures.append(f"missing manifest: {manifest_path}")
            continue
        if not report_file.exists():
            failures.append(f"missing generated report: {framework_id}")
            continue

        manifest = read_json(manifest_file)
        expected = generator.build_report(entry, manifest)
        actual = read_json(report_file)
        if actual != expected:
            failures.append(f"report not reproducible: {report_file.relative_to(ROOT)}")

    print("EXTERNAL FRAMEWORK REPORT GENERATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
