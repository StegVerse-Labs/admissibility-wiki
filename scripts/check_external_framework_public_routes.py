#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSOCIATIONS = ROOT / "static" / "external-frameworks" / "sidebar-page-associations.v1.json"
REPORT = ROOT / "reports" / "external-frameworks" / "public-route-verification.json"
DEFAULT_BASE = "https://stegverse-labs.github.io/admissibility-wiki/"
EXPECTED_FRAMEWORK_COUNT = 36


def normalize(text: str) -> str:
    return " ".join(html.unescape(text).split()).strip().lower()


def source_heading(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            frontmatter = text[3:end]
            match = re.search(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$", frontmatter)
            if match:
                return match.group(1).strip().strip("\"'")
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    if match:
        return re.sub(r"[`*_]", "", match.group(1)).strip()
    raise ValueError(f"no frontmatter title or H1 found in {path.relative_to(ROOT)}")


def rendered_text(payload: str) -> str:
    without_scripts = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", payload)
    without_tags = re.sub(r"(?s)<[^>]+>", " ", without_scripts)
    return normalize(without_tags)


def main() -> int:
    failures: list[str] = []
    if not ASSOCIATIONS.exists():
        print("EXTERNAL FRAMEWORK PUBLIC ROUTES: FAIL")
        print(f"- missing {ASSOCIATIONS.relative_to(ROOT)}")
        return 1

    data = json.loads(ASSOCIATIONS.read_text(encoding="utf-8"))
    frameworks = [entry for entry in data.get("entries", []) if entry.get("page_type") == "framework"]
    if len(frameworks) != EXPECTED_FRAMEWORK_COUNT:
        failures.append(f"expected {EXPECTED_FRAMEWORK_COUNT} framework routes, found {len(frameworks)}")

    base = os.environ.get("ADMISSIBILITY_WIKI_PUBLIC_BASE_URL", DEFAULT_BASE).rstrip("/") + "/"
    results: list[dict[str, object]] = []

    for entry in frameworks:
        framework_id = entry.get("framework_id")
        sidebar_route = entry.get("sidebar_route")
        page_path = entry.get("page_path")
        result: dict[str, object] = {
            "framework_id": framework_id,
            "sidebar_route": sidebar_route,
            "page_path": page_path,
            "status_code": None,
            "reachable": False,
            "content_verified": False,
            "expected_heading": None,
            "error": None,
        }
        try:
            if not isinstance(page_path, str) or not (ROOT / page_path).exists():
                raise ValueError(f"source page missing: {page_path}")
            if not isinstance(sidebar_route, str) or not sidebar_route.startswith("external-frameworks/"):
                raise ValueError(f"invalid sidebar route: {sidebar_route}")
            heading = source_heading(ROOT / page_path)
            result["expected_heading"] = heading
            route_suffix = sidebar_route.removeprefix("external-frameworks/")
            url = base + "external-frameworks/" + route_suffix
            request = urllib.request.Request(url, headers={"User-Agent": "admissibility-wiki-route-verifier/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                status = int(response.status)
                payload = response.read().decode("utf-8", errors="replace")
            result["status_code"] = status
            result["reachable"] = status == 200
            text = rendered_text(payload)
            obvious_404 = any(marker in text for marker in ("page not found", "404 | admissibility wiki", "we could not find what you were looking for"))
            heading_present = normalize(heading) in text
            result["content_verified"] = status == 200 and bool(text) and not obvious_404 and heading_present
            if not result["content_verified"]:
                raise ValueError(f"rendered content mismatch: status={status}, heading_present={heading_present}, obvious_404={obvious_404}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError) as exc:
            result["error"] = str(exc)
            failures.append(f"{framework_id}: {exc}")
        results.append(result)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({
        "schema": "admissibility_wiki.external_framework_public_route_verification.v1",
        "base_url": base,
        "expected_framework_routes": EXPECTED_FRAMEWORK_COUNT,
        "observed_framework_routes": len(frameworks),
        "reachable_routes": sum(1 for item in results if item["reachable"] is True),
        "content_verified_routes": sum(1 for item in results if item["content_verified"] is True),
        "overall_status": "FAIL" if failures else "PASS",
        "results": results,
        "authority_boundary": "Route verification proves public reachability and rendered source-heading fidelity only. It does not establish framework compatibility, certification, endorsement, standing, admissibility, release authority, or execution authority."
    }, indent=2) + "\n", encoding="utf-8")

    print("EXTERNAL FRAMEWORK PUBLIC ROUTES:", "FAIL" if failures else "PASS")
    print(f"routes={len(frameworks)}/{EXPECTED_FRAMEWORK_COUNT}")
    print(f"reachable={sum(1 for item in results if item['reachable'] is True)}")
    print(f"content_verified={sum(1 for item in results if item['content_verified'] is True)}")
    print(f"report={REPORT.relative_to(ROOT)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
