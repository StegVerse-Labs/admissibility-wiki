#!/usr/bin/env python3
from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "workflow_manifest.json"


def read_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def run_command(command: str) -> tuple[int, str]:
    result = subprocess.run(
        shlex.split(command),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout


def main() -> int:
    if not MANIFEST.exists():
        print("CANONICAL VALIDATION: FAIL")
        print("- workflow manifest missing")
        return 1

    manifest = read_manifest()
    commands = manifest.get("verification_commands", [])
    if not isinstance(commands, list) or not commands:
        print("CANONICAL VALIDATION: FAIL")
        print("- no verification commands declared")
        return 1

    failures: list[str] = []
    for command in commands:
        if not isinstance(command, str) or not command.strip():
            failures.append("invalid verification command declaration")
            continue
        print(f"$ {command}")
        returncode, output = run_command(command)
        if output:
            print(output, end="" if output.endswith("\n") else "\n")
        if returncode != 0:
            failures.append(f"{command} exited {returncode}")

    print("CANONICAL VALIDATION:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
