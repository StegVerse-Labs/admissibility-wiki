#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts" / "capture_external_command_observation.py"
RUNBOOK = ROOT / "docs" / "external-frameworks" / "command-capture-runbook.md"
CAPTURE_ROOT = ROOT / "docs" / "external-frameworks" / "capture"

REQUIRED = {
    "mcp": "https://modelcontextprotocol.io/specification/2025-06-18",
    "a2a": "https://a2a-protocol.org/latest/specification/",
    "guardrails-ai": "https://guardrailsai.com/",
    "llama-guard": "https://ollama.com/library/llama-guard3",
    "nemo-guardrails": "https://docs.nvidia.com/nemo/guardrails/home",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    for path in [ENGINE, RUNBOOK]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")

    engine_text = ENGINE.read_text(encoding="utf-8") if ENGINE.exists() else ""
    runbook_text = RUNBOOK.read_text(encoding="utf-8") if RUNBOOK.exists() else ""

    for phrase in [
        "captured_unverified",
        "external_output_is_execution_authority",
        "capture_is_compatibility_proof",
        "version_command",
        "execute_command",
        "sha256",
    ]:
        if phrase not in engine_text:
            failures.append(f"capture engine missing phrase: {phrase}")

    for framework_id, source in REQUIRED.items():
        path = CAPTURE_ROOT / framework_id / "capture-manifest.json"
        if not path.exists():
            failures.append(f"missing manifest: {path.relative_to(ROOT)}")
            continue
        try:
            manifest = load_json(path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            failures.append(f"invalid manifest JSON {framework_id}: {exc}")
            continue

        if manifest.get("artifact_type") != "external_framework_capture_manifest":
            failures.append(f"artifact type mismatch: {framework_id}")
        if manifest.get("schema_version") != "0.1":
            failures.append(f"schema version mismatch: {framework_id}")
        if manifest.get("framework_id") != framework_id:
            failures.append(f"framework id mismatch: {framework_id}")
        if manifest.get("source_reference") != source:
            failures.append(f"canonical source mismatch: {framework_id}")
        for field in [
            "case_id",
            "source_version_or_date",
            "target_behavior",
            "input_payload",
            "required_runtime_context",
            "limitations",
        ]:
            if not manifest.get(field):
                failures.append(f"manifest missing {field}: {framework_id}")
        if len(manifest.get("required_runtime_context", [])) < 4:
            failures.append(f"insufficient runtime context requirements: {framework_id}")
        if len(manifest.get("limitations", [])) < 2:
            failures.append(f"insufficient limitations: {framework_id}")
        if str(path.relative_to(ROOT)) not in runbook_text and framework_id != "mcp":
            failures.append(f"runbook missing manifest path: {framework_id}")

    for phrase in [
        "captured_unverified != observed_partial",
        "classifier result != admissibility",
        "allowed flow != execution authority",
    ]:
        if phrase not in runbook_text:
            failures.append(f"runbook missing boundary phrase: {phrase}")

    print("PRIORITY COMMAND CAPTURE HARNESSES:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
