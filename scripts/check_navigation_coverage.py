#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "static" / "navigation" / "navigation-coverage-policy.v1.json"
SIDEBAR = ROOT / "sidebars.js"
DOCS = ROOT / "docs"
REPORT = ROOT / "reports" / "navigation-coverage.json"


def fail(message: str) -> None:
    raise SystemExit(f"NAVIGATION COVERAGE: FAIL - {message}")


def doc_id(path: Path) -> str:
    relative = path.relative_to(DOCS).as_posix()
    if relative.endswith(".md"):
        relative = relative[:-3]
    elif relative.endswith(".mdx"):
        relative = relative[:-4]
    return relative


def main() -> int:
    for path in (POLICY, SIDEBAR, DOCS):
        if not path.exists():
            fail(f"missing required path: {path.relative_to(ROOT)}")

    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    if policy.get("schema") != "admissibility_wiki_navigation_coverage_policy.v1":
        fail("unexpected policy schema")
    if policy.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")

    docs = sorted(
        path for path in DOCS.rglob("*")
        if path.is_file() and path.suffix in {".md", ".mdx"}
    )
    docs_by_id = {doc_id(path): path for path in docs}

    sidebar_text = SIDEBAR.read_text(encoding="utf-8")
    quoted = re.findall(r"['\"]([^'\"]+)['\"]", sidebar_text)
    sidebar_ids = sorted({value for value in quoted if value in docs_by_id})

    apparent_doc_ids = sorted({
        value for value in quoted
        if "/" in value or value in {"index", "ADMISSIBILITY_WIKI_MIRROR_HANDOFF", "STEGVERSE_QUANTUM_SECURITY_MIRROR_HANDOFF", "ROBOTIC_LAW_ENFORCEMENT_ADOPTION_MIRROR_HANDOFF"}
    })
    missing_sidebar_targets = sorted(value for value in apparent_doc_ids if value not in docs_by_id)
    if missing_sidebar_targets:
        fail(f"sidebar targets missing from docs: {missing_sidebar_targets}")

    public = []
    non_public = []
    for identifier, path in docs_by_id.items():
        record = {
            "doc_id": identifier,
            "path": path.relative_to(ROOT).as_posix(),
            "classification": "PUBLIC_SIDEBAR" if identifier in sidebar_ids else "NON_PUBLIC_UNLISTED",
        }
        (public if identifier in sidebar_ids else non_public).append(record)

    if len(public) + len(non_public) != len(docs):
        fail("not every markdown document was classified")

    report = {
        "schema": "admissibility_wiki_navigation_coverage_report.v1",
        "repository": "StegVerse-Labs/admissibility-wiki",
        "policy": POLICY.relative_to(ROOT).as_posix(),
        "sidebar": SIDEBAR.relative_to(ROOT).as_posix(),
        "counts": {
            "markdown_pages": len(docs),
            "public_sidebar_pages": len(public),
            "non_public_unlisted_pages": len(non_public),
            "missing_sidebar_targets": len(missing_sidebar_targets),
            "unclassified_pages": 0,
        },
        "public_sidebar_pages": public,
        "non_public_unlisted_pages": non_public,
        "missing_sidebar_targets": missing_sidebar_targets,
        "authority_boundary": policy.get("authority_boundary"),
        "manual_tasks_required": [],
        "user_action_required": False,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if not report["authority_boundary"] or "does not create source authority" not in report["authority_boundary"]:
        fail("authority boundary is missing")
    if report["manual_tasks_required"] != [] or report["user_action_required"] is not False:
        fail("navigation audit violates no-manual boundary")

    print(
        "NAVIGATION COVERAGE: PASS - "
        f"pages={len(docs)} public={len(public)} non_public={len(non_public)} missing_targets=0 unclassified=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
