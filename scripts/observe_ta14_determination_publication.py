#!/usr/bin/env python3
"""Observe TA-14 determination publication without halting unrelated development."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/external-frameworks/ta-14-testing-support-determination-2026-08-01.md"
CANONICAL_WORKFLOW = ROOT / ".github/workflows/validate-chain-continuation.yml"
REPORT = ROOT / "reports/ta14-determination-publication-observation.json"
PUBLIC_URL = os.environ.get(
    "TA14_DETERMINATION_PUBLIC_URL",
    "https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/ta-14-testing-support-determination-2026-08-01",
)


def active_workflows() -> list[str]:
    workflow_dir = ROOT / ".github/workflows"
    if not workflow_dir.exists():
        return []
    return sorted(str(path.relative_to(ROOT)) for path in workflow_dir.glob("*.y*ml"))


def observe_public_url() -> tuple[str, int | None, str]:
    # Observation is active by default. Set TA14_OBSERVE_PUBLIC_NETWORK=false only
    # in an intentionally offline environment. Network failure remains continuable.
    if os.environ.get("TA14_OBSERVE_PUBLIC_NETWORK", "true").lower() != "true":
        return "NOT_OBSERVED_CONTINUABLE", None, "Network observation was explicitly disabled for this execution."
    try:
        request = urllib.request.Request(PUBLIC_URL, headers={"User-Agent": "StegVerse-publication-observer/1.1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(250000).decode("utf-8", errors="replace")
            code = response.getcode()
        title_present = "TA-14 Testing Support Determination" in body
        decision_present = "FURTHER PUBLIC-DEMO TESTING AND EVALUATION NOT SUPPORTED" in body
        if code == 200 and title_present and decision_present:
            return "PASS_PUBLIC_CONTENT_VERIFIED", code, "Expected title and determination were found."
        return "NOT_OBSERVED_CONTINUABLE", code, "Route responded but expected determination content was not established."
    except urllib.error.HTTPError as exc:
        return "NOT_OBSERVED_CONTINUABLE", exc.code, f"HTTP error: {exc}"
    except Exception as exc:
        return "NOT_OBSERVED_CONTINUABLE", None, f"Observation error: {exc}"


def main() -> int:
    workflows = active_workflows()
    structural_errors: list[str] = []
    if not SOURCE.exists():
        structural_errors.append(str(SOURCE.relative_to(ROOT)))
    if not CANONICAL_WORKFLOW.exists():
        structural_errors.append(str(CANONICAL_WORKFLOW.relative_to(ROOT)))
    if workflows != [".github/workflows/validate-chain-continuation.yml"]:
        structural_errors.append(f"single-workflow policy violated: {workflows}")

    public_state, http_status, detail = observe_public_url()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "ta14-determination-publication-observation.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "task_id": "PA-INT-010",
        "source": str(SOURCE.relative_to(ROOT)),
        "canonical_workflow": str(CANONICAL_WORKFLOW.relative_to(ROOT)),
        "active_workflows": workflows,
        "public_url": PUBLIC_URL,
        "public_state": public_state,
        "http_status": http_status,
        "detail": detail,
        "structural_state": "PASS_INTERNAL" if not structural_errors else "FAIL_INTERNAL_CONTINUABLE",
        "structural_errors": structural_errors,
        "development_policy": {
            "external_tasks_exist": False,
            "public_route_not_observed_blocks_unrelated_development": False,
            "deployment_claim_requires_content_verification": True,
            "network_observation_active_by_default": True
        },
        "authority_boundary": {
            "source_present_is_deployment_proof": False,
            "http_200_without_expected_content_is_publication_proof": False,
            "internal_observation_is_external_validation": False
        }
    }
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if structural_errors:
        print("TA-14 PUBLICATION OBSERVER: FAIL_INTERNAL_CONTINUABLE")
        for error in structural_errors:
            print(f"- {error}")
        return 1
    print(f"TA-14 PUBLICATION OBSERVER: {public_state}")
    print(f"Report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
