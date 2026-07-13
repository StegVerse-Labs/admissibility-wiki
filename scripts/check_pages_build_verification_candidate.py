#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pages_build_verification_candidate.py"
BUILD_WRITER = ROOT / "scripts" / "write_pages_build_receipt.py"

GENERATOR_MARKERS = [
    '"artifact_type": "pages_build_verification_candidate"',
    '"candidate_only": True',
    '"deployment_authorized": False',
    '"public_verification_complete": False',
    '"PAGES_BUILD_PASS_ARTIFACT_PENDING"',
    '"FAIL_CLOSED"',
    '"candidate generation does not mutate canonical status"',
    '"observe_pages_artifact_upload_and_bind_artifact_id_and_digest"',
    'reports" / "pages-build-receipt.json',
    'reports" / "pages-build-verification-candidate.json',
]
WRITER_MARKERS = [
    '"artifact_type": "admissibility_wiki_pages_build_receipt"',
    '"manifest_sha256"',
    '"file_count"',
    '"total_size_bytes"',
]


def main() -> int:
    failures: list[str] = []
    for path in (GENERATOR, BUILD_WRITER):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    generator = GENERATOR.read_text(encoding="utf-8") if GENERATOR.exists() else ""
    writer = BUILD_WRITER.read_text(encoding="utf-8") if BUILD_WRITER.exists() else ""

    if generator:
        try:
            ast.parse(generator)
        except SyntaxError as exc:
            failures.append(f"generator syntax error: {exc}")

    for marker in GENERATOR_MARKERS:
        if marker not in generator:
            failures.append(f"generator missing marker: {marker}")
    for marker in WRITER_MARKERS:
        if marker not in writer:
            failures.append(f"build writer missing marker: {marker}")

    if "static/status/pages-build-verification.json" in generator:
        failures.append("candidate generator must not mutate canonical status")
    if "subprocess" in generator or "os.system" in generator:
        failures.append("candidate generator must not execute external commands")

    print("PAGES BUILD VERIFICATION CANDIDATE:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
