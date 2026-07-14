#!/usr/bin/env python3
"""Validate the denial-reachability commit-boundary documentation surface."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/formalisms/denial-reachability-at-commit.md"
MANIFEST = ROOT / "static/formalisms/denial-reachability-at-commit.v0.1.json"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    require(DOC.is_file(), f"missing {DOC.relative_to(ROOT)}")
    require(MANIFEST.is_file(), f"missing {MANIFEST.relative_to(ROOT)}")

    doc = DOC.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    required_doc_terms = (
        "denial remains reachable and enforceable",
        "Authorization without a reachable refusal path",
        "INHERITED_AUTHORIZATION",
        "FAIL_CLOSED",
        "Post-hoc cancellation",
    )
    for term in required_doc_terms:
        require(term in doc, f"documentation missing required term: {term}")

    require(
        "formalisms/denial-reachability-at-commit" in sidebar,
        "formalism is not registered in sidebars.js",
    )
    require(
        "Denial reachability at the commit boundary" in handoff,
        "handoff does not preserve the installed formalism",
    )

    require(data.get("schema_version") == "0.1", "unexpected schema_version")
    require(
        data.get("formalism_id") == "stegverse.denial-reachability-at-commit.v0.1",
        "unexpected formalism_id",
    )
    require(
        data.get("authority_posture") == "NON_EXECUTION_AUTHORITY",
        "authority posture must remain non-execution authority",
    )

    predicates = set(data.get("required_predicates", []))
    require(
        {"ADMISSIBLE", "AUTHORITY_CURRENT", "STATE_SUFFICIENT", "DENIAL_REACHABLE", "DENIAL_ENFORCEABLE"}
        <= predicates,
        "required commit-boundary predicates are incomplete",
    )

    failure = data.get("failure_posture", {})
    require(failure.get("decision") == "FAIL_CLOSED", "failure decision must fail closed")
    require(
        failure.get("primary_failure_class") == "INHERITED_AUTHORIZATION",
        "primary failure class must be inherited authorization",
    )

    evidence = set(data.get("evidence_requirements", []))
    require(
        {"reachable_deny_path", "deny_enforcement_mechanism", "execution_control_receipt"}
        <= evidence,
        "denial reachability evidence requirements are incomplete",
    )

    print("PASS: denial reachability at commit boundary is documented and registered")


if __name__ == "__main__":
    main()
