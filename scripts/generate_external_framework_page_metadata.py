#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
START = "<!-- GENERATED:EXTERNAL_FRAMEWORK_METADATA:START -->"
END = "<!-- GENERATED:EXTERNAL_FRAMEWORK_METADATA:END -->"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def block_for(entry: dict[str, Any]) -> str:
    manifest_path = entry.get("manifest_path", "")
    manifest_file = ROOT / manifest_path
    manifest = read_json(manifest_file) if manifest_file.exists() else {}
    framework_id = entry.get("framework_id", "")
    source = entry.get("source", manifest.get("source_reference", ""))
    status = entry.get("status", "")
    testbench_state = entry.get("testbench_state", "")
    name = entry.get("name", manifest.get("name", framework_id))
    schema_version = manifest.get("schema_version", "missing")
    source_version = manifest.get("source_version", "missing")

    return "\n".join([
        START,
        "",
        "## Generated Framework Metadata",
        "",
        "This section is generated from the external-framework registry and manifest. Do not edit it manually.",
        "",
        f"- Framework ID: `{framework_id}`",
        f"- Name: `{name}`",
        f"- Registry status: `{status}`",
        f"- Testbench state: `{testbench_state}`",
        f"- Manifest path: `{manifest_path}`",
        f"- Manifest schema version: `{schema_version}`",
        f"- Source reference: `{source}`",
        f"- Source version: `{source_version}`",
        "- Metadata boundary: generated metadata is descriptive only; it does not create certification, endorsement, formalism adoption, admissibility proof, or execution authority.",
        "",
        END,
    ])


def insert_block(text: str, block: str) -> str:
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    anchor = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:START -->"
    if anchor in text:
        before, after = text.split(anchor, 1)
        return before.rstrip() + "\n\n" + block + "\n\n" + anchor + after

    lines = text.splitlines()
    insert_at = 0
    for index, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = index + 1
            break
    new_lines = lines[:insert_at] + ["", block, ""] + lines[insert_at:]
    return "\n".join(new_lines).rstrip() + "\n"


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
