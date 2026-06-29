#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_external_framework_results.py"
RESULTS = ROOT / "docs" / "external-frameworks" / "evaluation-results.md"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_external_framework_results", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        failures.append("results generator missing")
    if not RESULTS.exists():
        failures.append("evaluation results page missing")
    if failures:
        print("EXTERNAL FRAMEWORK RESULTS PAGE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    before = RESULTS.read_text(encoding="utf-8")
    generator = load_generator()
    generator.main()
    after = RESULTS.read_text(encoding="utf-8")
    if before != after:
        RESULTS.write_text(before, encoding="utf-8")
        failures.append("evaluation results page is not generated-current")

    print("EXTERNAL FRAMEWORK RESULTS PAGE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
