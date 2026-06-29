#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"
START = "<!-- GENERATED:EXTERNAL_FRAMEWORK_MAPPING:START -->"
END = "<!-- GENERATED:EXTERNAL_FRAMEWORK_MAPPING:END -->"
FIELDS = [
    "framework_identity",
    "source_reference",
    "source_version",
    "allowed_use_boundary",
    "claims",
    "non_claims",
    "input_artifact_type",
    "output_artifact_type",
    "actor_or_authority_model",
    "evidence_model",
    "policy_or_rule_model",
    "delegation_model",
    "decision_or_result_model",
    "execution_authority_claim",
    "receipt_or_trace_model",
    "reconstruction_model",
    "SPE_overlap",
    "StegVerse_ecosystem_overlap",
    "fail_closed_conditions",
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cell(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "not recorded"
    return str(value).replace("\n", " ").replace("|", "\\|")


def block_for(entry: dict[str, Any]) -> str:
    manifest = read_json(ROOT / entry["manifest_path"])
    mapping = manifest.get("transition_table_mapping", {})
    rows = ["| Field | Generated Value |", "|---|---|"]
    for field in FIELDS:
        rows.append(f"| `{field}` | {cell(mapping.get(field))} |")
    return "\n".join([
        START,
        "",
        "## Generated Transition Mapping",
        "",
        "This section is generated from the framework manifest. Do not edit it manually.",
        "",
        *rows,
        "",
        "Generated mapping is compatibility evidence only.",
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
    insert_at = next((index + 1 for index, line in enumerate(lines) if line.startswith("# ")), 0)
    return "\n".join(lines[:insert_at] + ["", block, ""] + lines[insert_at:]).rstrip() + "\n"


def main() -> int:
    registry = read_json(REGISTRY)
    for entry in registry.get("entries", []):
        path = ROOT / entry["path"]
        if path.exists():
            path.write_text(insert_block(path.read_text(encoding="utf-8"), block_for(entry)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
