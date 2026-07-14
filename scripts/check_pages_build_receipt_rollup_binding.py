#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_pages_build_receipt.py"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
IOS_MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"


def fail(message: str) -> None:
    raise SystemExit(f"PAGES BUILD RECEIPT ROLLUP BINDING: FAIL - {message}")


def main() -> int:
    for path in (WRITER, WORKFLOW, IOS_MIRROR):
        if not path.exists():
            fail(f"required file missing: {path.relative_to(ROOT)}")

    writer = WRITER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    mirror = IOS_MIRROR.read_text(encoding="utf-8")

    required_writer_markers = (
        'ROLLUP = ROOT / "static" / "status" / "canonical-workflow-observation-rollup.json"',
        '"state": "FAIL_CLOSED_ROLLUP_MISSING"',
        '"state": "ROLLUP_BOUND" if valid_terminal else "FAIL_CLOSED_ROLLUP_INVALID"',
        'payload.get("terminal_envelope") is True',
        'payload.get("recursive_derivative_expansion_allowed") is False',
        'payload.get("manual_tasks_required") == []',
        'payload.get("user_action_required") is False',
        'rollup_binding.get("completeness_state") == "COMPLETE_LOCAL_CHAIN"',
        '"schema_version": "0.2"',
        '"terminal_rollup_binding": rollup_binding',
        '"manual_tasks_required": []',
        '"user_action_required": False',
        '"rollup_binding_is_semantic_reclassification": False',
        '"repair_exact_build_or_rollup_failure_then_rebuild"',
    )
    for marker in required_writer_markers:
        if marker not in writer:
            fail(f"writer contract marker missing: {marker}")

    required_workflow_markers = (
        "python scripts/write_pages_build_receipt.py",
        "name: pages-build-receipt",
        "path: reports/pages-build-receipt.json",
        "if-no-files-found: error",
        "retention-days: 30",
    )
    for marker in required_workflow_markers:
        if marker not in workflow:
            fail(f"canonical workflow custody marker missing: {marker}")
        if marker not in mirror:
            fail(f"iOS workflow mirror custody marker missing: {marker}")

    if workflow != mirror:
        fail("canonical workflow and iOS-safe mirror differ")

    print(
        "PAGES BUILD RECEIPT ROLLUP BINDING: PASS - "
        "terminal=true recursive=false completeness=required retention_days=30 manual_tasks=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
