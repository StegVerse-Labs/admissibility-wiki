#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "external-frameworks" / "implementation-selections" / "cedar-policy-cli-4.11.0.selection-evidence.json"
REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_COMMIT = "0807ec154afd7ffa14a658c9955d25bfe12770ca"
EXPECTED_VERSION = "4.11.0"


def main() -> int:
    failures: list[str] = []
    for path in (EVIDENCE, REGISTRY):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("CEDAR IMPLEMENTATION SELECTION EVIDENCE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if evidence.get("artifact_type") != "external_framework_implementation_selection_evidence":
        failures.append("artifact_type mismatch")
    if evidence.get("framework_id") != "cedar-policy":
        failures.append("framework_id mismatch")
    if evidence.get("selection_state") != "implementation_selected_hash_bound":
        failures.append("selection_state mismatch")

    implementation = evidence.get("implementation", {})
    if implementation.get("identifier") != "cedar-policy-cli":
        failures.append("implementation identifier mismatch")
    if implementation.get("canonical_commit") != EXPECTED_COMMIT:
        failures.append("canonical commit mismatch")
    if implementation.get("version") != EXPECTED_VERSION:
        failures.append("version mismatch")

    source_rows = evidence.get("canonical_source_evidence", [])
    if len(source_rows) < 4:
        failures.append("insufficient canonical source evidence")
    canonical_parts = []
    for row in source_rows:
        blob = str(row.get("git_blob_sha", ""))
        path = str(row.get("path", ""))
        if not path or not HEX40.fullmatch(blob):
            failures.append(f"invalid source row: {row}")
        canonical_parts.append(f"{path}:{blob}")
    canonical = f"cedar-policy/cedar@{EXPECTED_COMMIT}|" + "|".join(canonical_parts)
    computed = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    recorded = evidence.get("source_evidence_bundle", {}).get("sha256")
    if recorded != computed or not HEX64.fullmatch(str(recorded or "")):
        failures.append("source evidence bundle hash mismatch")

    commands = evidence.get("commands", {})
    for key in ("version_command", "build_command", "evaluation_command_template"):
        if not str(commands.get(key, "")).strip():
            failures.append(f"commands.{key} missing")
    if "--locked" not in str(commands.get("build_command", "")):
        failures.append("build command must be lockfile-bound")

    boundary = evidence.get("authority_boundary", {})
    for key in ("selection_is_certification", "selection_is_compatibility", "selection_creates_standing", "selection_authorizes_execution", "source_bundle_hash_is_compiled_binary_hash"):
        if boundary.get(key) is not False:
            failures.append(f"authority_boundary.{key} must be false")

    cedar = next((item for item in registry.get("frameworks", []) if item.get("framework_id") == "cedar-policy"), None)
    if not cedar:
        failures.append("Cedar registry record missing")
    else:
        if cedar.get("selection_state") != "implementation_selected_hash_bound":
            failures.append("registry Cedar state mismatch")
        if cedar.get("execution_authorized") is not False:
            failures.append("registry Cedar execution must remain unauthorized")
        selection = cedar.get("selection", {})
        expected_path = str(EVIDENCE.relative_to(ROOT))
        if selection.get("selection_evidence_path") != expected_path:
            failures.append("registry evidence path mismatch")
        expected_hash = f"source-evidence-bundle-sha256:{computed}"
        if selection.get("artifact_or_package_hash") != expected_hash:
            failures.append("registry source bundle hash mismatch")
        if selection.get("compiled_binary_sha256") is not None:
            failures.append("compiled binary hash must remain pending")

    print("CEDAR IMPLEMENTATION SELECTION EVIDENCE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
