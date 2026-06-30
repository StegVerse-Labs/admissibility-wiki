#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_generated_page_closeout_state.py"
OUT = ROOT / "docs" / "external-frameworks"
FILES = [
    "generated-page-progress.json",
    "generated-page-release-readiness.json",
    "generated-page-downstream-tasks.json",
    "generated-page-ci-evidence-request.json",
    "generated-page-tag-candidate.json",
    "generated-page-closeout-bundle.json",
]


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_generated_page_closeout_state", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load closeout-state generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        print("GENERATED PAGE CLOSEOUT STATE GENERATION: FAIL")
        print("- generator missing")
        return 1

    paths = [OUT / name for name in FILES]
    before = {path: path.read_text(encoding="utf-8") if path.exists() else None for path in paths}
    load_generator().main()
    after = {path: path.read_text(encoding="utf-8") if path.exists() else None for path in paths}

    changed = [path.relative_to(ROOT).as_posix() for path in paths if before[path] != after[path]]
    for path, text in before.items():
        if text is not None:
            path.write_text(text, encoding="utf-8")

    if changed:
        failures.append("generated closeout state is not current: " + ", ".join(changed))

    print("GENERATED PAGE CLOSEOUT STATE GENERATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
