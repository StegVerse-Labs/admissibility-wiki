#!/usr/bin/env python3
"""Validate the StegVerse quantum-resilient complete-security publication package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "static/status/quantum-resilient-security-publication-status.json"
SIDEBAR = ROOT / "sidebars.js"
PACKAGE = ROOT / "package.json"

REQUIRED_FILES = (
    ROOT / "docs/STEGVERSE_QUANTUM_SECURITY_MIRROR_HANDOFF.md",
    ROOT / "docs/research/stegverse-complete-security-paper.md",
    ROOT / "docs/research/stegverse-complete-security-paper.tex",
    ROOT / "docs/research/references.bib",
    ROOT / "docs/social/stegverse-quantum-security-carousel.md",
    ROOT / "docs/governance/quantum-resilient-execution-security.md",
    ROOT / "simulations/quantum_execution_security_model.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"QUANTUM RESILIENT SECURITY PUBLICATION: FAIL - {message}")


def main() -> None:
    for path in REQUIRED_FILES:
        require(path.is_file(), f"missing required publication file: {path.relative_to(ROOT)}")

    require(STATUS.is_file(), f"missing status artifact: {STATUS.relative_to(ROOT)}")
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))

    paper = REQUIRED_FILES[1].read_text(encoding="utf-8")
    governance = REQUIRED_FILES[5].read_text(encoding="utf-8")
    handoff = REQUIRED_FILES[0].read_text(encoding="utf-8")
    combined = "\n".join(path.read_text(encoding="utf-8") for path in REQUIRED_FILES if path.suffix in {".md", ".tex", ".bib"})

    required_paper_markers = (
        "Abstract",
        "communication trust",
        "execution trust",
        "state-bound execution authority",
        "commit-time admissibility",
        "ML-KEM",
        "ML-DSA",
        "SLH-DSA",
        "reconstructability",
        "recoverability",
    )
    for marker in required_paper_markers:
        require(marker.lower() in paper.lower(), f"paper missing required marker: {marker}")

    required_governance_markers = (
        "ALLOW",
        "DENY",
        "FAIL_CLOSED",
        "verification",
        "execution authority",
        "quantum-resilient",
    )
    for marker in required_governance_markers:
        require(marker.lower() in governance.lower(), f"governance page missing required marker: {marker}")

    require("governance/quantum-resilient-execution-security" in sidebar, "governance page is not present in sidebars.js")
    require("research/stegverse-complete-security-paper" in sidebar, "research paper is not present in sidebars.js")
    require("social/stegverse-quantum-security-carousel" in sidebar, "carousel source is not present in sidebars.js")

    scripts = package.get("scripts", {})
    require("validate:quantum-resilient-security-publication" in scripts, "package.json is missing the dedicated validator command")
    require("validate:quantum-resilient-security-publication" in scripts.get("validate", ""), "dedicated validator is not integrated into npm run validate")

    claim_boundary = status.get("claim_boundary", {})
    require(claim_boundary.get("unconditional_quantum_proof_claim") is False, "unconditional quantum-proof claim must remain false")
    require(claim_boundary.get("post_quantum_cryptography_is_sufficient_for_execution_authority") is False, "PQC must not be treated as sufficient execution authority")
    require(claim_boundary.get("publication_grants_execution_authority") is False, "publication must not grant execution authority")
    require(status.get("manual_task_requirement") == "none", "manual task requirement must remain none")
    require(status.get("user_manual_action_required") is False, "user manual action must remain false")
    require(status.get("downstream_mutation_authority") == "none_granted", "downstream mutation authority must remain ungranted")

    forbidden_claims = (
        "unconditionally quantum proof",
        "guaranteed quantum proof",
        "immune to all quantum attacks",
        "post-quantum cryptography guarantees execution authority",
    )
    lowered = combined.lower()
    for phrase in forbidden_claims:
        require(phrase not in lowered, f"unsupported claim detected: {phrase}")

    require("Issue #20" in handoff or "issue 20" in handoff.lower(), "handoff does not identify the durable issue")
    require("PR #21" in handoff or "pull request 21" in handoff.lower(), "handoff does not identify the draft pull request")

    simulation = ROOT / "simulations/quantum_execution_security_model.py"
    result = subprocess.run(
        [sys.executable, str(simulation)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"simulation failed: {result.stderr.strip() or result.stdout.strip()}")
    require("PASS" in result.stdout, "simulation did not emit PASS")

    print("QUANTUM RESILIENT SECURITY PUBLICATION: PASS")


if __name__ == "__main__":
    main()
