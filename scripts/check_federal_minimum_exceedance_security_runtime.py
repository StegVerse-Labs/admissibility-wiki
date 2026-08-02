#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "static" / "security" / "federal-minimum-exceedance-security-profile.json"
VALIDATOR = ROOT / "scripts" / "check_federal_minimum_exceedance_security.py"


def run_validator() -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.rstrip()


def main() -> int:
    failures: list[str] = []
    if not PROFILE.exists() or not VALIDATOR.exists():
        print("FEDERAL MINIMUM EXCEEDANCE SECURITY RUNTIME: FAIL")
        print("- missing profile or validator")
        return 1

    original_text = PROFILE.read_text(encoding="utf-8")
    original = json.loads(original_text)

    try:
        code, output = run_validator()
        print(output)
        if code != 0:
            failures.append("valid profile did not pass")

        cases = [
            ("federal floor removal", lambda p: p.__setitem__("federal_floor", p["federal_floor"][:-1])),
            ("exceedance control downgrade", lambda p: p["exceedance_controls"].__setitem__("deny_by_default", False)),
            ("unsupported certification claim", lambda p: p["claims"].__setitem__("fedramp_authorized", True)),
            ("missing-evidence success inference", lambda p: p["prohibited_inferences"].__setitem__("missing_evidence_implies_success", True)),
            ("canonical workflow displacement", lambda p: p["owner"].__setitem__("workflow", ".github/workflows/alternate.yml")),
            ("cross-repository authority escalation", lambda p: p.__setitem__("cross_repository_mutation_authority_granted", True)),
        ]

        for label, mutate in cases:
            candidate = deepcopy(original)
            mutate(candidate)
            PROFILE.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
            code, output = run_validator()
            print(f"\n--- {label} ---")
            print(output)
            if code == 0:
                failures.append(f"negative case incorrectly passed: {label}")
    finally:
        PROFILE.write_text(original_text, encoding="utf-8")

    restore_code, restore_output = run_validator()
    print("\n--- restored profile ---")
    print(restore_output)
    if restore_code != 0:
        failures.append("restored profile did not pass")

    if failures:
        print("FEDERAL MINIMUM EXCEEDANCE SECURITY RUNTIME: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("FEDERAL MINIMUM EXCEEDANCE SECURITY RUNTIME: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
