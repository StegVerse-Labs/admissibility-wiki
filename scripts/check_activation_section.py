#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "activation" / "github-pages-cloudflare.md"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
CONFIG = ROOT / "docusaurus.config.js"
STATUS = ROOT / "static" / "activation" / "activation-section-completeness.v1.json"
CNAME = ROOT / "static" / "CNAME"

REQUIRED_GUIDE_MARKERS = [
    "https://stegverse-labs.github.io/admissibility-wiki/",
    ".github/workflows/validate-chain-continuation.yml",
    "Validation job: validate-chain-continuation",
    "Build job: build-pages",
    "Deployment job: deploy-pages",
    "Public verification job: verify-public-pages",
    "Manual task requirement: none",
    "User manual action required: false",
    "custom_domain: not_configured",
    "static/CNAME: absent",
    "workflow configuration != workflow pass",
    "publication receipt != execution authority",
]
FORBIDDEN_GUIDE_MARKERS = [
    ".github/workflows/deploy.yml",
    "run the deploy workflow manually",
    "Settings → Pages → Source",
]
REQUIRED_WORKFLOW_MARKERS = [
    "name: Validate chain continuation",
    "validate-chain-continuation:",
    "build-pages:",
    "deploy-pages:",
    "verify-public-pages:",
    "uses: actions/deploy-pages@v4",
    "name: full-validation-chain-report",
]
REQUIRED_CONFIG_MARKERS = [
    "url: 'https://stegverse-labs.github.io'",
    "baseUrl: '/admissibility-wiki/'",
    "organizationName: 'StegVerse-Labs'",
    "projectName: 'admissibility-wiki'",
    "onBrokenLinks: 'throw'",
]


def main() -> int:
    failures: list[str] = []
    for path in [GUIDE, WORKFLOW, CONFIG, STATUS]:
        if not path.exists():
            failures.append(f"missing path: {path.relative_to(ROOT)}")
    if CNAME.exists():
        failures.append("static/CNAME must remain absent for github.io project hosting")
    if failures:
        print("ACTIVATION SECTION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    guide = GUIDE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    config = CONFIG.read_text(encoding="utf-8")
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    for marker in REQUIRED_GUIDE_MARKERS:
        if marker not in guide:
            failures.append(f"activation guide missing marker: {marker}")
    for marker in FORBIDDEN_GUIDE_MARKERS:
        if marker in guide:
            failures.append(f"activation guide contains stale or manual marker: {marker}")
    for marker in REQUIRED_WORKFLOW_MARKERS:
        if marker not in workflow:
            failures.append(f"canonical workflow missing marker: {marker}")
    for marker in REQUIRED_CONFIG_MARKERS:
        if marker not in config:
            failures.append(f"Docusaurus config missing marker: {marker}")

    if status.get("schema") != "admissibility_wiki_activation_section_completeness.v1":
        failures.append("activation status schema mismatch")
    if status.get("classification") != "COMPLETE_WITH_EXTERNAL_GATES":
        failures.append("activation section classification mismatch")
    if status.get("canonical_workflow") != ".github/workflows/validate-chain-continuation.yml":
        failures.append("activation canonical workflow reference mismatch")
    counts = status.get("counts", {})
    if counts.get("activation_guides") != 1:
        failures.append("activation guide count is stale")
    if counts.get("canonical_active_workflows") != 1:
        failures.append("canonical active workflow count is stale")
    if counts.get("custom_domains") != 0:
        failures.append("custom domain count must remain zero")
    if counts.get("manual_user_tasks") != 0:
        failures.append("manual user task count must remain zero")
    for key, value in status.get("boundaries", {}).items():
        if value is not False:
            failures.append(f"activation boundary must be false: {key}")

    print("ACTIVATION SECTION:", "FAIL" if failures else "PASS")
    print("canonical_active_workflows=1")
    print("manual_user_tasks=0")
    print("custom_domains=0")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
