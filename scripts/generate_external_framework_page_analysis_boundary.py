#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
START = "<!-- GENERATED:EXTERNAL_FRAMEWORK_ANALYSIS_BOUNDARY:START -->"
END = "<!-- GENERATED:EXTERNAL_FRAMEWORK_ANALYSIS_BOUNDARY:END -->"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def block_for(entry: dict[str, Any]) -> str:
    framework_id = entry.get("framework_id", "unknown")
    name = entry.get("name", framework_id)
    return "\n".join([
        START,
        "",
        "## Generated Authored Analysis Boundary",
        "",
        "This section is generated. Do not edit it manually.",
        "",
        f"- Framework ID: `{framework_id}`",
        f"- Framework name: `{name}`",
        "- Generated sections above this boundary may be rebuilt from registry, manifest, compatibility-report, and result artifacts.",
        "- Authored analysis below this boundary may contain interpretation, notes, and framework-specific discussion.",
        "- Generators must preserve authored analysis unless a future validator explicitly declares a migration path.",
        "- Boundary rule: generated material is descriptive compatibility evidence only and does not create certification, endorsement, adoption, proof, or operational permission.",
        "",
        END,
    ])


def insert_block(text: str, block: str) -> str:
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + block + after

    anchor = "<!-- GENERATED:EXTERNAL_FRAMEWORK_EVALUATION_STATUS:END -->"
    if anchor in text:
        before, after = text.split(anchor, 1)
        return before + anchor + "\n\n" + block + after

    return text.rstrip() + "\n\n" + block + "\n"


def main() -> int:
    registry = read_json(REGISTRY)
    for entry in registry.get("entries", []):
        path = ROOT / entry["path"]
        if path.exists():
            path.write_text(insert_block(path.read_text(encoding="utf-8"), block_for(entry)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
