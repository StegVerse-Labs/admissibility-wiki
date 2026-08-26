#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"


def fail(message: str) -> None:
    raise SystemExit(f"CANONICAL ORCHESTRATION CONTRACT: FAIL: {message}")


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    header = text.split("jobs:", 1)[0]

    if "schedule:" in header or "cron:" in header:
        if "external-framework-worker-heartbeat:" not in text:
            fail("scheduled continuation must retain the bounded worker-heartbeat job")
    if "cancel-in-progress: true" not in header:
        fail("superseded runs must be cancelled")
    if "cancel-in-progress: false" in text:
        fail("obsolete-run retention is prohibited")
    if "push:\n    branches:\n      - main" not in header:
        fail("push execution must be restricted to main")
    if "pull_request:" not in header:
        fail("pull requests must retain validation coverage")
    if "workflow_dispatch:" not in header:
        fail("explicit operator validation must remain available")

    required_chain = [
        "needs: validate-chain-continuation",
        "needs: build-pages",
        "needs: deploy-pages",
    ]
    for marker in required_chain:
        if marker not in text:
            fail(f"missing ordered dependency: {marker}")

    print("CANONICAL ORCHESTRATION CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
