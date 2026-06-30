#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs" / "external-frameworks" / "generated-page-entrypoint-closeout-propagation.json"
CLOSEOUT = ROOT / "docs" / "external-frameworks" / "generated-page-closeout-bundle.json"
CLOSEOUT_PATH = "docs/external-frameworks/generated-page-closeout-bundle.json"


def main() -> int:
    failures: list[str] = []
    if not RECORD.exists():
        print("GENERATED PAGE ENTRYPOINT CLOSEOUT PROPAGATION: FAIL")
        print("- propagation record missing")
        return 1

    data = json.loads(RECORD.read_text(encoding="utf-8"))
    source_artifact = data.get("source_artifact")
    if data.get("artifact_type") != "generated_page_entrypoint_closeout_propagation":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if not isinstance(source_artifact, str) or not source_artifact.startswith("docs/external-frameworks/generated-page-"):
        failures.append("source artifact mismatch")
    if data.get("closeout_artifact") != CLOSEOUT_PATH:
        failures.append("closeout artifact mismatch")
    if data.get("propagation_state") != "required_by_closeout_bundle":
        failures.append("propagation state mismatch")
    if isinstance(source_artifact, str) and not (ROOT / source_artifact).exists():
        failures.append("source artifact missing")
    if not CLOSEOUT.exists():
        failures.append("closeout artifact missing")
    else:
        closeout = json.loads(CLOSEOUT.read_text(encoding="utf-8"))
        if source_artifact not in closeout.get("required_artifacts", []):
            failures.append("source artifact not required by closeout bundle")

    boundary = data.get("boundary", {})
    if boundary.get("propagation_record_is_authority") is not False:
        failures.append("propagation record authority boundary mismatch")
    if boundary.get("source_artifact_is_authority") is not False:
        failures.append("source artifact authority boundary mismatch")
    if boundary.get("closeout_artifact_is_authority") is not False:
        failures.append("closeout artifact authority boundary mismatch")
    if boundary.get("missing_closeout_propagation_fails_closed") is not True:
        failures.append("missing propagation boundary mismatch")

    print("GENERATED PAGE ENTRYPOINT CLOSEOUT PROPAGATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
