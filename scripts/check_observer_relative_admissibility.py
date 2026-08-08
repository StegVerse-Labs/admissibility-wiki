#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTRINE = ROOT / "docs" / "governance" / "observer-relative-admissibility.md"
STATUS = ROOT / "static" / "status" / "observer-relative-admissibility-status.json"
HANDOFF = ROOT / "docs" / "OBSERVER_RELATIVE_ADMISSIBILITY_MIRROR_HANDOFF.md"

DOCTRINE_MARKERS = (
    "transition facts != observer characterization",
    "capability demonstrated != malicious intent",
    "test authorization != production authorization",
    "one committed outcome != one observer point of view",
    "observer_id",
    "authority_scope",
    "admissibility_result",
    "characterization",
    "Authorized adversarial or capability testing",
    "Crossing the authorized test boundary is a new transition",
    "A_i(T)",
)

STATUS_TRUE = (
    "transition_facts_separate_from_characterization",
    "observer_context_required",
    "authority_scope_required",
    "evaluation_context_may_change_admissibility",
    "production_context_may_change_admissibility",
    "historical_transition_is_not_mutated_by_contest",
    "future_constraints_may_change_from_contest_evidence",
    "single_committed_outcome_does_not_imply_single_observer_pov",
)

STATUS_FALSE = (
    "test_authorization_is_production_authorization",
    "capability_demonstration_is_malicious_intent",
    "observer_label_is_transition_fact",
    "doctrine_publication_grants_execution_authority",
)

HANDOFF_MARKERS = (
    "OBSERVER-RELATIVE-ADMISSIBILITY-001",
    "docs/governance/observer-relative-admissibility.md",
    "scripts/check_observer_relative_admissibility.py",
    "MERGED INTO: StegVerse-Labs/admissibility-wiki",
)


def main() -> int:
    failures: list[str] = []

    if not DOCTRINE.exists():
        failures.append(f"missing {DOCTRINE.relative_to(ROOT)}")
    else:
        text = DOCTRINE.read_text(encoding="utf-8")
        for marker in DOCTRINE_MARKERS:
            if marker not in text:
                failures.append(f"doctrine missing marker: {marker}")

    if not STATUS.exists():
        failures.append(f"missing {STATUS.relative_to(ROOT)}")
    else:
        try:
            data = json.loads(STATUS.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"status JSON invalid: {exc}")
            data = {}
        if data.get("schema") != "admissibility_wiki.observer_relative_admissibility_status.v1":
            failures.append("status schema mismatch")
        if data.get("goal_id") != "OBSERVER-RELATIVE-ADMISSIBILITY-001":
            failures.append("status goal_id mismatch")
        req = data.get("requirements", {})
        for key in STATUS_TRUE:
            if req.get(key) is not True:
                failures.append(f"requirement not true: {key}")
        boundaries = data.get("authority_boundaries", {})
        for key in STATUS_FALSE:
            if boundaries.get(key) is not False:
                failures.append(f"authority boundary not false: {key}")
        validation = data.get("validation", {})
        if validation.get("canonical_parent") != "scripts/check_admissibility_automation_handoff.py":
            failures.append("canonical parent mismatch")

    if not HANDOFF.exists():
        failures.append(f"missing {HANDOFF.relative_to(ROOT)}")
    else:
        text = HANDOFF.read_text(encoding="utf-8")
        for marker in HANDOFF_MARKERS:
            if marker not in text:
                failures.append(f"handoff missing marker: {marker}")

    if failures:
        print("OBSERVER-RELATIVE ADMISSIBILITY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OBSERVER-RELATIVE ADMISSIBILITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
