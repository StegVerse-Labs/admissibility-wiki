#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "static" / "status" / "conceptual-inheritance-propagation-plan.json"

EXPECTED_DESTINATIONS = {
    "StegVerse-Labs/Site",
    "GCAT-BCAT-Engine/Publisher",
    "StegVerse-002/stegguardian-wiki",
    "StegVerse-002/StegGuardian",
}
ALLOWED_ACTIONS = {"DEFER", "QUEUE_AFTER_CURRENT_PRIORITY"}
REQUIRED_PROHIBITIONS = {
    "Queued propagation is not completed propagation",
    "Public visibility is not execution authority",
    "A destination reference does not grant mutation authority",
    "This plan does not supersede any destination handoff",
}


def main() -> int:
    failures: list[str] = []
    if not PLAN.exists():
        failures.append("missing conceptual inheritance propagation plan")
    else:
        try:
            data = json.loads(PLAN.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid propagation plan: {exc}")
            data = {}

        if data.get("goal_id") != "conceptual-inheritance-provenance-standing":
            failures.append("unexpected goal_id")
        if data.get("source_repository") != "StegVerse-Labs/admissibility-wiki":
            failures.append("unexpected source_repository")
        if data.get("authority_posture") != "QUEUE_ONLY_NO_DOWNSTREAM_MUTATION":
            failures.append("authority posture must remain queue-only")
        if data.get("manual_task_required") is not False:
            failures.append("manual_task_required must remain false")

        destinations = data.get("destinations", [])
        repos = {item.get("repository") for item in destinations if isinstance(item, dict)}
        if repos != EXPECTED_DESTINATIONS:
            failures.append("destination set is incomplete or unexpected")
        for item in destinations:
            if not isinstance(item, dict):
                failures.append("destination entry must be an object")
                continue
            if item.get("action") not in ALLOWED_ACTIONS:
                failures.append(f"unauthorized propagation action for {item.get('repository')}")
            if not item.get("handoff"):
                failures.append(f"missing handoff for {item.get('repository')}")
            if not item.get("reason"):
                failures.append(f"missing reason for {item.get('repository')}")

        prohibitions = set(data.get("prohibited_claims", []))
        if not REQUIRED_PROHIBITIONS.issubset(prohibitions):
            failures.append("propagation boundary prohibitions are incomplete")

        prerequisites = set(data.get("prerequisites", []))
        if "canonical workflow pass in StegVerse-Labs/admissibility-wiki" not in prerequisites:
            failures.append("canonical validation prerequisite missing")
        if "destination mirror handoff reviewed immediately before mutation" not in prerequisites:
            failures.append("destination handoff prerequisite missing")

    if failures:
        print("CONCEPTUAL INHERITANCE PROPAGATION PLAN: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONCEPTUAL INHERITANCE PROPAGATION PLAN: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
