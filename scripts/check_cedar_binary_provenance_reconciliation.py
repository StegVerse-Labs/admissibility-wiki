#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reconcile_cedar_registry_binary_provenance.py"
REGISTRY = ROOT / "docs" / "external-frameworks" / "implementation-selection-gates.v0.1.json"
HASH = "a" * 64


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run(paths: dict[str, Path], output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--registry", str(paths["registry"]),
            "--build-receipt", str(paths["build"]),
            "--candidate", str(paths["candidate"]),
            "--promotion-receipt", str(paths["promotion"]),
            "--application-result", str(paths["application"]),
            "--output", str(output),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> int:
    failures: list[str] = []
    for path in (SCRIPT, REGISTRY):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        print("CEDAR BINARY PROVENANCE RECONCILIATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    text = SCRIPT.read_text(encoding="utf-8")
    for marker in (
        "PROVENANCE_RECONCILED_HASH_ONLY",
        "PROVENANCE_UNRESOLVED_FAIL_CLOSED",
        "BUILT_HASHED_UNEXECUTED",
        "READY_FOR_REGISTRY_PROMOTION_REVIEW",
        "APPLIED_HASH_ONLY",
        '"runtime_execution_authorized": False',
        '"runtime_execution_requested": False',
        '"external_consequence_allowed": False',
        "binary hash mismatch across provenance chain",
    ):
        if marker not in text:
            failures.append(f"reconciliation script missing marker: {marker}")
    for forbidden in ("cedar authorize", "subprocess.run([binary", '"execution_authorized": True'):
        if forbidden in text:
            failures.append(f"reconciliation script contains forbidden marker: {forbidden}")

    if not failures:
        with tempfile.TemporaryDirectory(prefix="cedar-provenance-") as directory:
            root = Path(directory)
            paths = {name: root / f"{name}.json" for name in ("registry", "build", "candidate", "promotion", "application")}
            registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
            cedar = next(item for item in registry["frameworks"] if item.get("framework_id") == "cedar-policy")
            cedar["selection"]["compiled_binary_sha256"] = HASH
            cedar["execution_authorized"] = False
            write(paths["registry"], registry)
            write(paths["build"], {
                "overall_status": "BUILT_HASHED_UNEXECUTED",
                "binary": {"sha256": HASH, "executed_after_build": False},
                "authority_boundary": {"runtime_execution_authorized": False},
            })
            write(paths["candidate"], {
                "candidate_state": "READY_FOR_REGISTRY_PROMOTION_REVIEW",
                "binary_sha256": HASH,
                "registry_mutation_performed": False,
                "runtime_execution_authorized": False,
            })
            write(paths["promotion"], {
                "decision": "ALLOW_REGISTRY_PROMOTION_ONLY",
                "promotion_state": "APPLIED_HASH_ONLY",
                "source_promotion_candidate": {"binary_sha256": HASH},
                "registry_target": {"proposed_value": HASH},
                "registry_mutation_applied": True,
                "runtime_execution_authorized": False,
            })
            write(paths["application"], {
                "application_state": "APPLIED_HASH_ONLY",
                "registry": {"approved_value": HASH},
                "runtime_execution_authorized": False,
                "external_consequence_allowed": False,
            })
            output = root / "result.json"
            passed = run(paths, output)
            if passed.returncode != 0:
                failures.append(f"matching-chain test failed: {passed.stdout.strip()}")
            else:
                result = json.loads(output.read_text(encoding="utf-8"))
                if result.get("reconciliation_state") != "PROVENANCE_RECONCILED_HASH_ONLY":
                    failures.append("matching-chain reconciliation state mismatch")
                if result.get("all_hashes_equal") is not True:
                    failures.append("matching-chain equality not recorded")

            mismatched = json.loads(paths["candidate"].read_text(encoding="utf-8"))
            mismatched["binary_sha256"] = "b" * 64
            write(paths["candidate"], mismatched)
            fail_output = root / "failed.json"
            blocked = run(paths, fail_output)
            if blocked.returncode == 0:
                failures.append("mismatched-chain test did not fail closed")
            else:
                result = json.loads(fail_output.read_text(encoding="utf-8"))
                if result.get("reconciliation_state") != "PROVENANCE_UNRESOLVED_FAIL_CLOSED":
                    failures.append("mismatched-chain fail-closed state mismatch")
                if result.get("runtime_execution_authorized") is not False:
                    failures.append("mismatched-chain altered runtime authority")

    print("CEDAR BINARY PROVENANCE RECONCILIATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
