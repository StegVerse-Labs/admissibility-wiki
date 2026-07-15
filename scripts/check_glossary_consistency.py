#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "static" / "glossary" / "glossary-registry.v1.json"
INDEX = ROOT / "docs" / "glossary" / "index.md"

SECTION_ALIASES = {
    "terminology-reconciliation": {
        "equivalent_terms": ["## Equivalent Terms", "## Relationship Classes"],
        "related_terms": ["## Related Terms", "## Relationship Classes"],
    }
}


def fail(message: str) -> None:
    raise SystemExit(f"GLOSSARY CONSISTENCY: FAIL - {message}")


def has_any(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)


def main() -> None:
    if not REGISTRY.exists():
        fail(f"missing {REGISTRY.relative_to(ROOT)}")
    if not INDEX.exists():
        fail(f"missing {INDEX.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema") != "admissibility_wiki_glossary_registry.v1":
        fail("unexpected registry schema")
    if data.get("repository") != "StegVerse-Labs/admissibility-wiki":
        fail("repository mismatch")
    if data.get("index") != "docs/glossary/index.md":
        fail("index reference mismatch")

    relationship_classes = data.get("relationship_classes", [])
    if relationship_classes != ["synonymous", "adjacent", "new", "unresolved"]:
        fail("relationship classes must be exactly synonymous, adjacent, new, unresolved")

    terms = data.get("terms", [])
    counts = data.get("counts", {})
    if len(terms) != counts.get("terms"):
        fail("term count is stale")
    if counts.get("active") != len(terms):
        fail("active term count is stale")
    if counts.get("synonymous_relationships") != 0:
        fail("no synonymous relationships are currently accepted")

    index_text = INDEX.read_text(encoding="utf-8")
    ids: set[str] = set()
    paths: set[str] = set()
    names: set[str] = set()

    for term in terms:
        term_id = term.get("term_id")
        name = term.get("name")
        path = term.get("path")
        term_class = term.get("term_class")
        required_markers = term.get("required_markers", [])
        prohibited = term.get("prohibited_conflations", [])

        if not isinstance(term_id, str) or not term_id:
            fail("every term must have a non-empty term_id")
        if term_id in ids:
            fail(f"duplicate term_id: {term_id}")
        ids.add(term_id)

        if not isinstance(name, str) or not name:
            fail(f"missing name for {term_id}")
        if name in names:
            fail(f"duplicate term name: {name}")
        names.add(name)

        if not isinstance(path, str) or not path:
            fail(f"missing path for {term_id}")
        if path in paths:
            fail(f"duplicate glossary path: {path}")
        paths.add(path)

        page = ROOT / path
        if not page.exists():
            fail(f"missing glossary page: {path}")
        text = page.read_text(encoding="utf-8")

        if not isinstance(term_class, str) or not term_class:
            fail(f"missing term_class for {term_id}")
        if f"# {name}" not in text:
            fail(f"page title mismatch for {term_id}")
        if "## Definition" not in text:
            fail(f"missing Definition section for {term_id}")

        aliases = SECTION_ALIASES.get(term_id, {})
        equivalent_markers = aliases.get("equivalent_terms", ["## Equivalent Terms"])
        related_markers = aliases.get("related_terms", ["## Related Terms"])
        if not has_any(text, equivalent_markers):
            fail(f"missing Equivalent Terms semantic section for {term_id}")
        if not has_any(text, related_markers):
            fail(f"missing Related Terms semantic section for {term_id}")
        if name not in index_text:
            fail(f"index missing glossary entry: {name}")

        for marker in required_markers:
            if marker not in text:
                fail(f"missing required marker for {term_id}: {marker}")
        if not isinstance(prohibited, list) or not prohibited:
            fail(f"missing prohibited_conflations for {term_id}")

        definition_match = re.search(r"## Definition\s+(.+?)(?=\n## |\Z)", text, flags=re.S)
        if not definition_match or len(definition_match.group(1).strip()) < 30:
            fail(f"definition is missing or too short for {term_id}")

    expected_paths = {
        f"docs/glossary/{match}.md"
        for match in re.findall(r"\]\(\./([^)]+)\.md\)", index_text)
    }
    missing_from_registry = expected_paths - paths
    if missing_from_registry:
        fail(f"index entries missing from registry: {sorted(missing_from_registry)}")

    global_non_claims = data.get("global_non_claims", [])
    if len(global_non_claims) < 3:
        fail("at least three global non-claims are required")
    joined = " ".join(global_non_claims).lower()
    for boundary in ["source authority", "equivalence", "execution authority", "runtime behavior"]:
        if boundary not in joined:
            fail(f"global non-claims missing boundary: {boundary}")

    print("GLOSSARY CONSISTENCY: PASS")
    print(f"terms={len(terms)}")
    print("accepted_synonymous_relationships=0")
    print("authority_effect=NONE")


if __name__ == "__main__":
    main()
