#!/usr/bin/env python3
"""Fail closed if the wiki activation projection loses terminal-custody binding."""
from pathlib import Path
import sys

IMPORTER = Path("scripts/import_publisher_ecosystem_chat_activation.py")
WORKFLOW = Path(".github/workflows/validate-chain-continuation.yml")


def fail(message: str) -> None:
    print(f"ACTIVATION_PROJECTION_ORCHESTRATION_CONTRACT: FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not IMPORTER.is_file() or not WORKFLOW.is_file():
        fail("required importer or workflow missing")
    importer = IMPORTER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    required_importer = (
        "terminal_custody_verified",
        "terminal_custody_sha256",
        "master-records/orchestration",
        "custody_repository_mismatch",
        "projection_is_admissibility_determination\": False",
        "ecosystem_chat_activation_projection.v2",
    )
    for marker in required_importer:
        if marker not in importer:
            fail(f"importer marker absent: {marker}")
    required_workflow = (
        "Validate activation projection orchestration contract",
        "python scripts/check_activation_projection_orchestration_contract.py",
        "Import Publisher activation projection",
        "python scripts/import_publisher_ecosystem_chat_activation.py",
        "cancel-in-progress: true",
    )
    for marker in required_workflow:
        if marker not in workflow:
            fail(f"workflow marker absent: {marker}")
    if "schedule:" in workflow.split("permissions:", 1)[0]:
        fail("canonical wiki validation must not own a timer")
    print("ACTIVATION_PROJECTION_ORCHESTRATION_CONTRACT: PASS")
    print("terminal_custody_required=true")
    print("admissibility_authority_granted=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())