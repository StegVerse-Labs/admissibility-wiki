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
BUILD_REPORT = ROOT / "reports" / "external-frameworks" / "built-route-verification.json"
DEFAULT_BASE = "https://stegverse-labs.github.io/admissibility-wiki/"
DEFAULT_BUILD_DIR = ROOT / "build"
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


def content_matches(payload: str, heading: str) -> tuple[bool, bool, bool]:
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
    return bool(text) and not obvious_404 and heading_present, heading_present, obvious_404


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate External Framework source-route contracts, built-site route fidelity, "
            "or deployed public-route fidelity."
        )
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--source-only",
        action="store_true",
        help="Validate all 36 source routes, unique bindings, source pages, and extractable headings without build or network access.",
    )
    modes.add_argument(
        "--built-site",
        action="store_true",
        help="Validate all 36 generated Docusaurus route files and rendered heading fidelity from the local build directory.",
    )
    parser.add_argument(
        "--build-dir",
        default=str(DEFAULT_BUILD_DIR),
        help="Docusaurus build directory used with --built-site (default: build).",
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
    build_dir = Path(args.build_dir)
    if not build_dir.is_absolute():
        build_dir = ROOT / build_dir
    if args.built_site and not build_dir.exists():
        failures.append(f"build directory missing: {build_dir}")

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
            "built_file": None,
            "built_route_verified": False,
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

            route_suffix = sidebar_route.removeprefix("external-frameworks/").strip("/")
            if not route_suffix or ".." in route_suffix.split("/"):
                raise ValueError(f"unsafe or empty route suffix: {route_suffix}")

            if args.built_site:
                built_file = build_dir / "external-frameworks" / route_suffix / "index.html"
                result["built_file"] = str(built_file.relative_to(ROOT)) if built_file.is_relative_to(ROOT) else str(built_file)
                if not built_file.exists():
                    raise ValueError(f"built route file missing: {built_file}")
                payload = built_file.read_text(encoding="utf-8", errors="replace")
                matched, heading_present, obvious_404 = content_matches(payload, heading)
                result["built_route_verified"] = matched
                result["content_verified"] = matched
                if not matched:
                    raise ValueError(
                        f"built content mismatch: heading_present={heading_present}, obvious_404={obvious_404}"
                    )
            elif not args.source_only:
                url = base + "external-frameworks/" + route_suffix
                request = urllib.request.Request(url, headers={"User-Agent": "admissibility-wiki-route-verifier/1.2"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    status = int(response.status)
                    payload = response.read().decode("utf-8", errors="replace")
                result["status_code"] = status
                result["reachable"] = status == 200
                matched, heading_present, obvious_404 = content_matches(payload, heading)
                result["content_verified"] = status == 200 and matched
                if not result["content_verified"]:
                    raise ValueError(
                        f"rendered content mismatch: status={status}, heading_present={heading_present}, obvious_404={obvious_404}"
                    )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError) as exc:
            result["error"] = str(exc)
            failures.append(f"{framework_id}: {exc}")
        results.append(result)

    source_verified = sum(1 for item in results if item["source_contract_verified"] is True)
    built_verified = sum(1 for item in results if item["built_route_verified"] is True)
    reachable = sum(1 for item in results if item["reachable"] is True)
    content_verified = sum(1 for item in results if item["content_verified"] is True)

    if args.source_only:
        mode = "SOURCE_ONLY"
        report_path = SOURCE_REPORT
        schema = "admissibility_wiki.external_framework_source_route_contract.v1"
    elif args.built_site:
        mode = "BUILT_SITE_ROUTE"
        report_path = BUILD_REPORT
        schema = "admissibility_wiki.external_framework_built_route_verification.v1"
    else:
        mode = "DEPLOYED_PUBLIC_ROUTE"
        report_path = PUBLIC_REPORT
        schema = "admissibility_wiki.external_framework_public_route_verification.v1"

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(
            {
                "schema": schema,
                "mode": mode,
                "base_url": base if mode == "DEPLOYED_PUBLIC_ROUTE" else None,
                "build_dir": str(build_dir) if mode == "BUILT_SITE_ROUTE" else None,
                "expected_framework_routes": EXPECTED_FRAMEWORK_COUNT,
                "observed_framework_routes": len(frameworks),
                "source_contract_verified_routes": source_verified,
                "built_route_verified_routes": built_verified,
                "reachable_routes": reachable,
                "content_verified_routes": content_verified,
                "overall_status": "FAIL" if failures else "PASS",
                "results": results,
                "authority_boundary": (
                    "Source-route validation proves deterministic source wiring and extractable content markers only. "
                    "Built-site validation additionally proves that the Docusaurus output contains all expected route files with source-heading fidelity. "
                    "Deployed-route validation additionally proves public reachability and rendered heading fidelity. "
                    "None establishes framework compatibility, certification, endorsement, standing, admissibility, release authority, or execution authority."
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if args.source_only:
        label = "EXTERNAL FRAMEWORK SOURCE ROUTES"
    elif args.built_site:
        label = "EXTERNAL FRAMEWORK BUILT ROUTES"
    else:
        label = "EXTERNAL FRAMEWORK PUBLIC ROUTES"
    print(label + ":", "FAIL" if failures else "PASS")
    print(f"routes={len(frameworks)}/{EXPECTED_FRAMEWORK_COUNT}")
    print(f"source_contract_verified={source_verified}")
    if args.built_site:
        print(f"built_route_verified={built_verified}")
        print(f"content_verified={content_verified}")
    elif not args.source_only:
        print(f"reachable={reachable}")
        print(f"content_verified={content_verified}")
    print(f"report={report_path.relative_to(ROOT)}")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
