#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
PUBLIC_REPORT = ROOT / "reports" / "external-frameworks" / "public-route-verification.json"
SOURCE_REPORT = ROOT / "reports" / "external-frameworks" / "source-route-contract.json"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate External Framework source-route contracts and, unless --source-only is used, deployed route fidelity."
    )
    parser.add_argument(
        "--source-only",
        action="store_true",
        help="Validate all 36 source routes, unique bindings, source pages, and extractable headings without network requests.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    if not ASSOCIATIONS.exists():
        print("EXTERNAL FRAMEWORK ROUTE CONTRACT: FAIL")
        print(f"- missing {ASSOCIATIONS.relative_to(ROOT)}")
        return 1

    data = json.loads(ASSOCIATIONS.read_text(encoding="utf-8"))
    frameworks = [entry for entry in data.get("entries", []) if entry.get("page_type") == "framework"]
    if len(frameworks) != EXPECTED_FRAMEWORK_COUNT:
        failures.append(f"expected {EXPECTED_FRAMEWORK_COUNT} framework routes, found {len(frameworks)}")

    base = os.environ.get("ADMISSIBILITY_WIKI_PUBLIC_BASE_URL", DEFAULT_BASE).rstrip("/") + "/"
    results: list[dict[str, object]] = []
    seen_framework_ids: set[str] = set()
    seen_sidebar_routes: set[str] = set()
    seen_page_paths: set[str] = set()

    for entry in frameworks:
        framework_id = entry.get("framework_id")
        sidebar_route = entry.get("sidebar_route")
        page_path = entry.get("page_path")
        result: dict[str, object] = {
            "framework_id": framework_id,
            "sidebar_route": sidebar_route,
            "page_path": page_path,
            "source_contract_verified": False,
            "status_code": None,
            "reachable": False,
            "content_verified": False,
            "expected_heading": None,
            "error": None,
        }
        try:
            if not isinstance(framework_id, str) or not framework_id:
                raise ValueError(f"invalid framework_id: {framework_id}")
            if framework_id in seen_framework_ids:
                raise ValueError(f"duplicate framework_id: {framework_id}")
            seen_framework_ids.add(framework_id)

            if not isinstance(sidebar_route, str) or not sidebar_route.startswith("external-frameworks/"):
                raise ValueError(f"invalid sidebar route: {sidebar_route}")
            if sidebar_route in seen_sidebar_routes:
                raise ValueError(f"duplicate sidebar route: {sidebar_route}")
            seen_sidebar_routes.add(sidebar_route)

            if not isinstance(page_path, str) or not page_path.startswith("docs/external-frameworks/"):
                raise ValueError(f"invalid framework page path: {page_path}")
            if page_path in seen_page_paths:
                raise ValueError(f"duplicate framework page path: {page_path}")
            seen_page_paths.add(page_path)
            source_path = ROOT / page_path
            if not source_path.exists():
                raise ValueError(f"source page missing: {page_path}")

            heading = source_heading(source_path)
            if not heading.strip():
                raise ValueError(f"empty source heading: {page_path}")
            result["expected_heading"] = heading
            result["source_contract_verified"] = True

            if not args.source_only:
                route_suffix = sidebar_route.removeprefix("external-frameworks/")
                url = base + "external-frameworks/" + route_suffix
                request = urllib.request.Request(url, headers={"User-Agent": "admissibility-wiki-route-verifier/1.1"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    status = int(response.status)
                    payload = response.read().decode("utf-8", errors="replace")
                result["status_code"] = status
                result["reachable"] = status == 200
                text = rendered_text(payload)
                obvious_404 = any(
                    marker in text
                    for marker in (
                        "page not found",
                        "404 | admissibility wiki",
                        "we could not find what you were looking for",
                    )
                )
                heading_present = normalize(heading) in text
                result["content_verified"] = status == 200 and bool(text) and not obvious_404 and heading_present
                if not result["content_verified"]:
                    raise ValueError(
                        f"rendered content mismatch: status={status}, heading_present={heading_present}, obvious_404={obvious_404}"
                    )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError) as exc:
            result["error"] = str(exc)
            failures.append(f"{framework_id}: {exc}")
        results.append(result)

    source_verified = sum(1 for item in results if item["source_contract_verified"] is True)
    reachable = sum(1 for item in results if item["reachable"] is True)
    content_verified = sum(1 for item in results if item["content_verified"] is True)
    report_path = SOURCE_REPORT if args.source_only else PUBLIC_REPORT
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(
            {
                "schema": (
                    "admissibility_wiki.external_framework_source_route_contract.v1"
                    if args.source_only
                    else "admissibility_wiki.external_framework_public_route_verification.v1"
                ),
                "mode": "SOURCE_ONLY" if args.source_only else "DEPLOYED_PUBLIC_ROUTE",
                "base_url": None if args.source_only else base,
                "expected_framework_routes": EXPECTED_FRAMEWORK_COUNT,
                "observed_framework_routes": len(frameworks),
                "source_contract_verified_routes": source_verified,
                "reachable_routes": reachable,
                "content_verified_routes": content_verified,
                "overall_status": "FAIL" if failures else "PASS",
                "results": results,
                "authority_boundary": (
                    "Source-route validation proves deterministic source wiring and extractable content markers only; deployed-route validation additionally proves public reachability and rendered heading fidelity. Neither establishes framework compatibility, certification, endorsement, standing, admissibility, release authority, or execution authority."
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    label = "EXTERNAL FRAMEWORK SOURCE ROUTES" if args.source_only else "EXTERNAL FRAMEWORK PUBLIC ROUTES"
    print(label + ":", "FAIL" if failures else "PASS")
    print(f"routes={len(frameworks)}/{EXPECTED_FRAMEWORK_COUNT}")
    print(f"source_contract_verified={source_verified}")
    if not args.source_only:
        print(f"reachable={reachable}")
        print(f"content_verified={content_verified}")
    print(f"report={report_path.relative_to(ROOT)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
