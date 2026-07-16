#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "repo-standards-integration.md"
BUNDLE_PAGE = ROOT / "docs" / "governance" / "repo-standards-installation-bundle.md"
SIDEBAR = ROOT / "sidebars.js"
HANDOFF = ROOT / "docs" / "ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md"
HANDOFF_ADDENDUM = ROOT / "docs" / "MIRROR_HANDOFF_GUARD_ADDENDUM.md"
STATUS = ROOT / "static" / "status" / "repo-standards-integration-status.json"
QUEUE = ROOT / "static" / "status" / "repo-standards-integration-release-update-queue.json"
BUNDLE_PLAN = ROOT / "static" / "status" / "repo-standards-installation-bundle-plan.json"
VALIDATION_REPORT = ROOT / "static" / "status" / "repo-standards-installation-validation-report.json"
DEPLOYMENT_VERIFICATION = ROOT / "static" / "status" / "repo-standards-public-deployment-verification.json"

REQUIRED_PAGE_SNIPPETS = [
    "StegVerse-Labs/repo-standards",
    "Release-Gated Reference Rule",
    "PENDING_UPSTREAM_TAG_RELEASE",
    "repository validation equals admissibility",
]

REQUIRED_BUNDLE_PAGE_SNIPPETS = [
    "Repo Standards Installation Bundle",
    "Bundle Contents Expected After Tag",
    "Cross-Org Install Test",
    "PENDING_UPSTREAM_TAG_RELEASE",
]

REQUIRED_SIDEBAR_SNIPPETS = [
    "governance/repo-standards-integration",
    "governance/repo-standards-installation-bundle",
]

REQUIRED_HANDOFF_SNIPPETS = [
    "repo-standards-integration-and-installation-bundle-pending-release",
    "docs/governance/repo-standards-integration.md",
    "docs/governance/repo-standards-installation-bundle.md",
    "UPSTREAM_TAG_RELEASE_PENDING_OUTSIDE_CONNECTOR",
]


def require_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path, label: str) -> dict:
    raw = require_file(path)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} JSON invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} JSON root must be an object")
    return data


def require_snippets(label: str, text: str, snippets: list[str]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - {label} missing: {joined}")


def require_status() -> None:
    data = read_json(STATUS, "status")
    expected = {
        "status_id": "repo-standards-integration-status",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "goal_id": "repo-standards-integration-pending-release",
        "status": "PENDING_UPSTREAM_TAG_RELEASE",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - status {key} expected {value!r}, got {data.get(key)!r}"
            )

    local = data.get("local_artifacts", {})
    if local.get("page") != "docs/governance/repo-standards-integration.md":
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - status local_artifacts.page is incorrect")
    if local.get("validator") != "scripts/check_repo_standards_integration.py":
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - status local_artifacts.validator is incorrect")


def require_queue() -> None:
    data = read_json(QUEUE, "queue")
    expected = {
        "queue_id": "repo-standards-integration-release-update-queue",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "status": "PENDING_UPSTREAM_TAG_RELEASE",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - queue {key} expected {value!r}, got {data.get(key)!r}"
            )
    pending = data.get("pending_updates")
    if not isinstance(pending, list) or len(pending) < 3:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - queue must define at least three pending updates")
    targets = {item.get("target") for item in pending if isinstance(item, dict)}
    required_targets = {
        "docs/governance/repo-standards-integration.md",
        "static/status/repo-standards-integration-status.json",
        "docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md",
    }
    missing = sorted(required_targets - targets)
    if missing:
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - queue missing targets: {', '.join(missing)}")


def require_bundle_plan() -> None:
    data = read_json(BUNDLE_PLAN, "bundle plan")
    expected = {
        "plan_id": "repo-standards-installation-bundle-plan",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "status": "PENDING_UPSTREAM_TAG_RELEASE",
        "source_repository": "StegVerse-Labs/repo-standards",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - bundle plan {key} expected {value!r}, got {data.get(key)!r}"
            )
    paths = data.get("expected_bundle_paths")
    if not isinstance(paths, list) or "config/org-profile.yaml" not in paths:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - bundle plan must require config/org-profile.yaml")
    if "runtime/" not in paths or "orchestration/" not in paths:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - bundle plan missing runtime/orchestration paths")


def require_validation_report() -> None:
    data = read_json(VALIDATION_REPORT, "validation report")
    expected = {
        "report_id": "repo-standards-installation-validation-report",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "goal_id": "repo-standards-integration-and-installation-bundle-pending-release",
        "result": "PENDING_LOCAL_VALIDATION",
        "validator": "scripts/check_repo_standards_integration.py",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - validation report {key} expected {value!r}, got {data.get(key)!r}"
            )
    commands = data.get("commands")
    if not isinstance(commands, list) or "npm run validate:repo-standards-integration" not in commands:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - validation report must include npm validation command")


def require_deployment_verification() -> None:
    data = read_json(DEPLOYMENT_VERIFICATION, "deployment verification")
    expected = {
        "verification_id": "repo-standards-public-deployment-verification",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "goal_id": "repo-standards-integration-and-installation-bundle-pending-release",
        "status": "PENDING_PUBLIC_DEPLOYMENT_VERIFICATION",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(
                f"REPO STANDARDS INTEGRATION: FAIL - deployment verification {key} expected {value!r}, got {data.get(key)!r}"
            )
    public_paths = {item.get("public_path") for item in data.get("pages_expected_after_deploy", []) if isinstance(item, dict)}
    required_paths = {
        "/governance/repo-standards-integration",
        "/governance/repo-standards-installation-bundle",
    }
    missing = sorted(required_paths - public_paths)
    if missing:
        raise SystemExit(f"REPO STANDARDS INTEGRATION: FAIL - deployment verification missing public paths: {', '.join(missing)}")


def main() -> int:
    page = require_file(PAGE)
    bundle_page = require_file(BUNDLE_PAGE)
    sidebar = require_file(SIDEBAR)
    handoff = require_file(HANDOFF)
    handoff_addendum = require_file(HANDOFF_ADDENDUM)
    combined_handoff = handoff + "\n" + handoff_addendum

    require_snippets("page", page, REQUIRED_PAGE_SNIPPETS)
    require_snippets("bundle page", bundle_page, REQUIRED_BUNDLE_PAGE_SNIPPETS)
    require_snippets("sidebar", sidebar, REQUIRED_SIDEBAR_SNIPPETS)
    require_snippets("handoff continuity record", combined_handoff, REQUIRED_HANDOFF_SNIPPETS)
    if "release authority: none granted" not in handoff_addendum:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - handoff addendum missing release non-authority boundary")
    if "destination mutation authority: none granted" not in handoff_addendum:
        raise SystemExit("REPO STANDARDS INTEGRATION: FAIL - handoff addendum missing destination mutation non-authority boundary")
    require_status()
    require_queue()
    require_bundle_plan()
    require_validation_report()
    require_deployment_verification()

    print("REPO STANDARDS INTEGRATION: PASS - integration, installation bundle, validation, and deployment verification surfaces present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
