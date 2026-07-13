#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACQUIRE = ROOT / "scripts/acquire_external_chat_activation_evidence.py"
SYNC = ROOT / "scripts/sync_external_chat_activation_evidence.py"
IMPORTER = ROOT / "scripts/import_external_chat_activation_evidence.py"
AGGREGATE = ROOT / "scripts/check_goal5_external_frameworks_all.py"


def fail(message: str) -> int:
    print(f"EXTERNAL CHAT ACTIVATION SYNC CONTRACT: FAIL - {message}")
    return 1


def main() -> int:
    for path in (ACQUIRE, SYNC, IMPORTER, AGGREGATE):
        if not path.exists():
            return fail(f"missing {path.relative_to(ROOT)}")

    acquire = ACQUIRE.read_text(encoding="utf-8")
    sync = SYNC.read_text(encoding="utf-8")
    importer = IMPORTER.read_text(encoding="utf-8")
    aggregate = AGGREGATE.read_text(encoding="utf-8")

    required_acquire = (
        'OWNER = "StegVerse-Labs"',
        'REPO = "Site"',
        'WORKFLOW_NAME = "Site Task Runner"',
        'ARTIFACT_PREFIX = "external-chat-activation-evidence-"',
        'head_branch") == "main"',
        'conclusion") == "success"',
        'return sorted(candidates',
        'expected_name = f"{ARTIFACT_PREFIX}{run_id}-{run_attempt}"',
        'artifact.get("name") == expected_name',
        'multiple exact activation evidence artifacts found',
        'no_successful_run_has_exact_activation_evidence_artifact',
        'artifact name does not bind selected workflow run and attempt',
        'payload workflow_run_id does not match selected run',
        'payload workflow_run_attempt does not match selected run attempt',
        'payload commit_sha does not match selected run head_sha',
        'successful_runs_inspected',
        'public_artifact_download_requires_authentication',
        'projection_written": False',
        '"state": "FAIL_CLOSED"',
    )
    for marker in required_acquire:
        if marker not in acquire:
            return fail(f"acquisition client missing marker: {marker}")

    forbidden_acquire = (
        'selected = max(candidates',
        'str(artifact.get("name", "")).startswith(ARTIFACT_PREFIX)',
        'successful_run_has_no_activation_evidence_artifact',
    )
    for marker in forbidden_acquire:
        if marker in acquire:
            return fail(f"acquisition client retains stale selection behavior: {marker}")

    required_sync = (
        'state == "FAIL_CLOSED"',
        'state == "SKIPPED"',
        'state != "ACQUIRED_EXACT_ARTIFACT"',
        'projected evidence hash drift',
        'provenance run identity drift',
        'provenance commit identity drift',
        'receipt["state"] = "IMPORTED_EXACT_ARTIFACT"',
    )
    for marker in required_sync:
        if marker not in sync:
            return fail(f"sync orchestrator missing marker: {marker}")

    for marker in (
        'payload.get("repository") != "StegVerse-Labs/Site"',
        'activation evidence SHA-256 mismatch',
        'mutation_required_disabled',
        'import_is_repository_mutation_authority": False',
        'import_is_publication_authority": False',
        'import_is_certification": False',
        'import_creates_standing": False',
    ):
        if marker not in importer:
            return fail(f"importer boundary missing marker: {marker}")

    aggregate_markers = (
        'SYNC_SCRIPT = "scripts/sync_external_chat_activation_evidence.py"',
        'scripts/check_external_chat_activation_sync.py',
        'sync_state',
        'sync_output',
        'external_chat_activation_sync',
    )
    for marker in aggregate_markers:
        if marker not in aggregate:
            return fail(f"Goal 5 aggregate missing marker: {marker}")

    print("EXTERNAL CHAT ACTIVATION SYNC CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
