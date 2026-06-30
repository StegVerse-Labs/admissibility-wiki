#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_external_framework_page_status.py"
BOUNDARY_CHECK = ROOT / "scripts" / "check_external_framework_page_analysis_boundary.py"
CANDIDATE_CHECK = ROOT / "scripts" / "check_external_framework_page_candidates.py"
SURFACE_CHECK = ROOT / "scripts" / "check_external_framework_page_surfaces.py"
SURFACE_HANDOFF_CHECK = ROOT / "scripts" / "check_generated_page_surfaces_handoff.py"
ROOT_ADDENDUM_CHECK = ROOT / "scripts" / "check_generated_page_surfaces_root_addendum.py"
WORKFLOW_MIGRATION_CHECK = ROOT / "scripts" / "check_generated_page_workflow_entrypoint_migration.py"
ENTRYPOINT_PROPAGATION_CHECK = ROOT / "scripts" / "check_generated_page_entrypoint_closeout_propagation.py"
RELEASE_EVIDENCE_CHECK = ROOT / "scripts" / "check_generated_page_release_evidence_bundle.py"
CI_EVIDENCE_SURFACE_CHECK = ROOT / "scripts" / "check_generated_page_ci_evidence_surface.py"
CI_EVIDENCE_HANDOFF_CHECK = ROOT / "scripts" / "check_generated_page_ci_evidence_surface_handoff.py"
SUBSYSTEM_CAPABILITY_CHECK = ROOT / "scripts" / "check_generated_page_subsystem_capability.py"
REGISTRY = ROOT / "docs" / "external-frameworks" / "index.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_external_framework_page_status", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load page-status generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_check(path: Path, label: str, failures: list[str]) -> None:
    if path.exists():
        result = subprocess.run(["python", str(path)], check=False)
        if result.returncode != 0:
            failures.append(f"{label} failed")


def main() -> int:
    failures: list[str] = []
    if not GENERATOR.exists():
        failures.append("page-status generator missing")
    if not REGISTRY.exists():
        failures.append("registry missing")
    if failures:
        print("EXTERNAL FRAMEWORK PAGE STATUS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    tracked = sorted((ROOT / "docs" / "external-frameworks").glob("*.md"))
    original = {path: path.read_text(encoding="utf-8") for path in tracked}
    generator = load_generator()

    generator.main()
    generated_once = {path: path.read_text(encoding="utf-8") for path in tracked}
    generator.main()
    generated_twice = {path: path.read_text(encoding="utf-8") for path in tracked}

    changed = [path.relative_to(ROOT).as_posix() for path in tracked if generated_once[path] != generated_twice[path]]
    for path, text in original.items():
        path.write_text(text, encoding="utf-8")

    if changed:
        failures.append("page-status generator is not idempotent: " + ", ".join(changed))

    run_check(BOUNDARY_CHECK, "analysis boundary check", failures)
    run_check(CANDIDATE_CHECK, "page candidate state check", failures)
    run_check(SURFACE_CHECK, "page surface inventory check", failures)
    run_check(SURFACE_HANDOFF_CHECK, "page surface handoff check", failures)
    run_check(ROOT_ADDENDUM_CHECK, "page surface root addendum check", failures)
    run_check(WORKFLOW_MIGRATION_CHECK, "workflow entrypoint migration check", failures)
    run_check(ENTRYPOINT_PROPAGATION_CHECK, "entrypoint closeout propagation check", failures)
    run_check(RELEASE_EVIDENCE_CHECK, "release evidence bundle check", failures)
    run_check(CI_EVIDENCE_SURFACE_CHECK, "CI evidence surface check", failures)
    run_check(CI_EVIDENCE_HANDOFF_CHECK, "CI evidence handoff check", failures)
    run_check(SUBSYSTEM_CAPABILITY_CHECK, "subsystem capability check", failures)

    print("EXTERNAL FRAMEWORK PAGE STATUS:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
