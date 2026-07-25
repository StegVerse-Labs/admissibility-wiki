#!/usr/bin/env python3
"""Fail closed if the wiki activation projection loses terminal-custody binding."""
from pathlib import Path
import sys

IMPORTER = Path("scripts/import_publisher_ecosystem_chat_activation.py")
CHAIN = Path("scripts/check_full_validation_chain.py")
WORKFLOW = Path(".github/workflows/validate-chain-continuation.yml")


def fail(message: str) -> None:
    print(f"ACTIVATION_PROJECTION_ORCHESTRATION_CONTRACT: FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not IMPORTER.is_file() or not CHAIN.is_file() or not WORKFLOW.is_file():
        fail("required importer, validation chain, or workflow missing")
    importer = IMPORTER.read_text(encoding="utf-8")
    chain = CHAIN.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    for marker in (
        "terminal_custody_verified",
        "terminal_custody_sha256",
        "master-records/orchestration",
        "custody_repository_mismatch",
        "projection_is_admissibility_determination\": False",
        "ecosystem_chat_activation_projection.v2",
    ):
        if marker not in importer:
            fail(f"importer marker absent: {marker}")
    if "scripts/check_activation_projection_orchestration_contract.py" not in chain:
        fail("guard is not bound into the canonical full validation chain")
    if "cancel-in-progress: true" not in workflow:
        fail("superseded canonical runs must be cancelled")
    if "schedule:" in workflow.split("permissions:", 1)[0]:
        fail("canonical wiki validation must not own a timer")
    print("ACTIVATION_PROJECTION_ORCHESTRATION_CONTRACT: PASS")
    print("terminal_custody_required=true")
    print("canonical_validation_binding=true")
    print("admissibility_authority_granted=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())