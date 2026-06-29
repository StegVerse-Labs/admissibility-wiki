#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_external_framework_page_analysis_boundary.py"
FRAMEWORK_DIR = ROOT / "docs" / "external-frameworks"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_external_framework_page_analysis_boundary", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load analysis-boundary generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        failures.append("analysis-boundary generator missing")
    if not FRAMEWORK_DIR.exists():
        failures.append("external framework directory missing")
    if failures:
        print("EXTERNAL FRAMEWORK PAGE ANALYSIS BOUNDARY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    tracked = sorted(FRAMEWORK_DIR.glob("*.md"))
    before = {path: path.read_text(encoding="utf-8") for path in tracked}
    generator = load_generator()
    generator.main()
    after = {path: path.read_text(encoding="utf-8") for path in tracked}
    changed = [path.relative_to(ROOT).as_posix() for path in tracked if before[path] != after[path]]

    for path, text in before.items():
        path.write_text(text, encoding="utf-8")

    if changed:
        failures.append("generated analysis-boundary blocks are not current: " + ", ".join(changed))

    print("EXTERNAL FRAMEWORK PAGE ANALYSIS BOUNDARY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
