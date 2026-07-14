#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "static" / "translation-records" / "external-bibliographic-intake.v0.1.json"
LOCATORS = ROOT / "static" / "translation-records" / "source-locator-intake.v0.1.json"
ROUTING = ROOT / "static" / "translation-records" / "specialist-review-routing.v0.1.json"

ALLOWED_LOCATOR_RESULTS = {"CONFIRMED", "PARTIAL", "UNRESOLVED", "CONFLICTING", "REJECTED"}
ALLOWED_ROUTE_RESULTS = {"MAP", "ACCEPT", "DEFER", "DISPUTE", "ESCALATE", "REFUSE", "SUPERSEDE"}


def fail(message: str) -> None:
    raise SystemExit(f"SOURCE LOCATOR AND SPECIALIST ROUTING: FAIL - {message}")


def main() -> None:
    for path in (BIB, LOCATORS, ROUTING):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    bib = json.loads(BIB.read_text(encoding="utf-8"))
    known_bib = {record["bibliographic_id"] for record in bib.get("records", [])}
    known_sources = {record["source_id"] for record in bib.get("records", [])}

    locator_data = json.loads(LOCATORS.read_text(encoding="utf-8"))
    declared_results = set(locator_data.get("allowed_verification_results", []))
    if declared_results != ALLOWED_LOCATOR_RESULTS:
        fail("locator result set is incomplete or changed")

    locator_ids: set[str] = set()
    for record in locator_data.get("records", []):
        locator_id = record.get("locator_intake_id")
        if not locator_id or locator_id in locator_ids:
            fail("locator IDs must be present and unique")
        locator_ids.add(locator_id)
        if record.get("bibliographic_id") not in known_bib:
            fail(f"locator {locator_id} references unknown bibliographic record")
        if record.get("source_id") not in known_sources:
            fail(f"locator {locator_id} references unknown source")
        if record.get("verification_result") not in ALLOWED_LOCATOR_RESULTS:
            fail(f"locator {locator_id} has invalid verification result")
        if "not" not in str(record.get("non_claims", "")).lower():
            fail(f"locator {locator_id} lacks an explicit non-claim")

    routing_data = json.loads(ROUTING.read_text(encoding="utf-8"))
    review_classes = {item["review_class"] for item in routing_data.get("review_classes", [])}
    if not review_classes:
        fail("no specialist review classes declared")

    route_ids: set[str] = set()
    for route in routing_data.get("routes", []):
        route_id = route.get("route_id")
        if not route_id or route_id in route_ids:
            fail("route IDs must be present and unique")
        route_ids.add(route_id)
        if route.get("bibliographic_id") not in known_bib:
            fail(f"route {route_id} references unknown bibliographic record")
        if route.get("source_id") not in known_sources:
            fail(f"route {route_id} references unknown source")
        if route.get("locator_intake_id") not in locator_ids:
            fail(f"route {route_id} references unknown locator intake")
        required = route.get("required_review_classes")
        if not isinstance(required, list) or not required:
            fail(f"route {route_id} requires at least one specialist class")
        unknown = set(required) - review_classes
        if unknown:
            fail(f"route {route_id} references unknown review classes: {sorted(unknown)}")
        if route.get("current_result") not in ALLOWED_ROUTE_RESULTS:
            fail(f"route {route_id} has invalid current result")
        if not str(route.get("re_evaluation_trigger", "")).strip():
            fail(f"route {route_id} lacks a re-evaluation trigger")
        if "not" not in str(route.get("non_claims", "")).lower():
            fail(f"route {route_id} lacks an explicit non-claim")

    print(f"SOURCE LOCATOR AND SPECIALIST ROUTING: PASS - {len(locator_ids)} locators and {len(route_ids)} routes validated")


if __name__ == "__main__":
    main()
