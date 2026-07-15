#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "static" / "sections" / "research-social-stegverse-completeness.v1.json"
SIDEBAR = ROOT / "sidebars.js"


def fail(message: str) -> None:
    raise SystemExit(f"RESEARCH SOCIAL STEGVERSE: FAIL - {message}")


def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing {ARTIFACT.relative_to(ROOT)}")
    if not SIDEBAR.exists():
        fail("missing sidebars.js")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("schema") != "admissibility_wiki_research_social_stegverse_completeness.v1":
        fail("schema mismatch")
    if data.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if data.get("classification") != "COMPLETE_WITH_EXTERNAL_GATES":
        fail("classification mismatch")

    public_pages = data.get("public_pages", [])
    hidden_pages = data.get("explicit_non_public_pages", [])
    counts = data.get("counts", {})
    if counts.get("public_sidebar_pages") != len(public_pages):
        fail("public page count is stale")
    if counts.get("stegverse_explicit_non_public_pages") != len(hidden_pages):
        fail("hidden page count is stale")

    sidebar_text = SIDEBAR.read_text(encoding="utf-8")
    public_paths: set[str] = set()
    for entry in public_pages:
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            fail("public entry missing path")
        if path in public_paths:
            fail(f"duplicate public page: {path}")
        public_paths.add(path)
        page = ROOT / path
        if not page.exists():
            fail(f"missing public page: {path}")
        text = page.read_text(encoding="utf-8")
        if entry.get("authority_effect") != "NONE":
            fail(f"public page authority effect must be NONE: {path}")
        route = path.removeprefix("docs/").removesuffix(".md")
        if route not in sidebar_text:
            fail(f"public page absent from sidebar: {route}")
        if path.endswith("stegverse-complete-security-paper.md"):
            for marker in ["Research architecture draft", "not a certification", "does not make unconditional claims"]:
                if marker not in text:
                    fail(f"security paper missing boundary: {marker}")
        if path.endswith("terminology-overlap-research-notes.md"):
            for marker in ["research note", "source-aware preliminary", "does not accept any external term as equivalent"]:
                if marker not in text:
                    fail(f"terminology research missing boundary: {marker}")
        if path.endswith("stegverse-quantum-security-carousel.md"):
            for marker in ["not certification", "communication trust is not execution trust", "Quantum proof"]:
                if marker.lower() not in text.lower():
                    fail(f"social derivative missing boundary: {marker}")
        if path.endswith("stegcore.md"):
            for marker in ["implementation surface", "not as the definition of admissibility", "not be described as proving all governance claims"]:
                if marker not in text:
                    fail(f"StegCore page missing boundary: {marker}")

    hidden_paths: set[str] = set()
    for entry in hidden_pages:
        path = entry.get("path")
        state = entry.get("navigation_state")
        if not isinstance(path, str) or not path:
            fail("hidden entry missing path")
        if path in hidden_paths or path in public_paths:
            fail(f"duplicate or conflicting page disposition: {path}")
        hidden_paths.add(path)
        if not (ROOT / path).exists():
            fail(f"missing hidden page: {path}")
        route = path.removeprefix("docs/").removesuffix(".md")
        if route in sidebar_text:
            fail(f"explicit non-public page appears in sidebar: {route}")
        if state not in {"NON_PUBLIC_EXPLICIT", "NON_PUBLIC_HISTORICAL_RECONCILIATION_REQUIRED"}:
            fail(f"invalid navigation state for {path}: {state}")

    current_status = ROOT / "docs" / "stegverse" / "current-status.md"
    current_text = current_status.read_text(encoding="utf-8")
    if "Generated: 2026-06-17" not in current_text:
        fail("historical current-status snapshot date changed without reconciliation")
    if not any(item.get("path") == "docs/stegverse/current-status.md" and item.get("navigation_state") == "NON_PUBLIC_HISTORICAL_RECONCILIATION_REQUIRED" for item in hidden_pages):
        fail("dated current-status snapshot lacks historical reconciliation disposition")

    boundaries = data.get("authority_boundaries", {})
    for key in [
        "research_draft_is_certification",
        "social_derivative_is_independent_source_authority",
        "wiki_component_page_is_implementation_authority",
        "dated_status_snapshot_is_current_authority",
        "publication_grants_execution_authority",
        "section_completeness_grants_release_authority",
    ]:
        if boundaries.get(key) is not False:
            fail(f"authority boundary must be false: {key}")

    print("RESEARCH SOCIAL STEGVERSE: PASS")
    print(f"public_pages={len(public_pages)}")
    print(f"explicit_non_public_pages={len(hidden_pages)}")
    print("historical_status_snapshots=1")


if __name__ == "__main__":
    main()
