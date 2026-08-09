#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "external-frameworks" / "cedar"
DEFAULT_OUTPUT = REPORTS / "cedar-same-environment-replay-receipt.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def normalized_decision(stdout: bytes) -> str | None:
    text = stdout.decode("utf-8", errors="replace").strip().upper()
    if text == "ALLOW":
        return "ALLOW"
    if text == "DENY":
        return "DENY"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay captured Cedar authorization cases in the same runner and exact binary environment.")
    parser.add_argument("--allow-capture", type=Path, required=True)
    parser.add_argument("--deny-capture", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    receipt = {
        "artifact_type": "cedar_same_environment_replay_receipt",
        "schema_version": "0.1",
        "framework_id": "cedar-policy",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "replay_class": "SAME_RUNNER_SAME_BINARY",
        "cases": [],
        "overall_result": "FAIL",
        "authority_boundary": {
            "replay_is_execution_authority": False,
            "replay_creates_standing": False,
            "replay_is_certification": False,
            "replay_is_independent_provider_reproduction": False,
            "replay_binds_external_consequence": False,
        },
        "limitations": [
            "Replay occurs on the same hosted runner and exact binary as the original bounded capture.",
            "Fresh-runner replay is not established by this receipt.",
            "Independent implementation or provider reproduction is not established by this receipt.",
            "Deterministic replay evidence does not grant standing or execution authority.",
        ],
    }

    failures: list[str] = []
    binary_hashes: set[str] = set()
    for label, path in (("allow", args.allow_capture), ("deny", args.deny_capture)):
        try:
            capture = load(path)
            runtime = capture["runtime"]
            replay = capture["replay"]
            evaluate_command = replay["evaluate_command"]
            version_command = replay["version_command"]
            if not isinstance(evaluate_command, list) or not all(isinstance(x, str) for x in evaluate_command):
                raise ValueError("evaluate_command is not a string list")
            if not isinstance(version_command, list) or not all(isinstance(x, str) for x in version_command):
                raise ValueError("version_command is not a string list")
            binary = Path(evaluate_command[0])
            if not binary.exists() or not binary.is_file():
                raise ValueError("captured binary path is unavailable in same environment")
            binary_hash = hashlib.sha256(binary.read_bytes()).hexdigest()
            binary_hashes.add(binary_hash)

            version_result = run(version_command)
            evaluation = run(evaluate_command)
            decision = normalized_decision(evaluation.stdout)
            expected_decision = runtime.get("observed_decision")
            expected_exit = runtime.get("exit_code")
            expected_stdout_sha = capture.get("hashes", {}).get("stdout_sha256")
            expected_stderr_sha = capture.get("hashes", {}).get("stderr_sha256")

            predicates = {
                "version_exit_matches": version_result.returncode == 0,
                "version_output_matches": version_result.stdout.decode("utf-8", errors="replace") == runtime.get("version_output", {}).get("raw"),
                "decision_matches": decision == expected_decision,
                "exit_code_matches": evaluation.returncode == expected_exit,
                "stdout_sha256_matches": sha256_bytes(evaluation.stdout) == expected_stdout_sha,
                "stderr_sha256_matches": sha256_bytes(evaluation.stderr) == expected_stderr_sha,
                "binary_hash_matches_capture": binary_hash == capture.get("runtime", {}).get("binary_sha256", binary_hash),
            }
            matched = all(predicates.values())
            if not matched:
                failures.append(label)
            receipt["cases"].append({
                "label": label,
                "source_case_id": capture.get("case_id"),
                "captured_decision": expected_decision,
                "replayed_decision": decision,
                "captured_exit_code": expected_exit,
                "replayed_exit_code": evaluation.returncode,
                "binary_sha256": binary_hash,
                "predicates": predicates,
                "matched": matched,
            })
        except Exception as exc:
            failures.append(label)
            receipt["cases"].append({"label": label, "matched": False, "error": str(exc)})

    if len(binary_hashes) > 1:
        failures.append("binary_hash_divergence")
    receipt["binary_sha256"] = next(iter(binary_hashes), None)
    receipt["cases_total"] = len(receipt["cases"])
    receipt["cases_matched"] = sum(1 for case in receipt["cases"] if case.get("matched"))
    receipt["overall_result"] = "PASS" if not failures and receipt["cases_total"] == 2 else "FAIL"
    receipt["failures"] = failures

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        f"CEDAR SAME-ENVIRONMENT REPLAY: {receipt['overall_result']} "
        f"matched={receipt['cases_matched']}/{receipt['cases_total']} -> {args.output}"
    )
    return 0 if receipt["overall_result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
