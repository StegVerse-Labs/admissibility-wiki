#!/usr/bin/env python3
"""Deterministically validate the reconstruction singularity bounded formalism."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "static/formalisms/reconstruction-singularity.v0.1.json"
CASES_PATH = ROOT / "static/formalisms/fixtures/reconstruction-singularity-cases.v0.1.json"
DOC_PATH = ROOT / "docs/formalisms/reconstruction-singularity.md"


def fail(message: str) -> int:
    print(f"RECONSTRUCTION SINGULARITY: FAIL - {message}")
    return 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (MODEL_PATH, CASES_PATH, DOC_PATH):
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    model = load_json(MODEL_PATH)
    cases = load_json(CASES_PATH)

    if model.get("model_id") != "stegverse.reconstruction-singularity.v0.1":
        return fail("unexpected model_id")
    if cases.get("model_id") != model.get("model_id"):
        return fail("fixture model_id does not match contract")

    predicate = model.get("reconstruction_predicate", {})
    terms = predicate.get("terms")
    if predicate.get("operator") != "ALL" or not isinstance(terms, list) or not terms:
        return fail("reconstruction predicate must be a non-empty ALL predicate")
    if predicate.get("missing_term_result") != "FAIL_CLOSED":
        return fail("missing predicate terms must fail closed")

    authority = model.get("authority", {})
    if not authority or any(value is not False for value in authority.values()):
        return fail("bounded formalism must not infer authority")

    seen_ids: set[str] = set()
    observed_allow = False
    observed_fail_closed = False
    for case in cases.get("cases", []):
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id or case_id in seen_ids:
            return fail("case ids must be unique non-empty strings")
        seen_ids.add(case_id)

        supplied = case.get("predicate")
        if not isinstance(supplied, dict):
            return fail(f"{case_id}: predicate must be an object")
        if set(supplied) != set(terms):
            return fail(f"{case_id}: predicate terms do not exactly match contract")
        if any(not isinstance(supplied[term], bool) for term in terms):
            return fail(f"{case_id}: predicate values must be booleans")

        actual = "RECONSTRUCTION_ADMISSIBLE" if all(supplied[term] for term in terms) else "FAIL_CLOSED"
        expected = case.get("expected_result")
        if actual != expected:
            return fail(f"{case_id}: expected {expected}, calculated {actual}")
        observed_allow = observed_allow or actual == "RECONSTRUCTION_ADMISSIBLE"
        observed_fail_closed = observed_fail_closed or actual == "FAIL_CLOSED"

    if not observed_allow or not observed_fail_closed:
        return fail("fixtures must exercise both admissible and fail-closed branches")

    doc = DOC_PATH.read_text(encoding="utf-8")
    required_doc_terms = (
        "reconstruction is no longer a downstream audit function",
        "procedural memory != governable learning",
        "static/formalisms/reconstruction-singularity.v0.1.json",
        "scripts/check_reconstruction_singularity.py",
    )
    for term in required_doc_terms:
        if term not in doc:
            return fail(f"documentation missing required term: {term}")

    print(
        "RECONSTRUCTION SINGULARITY: PASS - contract, doctrine, admissible branch, "
        f"and fail-closed branches validated ({len(seen_ids)} cases)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
