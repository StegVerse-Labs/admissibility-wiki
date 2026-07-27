#!/usr/bin/env python3
"""Observe deployed ArquivoNulo routes and emit a bounded publication report."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "arquivonulo-public-route-observation.json"
BASE_URL = os.environ.get(
    "ADMISSIBILITY_WIKI_PUBLIC_BASE_URL",
    "https://stegverse-labs.github.io/admissibility-wiki",
).rstrip("/")
TIMEOUT = float(os.environ.get("PUBLIC_ROUTE_TIMEOUT_SECONDS", "20"))

ROUTES = (
    {
        "id": "doctrine_page",
        "path": "/external-frameworks/arquivonulo",
        "content_type_contains": "text/html",
        "markers": (
            "ArquivoNulo",
            "valid proof",
            "continuing admissibility",
            "PUBLICLY_UNRESOLVED",
        ),
    },
    {
        "id": "evaluation_json",
        "path": "/data/framework-evaluations/arquivonulo.json",
        "content_type_contains": "application/json",
        "markers": (
            '"framework_id": "arquivonulo"',
            '"status": "PUBLICLY_UNRESOLVED"',
            '"commit_bound_prevention_demonstrated": false',
        ),
    },
    {
        "id": "status_json",
        "path": "/status/arquivonulo-execution-boundary-status.json",
        "content_type_contains": "application/json",
        "markers": (
            '"goal_id": "arquivonulo-execution-boundary-evaluation"',
            '"canonical_validation_observed": false',
            '"activation_receipt_closed": false',
        ),
    },
)


def observe(route: dict[str, object]) -> dict[str, object]:
    url = BASE_URL + str(route["path"])
    result: dict[str, object] = {
        "id": route["id"],
        "url": url,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "http_status": None,
        "content_type": None,
        "required_markers_present": False,
        "success": False,
        "error": None,
    }
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "StegVerse-public-route-check/1.0"})
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            result["http_status"] = response.status
            result["content_type"] = content_type
            markers_present = all(str(marker) in body for marker in route["markers"])
            type_ok = str(route["content_type_contains"]) in content_type
            result["required_markers_present"] = markers_present
            result["success"] = response.status == 200 and type_ok and markers_present
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> int:
    observations = [observe(route) for route in ROUTES]
    complete = all(item["success"] is True for item in observations)
    payload = {
        "schema_version": "1.0.0",
        "goal_id": "arquivonulo-execution-boundary-evaluation",
        "base_url": BASE_URL,
        "state": "WORKFLOW_OBSERVED_PUBLICATION_COMPLETE" if complete else "PUBLIC_ROUTE_OBSERVATION_FAIL_CLOSED",
        "observations": observations,
        "publication_boundary": "Publication verifies route availability and bounded content only; it does not establish continuing admissibility, certification, execution authority, or live ArquivoNulo capability.",
        "authority": {
            "certification": False,
            "endorsement": False,
            "execution": False,
            "custody": False,
            "integration": False,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
