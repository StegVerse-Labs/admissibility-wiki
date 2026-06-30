#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_generated_page_closeout_state.py"
STATE_MODEL_CHECK = ROOT / "scripts" / "check_generated_page_state_model.py"
SUMMARY = ROOT / "docs" / "external-frameworks" / "generated-page-validation-summary.json"
GENERATED_FILES = [
    ROOT / "docs" / "external-frameworks" / "generated-page-validation-summary.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-progress.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-release-readiness.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-downstream-tasks.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-ci-evidence-request.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-tag-candidate.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-closeout-bundle.json",
    ROOT / "docs" / "external-frameworks" / "generated-page-activation-gate.json",
]


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_generated_page_closeout_state", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load closeout-state generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if path.exists():
        result = subprocess.run(["python", str(path)], check=False)
        if result.returncode != 0:
            failures.append(f"{label} failed")


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        print("GENERATED PAGE VALIDATION SUMMARY GENERATION: FAIL")
        print("- generator missing")
        return 1
    if not SUMMARY.exists():
        print("GENERATED PAGE VALIDATION SUMMARY GENERATION: FAIL")
        print("- validation summary missing")
        return 1

    run_check(STATE_MODEL_CHECK, "state model check", failures)

    before = {path: path.read_text(encoding="utf-8") if path.exists() else None for path in GENERATED_FILES}
    load_generator().main()
    after = {path: path.read_text(encoding="utf-8") if path.exists() else None for path in GENERATED_FILES}

    for path, text in before.items():
        if text is not None:
            path.write_text(text, encoding="utf-8")

    if before[SUMMARY] != after[SUMMARY]:
        failures.append("validation summary is not current with state-model closeout generator")

    print("GENERATED PAGE VALIDATION SUMMARY GENERATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
