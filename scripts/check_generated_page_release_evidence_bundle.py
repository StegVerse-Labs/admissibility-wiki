#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "docs" / "external-frameworks" / "generated-page-release-evidence-bundle.json"
READINESS = ROOT / "docs" / "external-frameworks" / "generated-page-release-readiness.json"
TAG = ROOT / "docs" / "external-frameworks" / "generated-page-tag-candidate.json"


def main() -> int:
    failures: list[str] = []
    if not BUNDLE.exists():
        print("GENERATED PAGE RELEASE EVIDENCE BUNDLE: FAIL")
        print("- release evidence bundle missing")
        return 1

    data = json.loads(BUNDLE.read_text(encoding="utf-8"))
    if data.get("artifact_type") != "generated_page_release_evidence_bundle":
        failures.append("artifact type mismatch")
    if data.get("schema_version") != "0.1":
        failures.append("schema version mismatch")
    if data.get("repo") != "StegVerse-Labs/admissibility-wiki":
        failures.append("repo mismatch")
    if data.get("active_goal") != "declarative-external-framework-generation-pipeline":
        failures.append("active goal mismatch")
    if data.get("release_ready") is not False:
        failures.append("release evidence must remain blocked before release authorization")

    if READINESS.exists():
        readiness = json.loads(READINESS.read_text(encoding="utf-8"))
        if data.get("release_ready") != readiness.get("release_ready"):
            failures.append("release readiness mismatch")
    else:
        failures.append("release readiness artifact missing")

    if TAG.exists():
        tag = json.loads(TAG.read_text(encoding="utf-8"))
        if data.get("release_candidate") != tag.get("tag_candidate"):
            failures.append("release candidate mismatch")
        for blocker in tag.get("blocked_by", []):
            if blocker not in data.get("blocked_by", []):
                failures.append(f"missing release blocker: {blocker}")
    else:
        failures.append("tag candidate artifact missing")

    for artifact in data.get("required_evidence", []):
        if not isinstance(artifact, str) or not (ROOT / artifact).exists():
            failures.append(f"required evidence missing: {artifact}")

    boundary = data.get("boundary", {})
    if boundary.get("release_evidence_bundle_is_authority") is not False:
        failures.append("authority boundary mismatch")
    if boundary.get("release_without_authorization_allowed") is not False:
        failures.append("release authorization boundary mismatch")
    if boundary.get("missing_public_verification_fails_closed") is not True:
        failures.append("public verification boundary mismatch")
    if boundary.get("downstream_install_allowed_before_tag") is not False:
        failures.append("downstream install boundary mismatch")

    print("GENERATED PAGE RELEASE EVIDENCE BUNDLE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
