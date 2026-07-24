#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "exports" / "site" / "asro-reciprocal-projection-bundle.json"


def main() -> int:
    failures: list[str] = []
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))

    if bundle.get("state") != "QUEUED_NON_COLLIDING_NO_DESTINATION_MUTATION":
        failures.append("projection bundle must remain queued")
    review = bundle.get("destination_handoff_review", {})
    if review.get("path") != "docs/SITE_MIRROR_HANDOFF.md":
        failures.append("Site handoff reference missing")
    if review.get("projection_authorized_now") is not False:
        failures.append("bundle may not infer Site mutation authority")
    if bundle.get("destination_repository") != "StegVerse-Labs/Site":
        failures.append("unexpected destination repository")

    artifacts = bundle.get("source_artifacts", [])
    required_sources = {
        "docs/external-frameworks/asro.md",
        "static/status/reciprocal-framework-evaluation-status.json",
        "static/data/framework-evaluations/asro.json",
        "static/data/framework-evaluations/test-cases/asro-declared-reference-membership-v1.json",
        "static/data/framework-evaluations/runs/asro-declared-reference-membership-v1-stegverse-run-001.jsonl",
        "receipts/asro-bounded-comparison-run-001.json",
    }
    found_sources = {item.get("source_path") for item in artifacts}
    for source in required_sources:
        if source not in found_sources:
            failures.append(f"missing projection source: {source}")
        elif not (ROOT / source).exists():
            failures.append(f"projection source does not exist: {source}")

    for key, value in bundle.get("authority", {}).items():
        if value is not False:
            failures.append(f"projection authority escalation: {key}")
    if bundle.get("user_manual_action_required") is not False:
        failures.append("projection queue must not create a user task")

    required_behavior = " ".join(bundle.get("required_destination_behavior", []))
    for marker in (
        "NOT_TESTED",
        "reviewer issuer as unresolved",
        "separate results",
    ):
        if marker not in required_behavior:
            failures.append(f"destination behavior missing marker: {marker}")

    if failures:
        print("ASRO SITE PROJECTION BUNDLE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ASRO SITE PROJECTION BUNDLE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
