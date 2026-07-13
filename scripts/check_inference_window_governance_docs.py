#!/usr/bin/env python3
"""Validate the inference-window governance documentation and activation mesh."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMALISM = ROOT / "docs/formalisms/inference-window-irreversibility-governance.md"
LIFECYCLE = ROOT / "docs/formalisms/governed-action-lifecycle.md"
IICT = ROOT / "docs/formalisms/irreversibility-inference-convergence-theorem.md"
INDEX = ROOT / "docs/formalisms/index.md"
SIDEBAR = ROOT / "sidebars.js"
STATUS = ROOT / "static/status/inference-window-governance-status.json"
SCHEMA = ROOT / "static/schemas/inference-window-governance.schema.json"
CASES = ROOT / "static/examples/inference-window-governance.worked-cases.json"
VALIDATOR = ROOT / "scripts/validate_inference_window_governance.py"
TESTS = ROOT / "tests/test_inference_window_governance.py"


def require(path: Path, phrases: list[str], failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return
    body = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in body:
            failures.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")


def main() -> int:
    failures: list[str] = []

    require(
        FORMALISM,
        [
            "Governance is not the elimination of error",
            "ValidAt(t_0) \\not\\Rightarrow ValidAt(t_c)",
            "governed-action-lifecycle.md",
            "irreversibility-inference-convergence-theorem.md",
            "ALLOW, DENY, DEFER, ESCALATE",
        ],
        failures,
    )
    require(
        LIFECYCLE,
        [
            "proposal",
            "commit-time revalidation",
            "bounded execution",
            "consequence observation",
            "recovery, correction, or accountability",
            "reconstruction",
            "inference-window-irreversibility-governance.md",
            "irreversibility-inference-convergence-theorem.md",
        ],
        failures,
    )
    require(
        IICT,
        [
            "theorem candidate",
            "inference-window-irreversibility-governance.md",
            "governed-action-lifecycle.md",
            "A passing inference-window validator does not prove IICT",
        ],
        failures,
    )
    require(
        INDEX,
        [
            "Inference-Window and Irreversibility-Bounded Governance",
            "Governed Action Lifecycle",
            "Irreversibility-Inference Convergence Theorem",
        ],
        failures,
    )
    require(
        SIDEBAR,
        [
            "formalisms/inference-window-irreversibility-governance",
            "formalisms/governed-action-lifecycle",
            "formalisms/irreversibility-inference-convergence-theorem",
        ],
        failures,
    )

    for path in [SCHEMA, CASES, VALIDATOR, TESTS]:
        if not path.exists():
            failures.append(f"missing canonical artifact: {path.relative_to(ROOT)}")

    if STATUS.exists():
        try:
            status = json.loads(STATUS.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"invalid status JSON: {exc}")
        else:
            artifacts = status.get("canonical_artifacts", {})
            expected = {
                "formalism": "docs/formalisms/inference-window-irreversibility-governance.md",
                "lifecycle": "docs/formalisms/governed-action-lifecycle.md",
                "iict_relationship": "docs/formalisms/irreversibility-inference-convergence-theorem.md",
                "schema": "static/schemas/inference-window-governance.schema.json",
                "worked_cases": "static/examples/inference-window-governance.worked-cases.json",
                "validator": "scripts/validate_inference_window_governance.py",
                "tests": "tests/test_inference_window_governance.py",
            }
            for key, value in expected.items():
                if artifacts.get(key) != value:
                    failures.append(f"status canonical_artifacts.{key} mismatch")
            if status.get("claims_boundary", {}).get("guarantees_correctness") is not False:
                failures.append("status must not claim guaranteed correctness")
    else:
        failures.append("missing status JSON")

    print("INFERENCE WINDOW GOVERNANCE DOCS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
