#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_GENERATOR = ROOT / "scripts" / "generate_external_framework_results.py"


def load_canonical_generator():
    spec = importlib.util.spec_from_file_location("generate_external_framework_results", CANONICAL_GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load canonical external framework results generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    generator = load_canonical_generator()
    return int(generator.main() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
