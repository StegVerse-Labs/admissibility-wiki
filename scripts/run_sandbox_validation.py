#!/usr/bin/env python3
"""Run the admissibility-wiki ST-017 profile in an isolated repository copy."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "templates/sandbox-first/admissibility-wiki.sandbox-profile.json"
REPORT = ROOT / "reports/sandbox-first-validation.report.json"


def ignore(_directory: str, names: list[str]) -> set[str]:
    excluded = {".git", "node_modules", "build", ".docusaurus", "__pycache__", ".pytest_cache"}
    return {name for name in names if name in excluded}


def main() -> int:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    results: list[dict[str, object]] = []
    started = time.time()
    sandbox_status = "PASS"

    with tempfile.TemporaryDirectory(prefix="admissibility-wiki-st017-") as temp_dir:
        sandbox = Path(temp_dir) / "repo"
        shutil.copytree(ROOT, sandbox, ignore=ignore)
        (sandbox / "reports").mkdir(parents=True, exist_ok=True)

        for item in profile["commands"]:
            command = item["command"]
            command_started = time.time()
            try:
                completed = subprocess.run(
                    command,
                    cwd=sandbox,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=item.get("timeout_seconds", 900),
                    check=False,
                )
                return_code = completed.returncode
                output = completed.stdout
            except subprocess.TimeoutExpired as exc:
                return_code = 124
                output = (exc.stdout or "") + "\nTIMEOUT"
            status = "PASS" if return_code == 0 else "FAIL"
            results.append({
                "id": item["id"],
                "command": command,
                "status": status,
                "return_code": return_code,
                "duration_seconds": round(time.time() - command_started, 3),
                "output": output[-12000:],
            })
            if status == "FAIL":
                sandbox_status = "FAIL"
                break

    report = {
        "schema": "stegverse.st017.sandbox_validation.v1",
        "repository": profile["repository"],
        "profile": str(PROFILE.relative_to(ROOT)),
        "sandbox_status": sandbox_status,
        "github_actions_status": "NOT_OBSERVED",
        "public_output_status": "NOT_VERIFIED",
        "commands_total": len(profile["commands"]),
        "commands_executed": len(results),
        "commands_passed": sum(result["status"] == "PASS" for result in results),
        "duration_seconds": round(time.time() - started, 3),
        "results": results,
        "authority": {
            "runtime_execution_authorized": False,
            "artifact_promotion_authorized": False,
            "canonical_status_mutation_authorized": False,
            "deployment_authorized": False,
            "public_verification_claimed": False,
            "release_authorized": False,
            "downstream_propagation_authorized": False,
            "standing_granted": False,
            "admissibility_granted": False,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"SANDBOX: {sandbox_status}")
    for result in results:
        print(f"{result['id']}: {result['status']}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0 if sandbox_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
