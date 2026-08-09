#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "external-frameworks" / "cedar"
STATUS = REPORTS / "cedar-capture-status.json"
REPLAY_SCRIPT = ROOT / "scripts" / "run_cedar_same_environment_replay.py"
REPLAY_RECEIPT = REPORTS / "cedar-same-environment-replay-receipt.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected object: {path}")
    return payload


def run_same_environment_replay(captures: dict[str, Path]) -> tuple[str, str]:
    if not REPLAY_SCRIPT.exists():
        return "FAIL", f"replay script missing: {REPLAY_SCRIPT.relative_to(ROOT)}"
    completed = subprocess.run(
        [
            sys.executable,
            str(REPLAY_SCRIPT),
            "--allow-capture",
            str(captures["allow"]),
            "--deny-capture",
            str(captures["deny"]),
            "--output",
            str(REPLAY_RECEIPT),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout.rstrip()
    if completed.returncode != 0:
        return "FAIL", output or f"same-environment replay exited {completed.returncode}"
    try:
        receipt = load(REPLAY_RECEIPT)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return "FAIL", f"same-environment replay receipt invalid: {exc}"
    if receipt.get("overall_result") != "PASS" or receipt.get("cases_total") != 2 or receipt.get("cases_matched") != 2:
        return "FAIL", "same-environment replay receipt predicates did not pass"
    return "PASS", output


def main() -> int:
    failures: list[str] = []
    captures = {
        "allow": REPORTS / "cedar-allow-capture.json",
        "deny": REPORTS / "cedar-deny-capture.json",
    }

    for label, path in captures.items():
        if not path.exists():
            failures.append(f"missing {label} capture: {path.relative_to(ROOT)}")
            continue
        try:
            receipt = load(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            failures.append(f"invalid {label} capture: {exc}")
            continue

        if receipt.get("artifact_type") != "external_framework_observed_evidence_capture":
            failures.append(f"{label} artifact_type mismatch")
        if receipt.get("framework_id") != "cedar-policy":
            failures.append(f"{label} framework_id mismatch")
        if receipt.get("capture_state") != "captured_unverified":
            failures.append(f"{label} capture_state must remain captured_unverified")

        runtime = receipt.get("runtime", {})
        for key in ["implementation_id", "version_command", "version_output", "evaluate_command", "exit_code"]:
            if key not in runtime:
                failures.append(f"{label} runtime missing {key}")

        hashes = receipt.get("hashes", {})
        for key in ["policy_sha256", "request_sha256", "stdout_sha256", "stderr_sha256"]:
            value = hashes.get(key)
            if not isinstance(value, str) or len(value) != 64:
                failures.append(f"{label} missing valid {key}")

        authority = receipt.get("authority_context", {})
        for key in [
            "cedar_decision_is_execution_authority",
            "capture_is_stegverse_standing",
            "capture_is_compatibility_proof",
            "current_delegation_attached",
            "commit_time_authority_reconstructed",
        ]:
            if authority.get(key) is not False:
                failures.append(f"{label} authority boundary must keep {key}=false")

        replay = receipt.get("replay", {})
        if not replay.get("version_command") or not replay.get("evaluate_command"):
            failures.append(f"{label} replay commands missing")
        if not receipt.get("limitations"):
            failures.append(f"{label} limitations missing")

    replay_state = "not_performed"
    replay_output = ""
    if not failures:
        replay_state, replay_output = run_same_environment_replay(captures)
        if replay_state != "PASS":
            failures.append(f"same-environment replay failed: {replay_output}")

    STATUS.parent.mkdir(parents=True, exist_ok=True)
    status = {
        "artifact_type": "external_framework_capture_validation_status",
        "schema_version": "0.2",
        "framework_id": "cedar-policy",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_status": "FAIL" if failures else "PASS",
        "capture_state": "captured_unverified",
        "same_environment_replay_state": "observed_pass" if replay_state == "PASS" else replay_state,
        "fresh_runner_replay_state": "not_performed",
        "independent_implementation_or_provider_review": "not_performed",
        "compatibility_state": "not_claimed",
        "standing_state": "not_created",
        "execution_authority_state": "not_created",
        "artifacts": {
            **{
                label: {
                    "present": path.exists(),
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path) if path.exists() else None,
                }
                for label, path in captures.items()
            },
            "same_environment_replay": {
                "present": REPLAY_RECEIPT.exists(),
                "path": str(REPLAY_RECEIPT.relative_to(ROOT)),
                "sha256": sha256(REPLAY_RECEIPT) if REPLAY_RECEIPT.exists() else None,
            },
        },
        "same_environment_replay_output": replay_output[-4000:],
        "validation_failures": failures,
        "authority_boundary": {
            "validation_is_execution_authority": False,
            "capture_is_compatibility_proof": False,
            "replay_is_compatibility_proof": False,
            "capture_creates_standing": False,
            "replay_creates_standing": False,
            "implementation_identification_is_certification": False,
        },
    }
    STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")

    print("CEDAR CAPTURE ARTIFACT VALIDATION:", status["overall_status"])
    print(f"same_environment_replay_state={status['same_environment_replay_state']}")
    if replay_output:
        print(replay_output)
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
