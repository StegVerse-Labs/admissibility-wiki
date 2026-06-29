#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
START = "<!-- GENERATED:EXTERNAL_FRAMEWORK_TERMS:START -->"
END = "<!-- GENERATED:EXTERNAL_FRAMEWORK_TERMS:END -->"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def list_items(values: Any) -> list[str]:
    if isinstance(values, list):
        return [str(item) for item in values]
    if isinstance(values, str):
        return [values]
    return []


def rows(mapping: dict[str, Any]) -> list[str]:
    out = []
    for key in sorted(mapping):
        value = mapping[key]
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (dict, list)):
            rendered = json.dumps(value, sort_keys=True)
        else:
            rendered = str(value)
        out.append(f"| `{key}` | {rendered} |")
    return out


def bullet_section(title: str, items: list[str]) -> list[str]:
    if not items:
        items = ["No generated entries recorded."]
    return [f"### {title}", "", *[f"- {item}" for item in items], ""]


def block_for(entry: dict[str, Any]) -> str:
    manifest_path = entry.get("manifest_path", "")
    manifest = read_json(ROOT / manifest_path) if manifest_path else {}
    mapping = manifest.get("transition_table_mapping", {})
    spe = manifest.get("SPE_overlap", {})
    ecosystem = manifest.get("StegVerse_ecosystem_overlap", {})

    lines = [
        START,
        "",
        "## Generated Framework Terms",
        "",
        "This section is generated from the framework manifest. Do not edit it manually.",
        "",
        *bullet_section("Allowed Use Boundary", list_items(manifest.get("allowed_use_boundary"))),
        *bullet_section("Claims", list_items(manifest.get("claims"))),
        *bullet_section("Non-Claims", list_items(manifest.get("non_claims"))),
        "### Transition Table Mapping",
        "",
        "| Element | Generated Value |",
        "|---|---|",
        *rows(mapping),
        "",
        "### SPE Overlap",
        "",
        "| Element | Generated Value |",
        "|---|---|",
        *rows(spe),
        "",
        "### StegVerse Ecosystem Overlap",
        "",
        "| Element | Generated Value |",
        "|---|---|",
        *rows(ecosystem),
        "",
        "Terms boundary: generated terms are descriptive compatibility evidence only; they do not create certification, endorsement, formalism adoption, admissibility proof, or execution authority.",
        "",
        END,
    ]
    return "\n".join(lines)


def insert_block(text: str, block: str) -> str:
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    anchor = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:START -->"
    if anchor in text:
        before, after = text.split(anchor, 1)
        return before.rstrip() + "\n\n" + block + "\n\n" + anchor + after

    return text.rstrip() + "\n\n" + block + "\n"


def main() -> int:
    registry = read_json(REGISTRY)
    for entry in registry.get("entries", []):
        path = ROOT / entry["path"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        path.write_text(insert_block(text, block_for(entry)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
