#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED_RUNNER = ROOT / "scripts" / "run_pinned_opa_ci_capture.py"
CAPTURE_SCRIPT = ROOT / "scripts" / "capture_opa_observation.py"
EXPECTED_VERSION = "1.0.0"
FORBIDDEN = (
    '"version", "--format=json"',
    "'version', '--format=json'",
    "version --format=json",
)


def main() -> int:
    failures: list[str] = []
    sources: dict[str, str] = {}

    for path in (PINNED_RUNNER, CAPTURE_SCRIPT):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
            continue
        source = path.read_text(encoding="utf-8")
        sources[str(path.relative_to(ROOT))] = source
        try:
            ast.parse(source)
        except SyntaxError as exc:
            failures.append(f"{path.relative_to(ROOT)} syntax error: {exc}")

    for label, source in sources.items():
        for forbidden in FORBIDDEN:
            if forbidden in source:
                failures.append(f"{label} contains unsupported OPA version probe: {forbidden}")
        if '"version"' not in source and "'version'" not in source:
            failures.append(f"{label} missing plain OPA version probe")
        if EXPECTED_VERSION not in source:
            failures.append(f"{label} missing pinned version marker {EXPECTED_VERSION}")
        if "version mismatch" not in source:
            failures.append(f"{label} missing fail-closed version mismatch handling")

    pinned = sources.get("scripts/run_pinned_opa_ci_capture.py", "")
    for marker in (
        'OPA_VERSION = "v1.0.0"',
        'run([str(binary), "version"])',
        'OPA_VERSION.removeprefix("v")',
        '"runtime_version_output": version_output',
    ):
        if marker not in pinned:
            failures.append(f"pinned runner missing marker: {marker}")

    capture = sources.get("scripts/capture_opa_observation.py", "")
    for marker in (
        'OPA_VERSION = "1.0.0"',
        'run([str(opa_path), "version"])',
        'version_payload: Any = {"raw": version_output, "version": OPA_VERSION}',
    ):
        if marker not in capture:
            failures.append(f"nested capture script missing marker: {marker}")

    print("OPA VERSION PROBE COMPATIBILITY:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
