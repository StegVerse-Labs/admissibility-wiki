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
WORKFLOW_MANIFEST = ROOT / "workflow_manifest.json"


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

    for path in [GENERATOR, REGISTRY, REPORT_DIR, WORKFLOW_MANIFEST]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    if failures:
        print("EXTERNAL FRAMEWORK REPORT GENERATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    generator = load_generator()
    registry = read_json(REGISTRY)
    workflow_manifest = read_json(WORKFLOW_MANIFEST)
    recorded_reports = {
        path for path in workflow_manifest.get("generated_reports", [])
        if isinstance(path, str) and path.startswith("docs/external-frameworks/reports/")
    }

    for entry in registry.get("entries", []):
        manifest_path = entry.get("manifest_path")
        if not isinstance(manifest_path, str):
            failures.append(f"entry missing manifest path: {entry.get('framework_id')}")
            continue
        manifest_file = ROOT / manifest_path
        if not manifest_file.exists():
            failures.append(f"missing manifest: {manifest_path}")
            continue

        manifest = read_json(manifest_file)
        expected = generator.build_report(entry, manifest)
        if expected.get("framework_id") != entry.get("framework_id"):
            failures.append(f"generated report framework mismatch: {entry.get('framework_id')}")
        if expected.get("framework_manifest") != manifest_path:
            failures.append(f"generated report manifest mismatch: {entry.get('framework_id')}")

    for report in sorted(recorded_reports):
        report_path = ROOT / report
        if not report_path.exists():
            failures.append(f"missing recorded report: {report}")
            continue
        actual = read_json(report_path)
        framework_id = actual.get("framework_id")
        entry = next((item for item in registry.get("entries", []) if item.get("framework_id") == framework_id), None)
        if entry is None:
            failures.append(f"recorded report has unknown framework id: {framework_id}")
            continue
        manifest = read_json(ROOT / entry["manifest_path"])
        expected = generator.build_report(entry, manifest)
        if actual != expected:
            failures.append(f"recorded report not reproducible: {report}")

    print("EXTERNAL FRAMEWORK REPORT GENERATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
