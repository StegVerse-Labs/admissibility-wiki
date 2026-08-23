#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-chain-continuation.yml"
IOS_MIRROR = ROOT / "iosnoperiod" / "github" / "workflows" / "validate-chain-continuation.yml"
IOS_STATUS = ROOT / "static" / "status" / "ios-workflow-mirror-status.json"
ROUTE_VALIDATOR = ROOT / "scripts" / "check_external_framework_public_routes.py"
ASSOCIATIONS = ROOT / "static" / "external-frameworks" / "sidebar-page-associations.v1.json"
HANDOFF = ROOT / "docs" / "external-frameworks" / "EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md"
EXPECTED_FRAMEWORK_COUNT = 36


def require_marker(text: str, marker: str, failures: list[str], label: str) -> None:
    if marker not in text:
        failures.append(f"missing {label}: {marker}")


def require_order(text: str, markers: list[str], failures: list[str], label: str) -> None:
    positions: list[int] = []
    for marker in markers:
        pos = text.find(marker)
        if pos < 0:
            failures.append(f"{label} missing marker: {marker}")
            return
        positions.append(pos)
    if positions != sorted(positions):
        failures.append(f"{label} order mismatch: {' -> '.join(markers)}")


def main() -> int:
    failures: list[str] = []
    for path in (WORKFLOW, IOS_MIRROR, IOS_STATUS, ROUTE_VALIDATOR, ASSOCIATIONS, HANDOFF):
        if not path.exists():
            failures.append(f"missing required path: {path.relative_to(ROOT)}")
    if failures:
        print("EXTERNAL FRAMEWORK PUBLICATION PROOF CONTRACT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    workflow = WORKFLOW.read_text(encoding="utf-8")
    route_validator = ROUTE_VALIDATOR.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    associations = json.loads(ASSOCIATIONS.read_text(encoding="utf-8"))
    ios_status = json.loads(IOS_STATUS.read_text(encoding="utf-8"))
    frameworks = [entry for entry in associations.get("entries", []) if entry.get("page_type") == "framework"]

    if len(frameworks) != EXPECTED_FRAMEWORK_COUNT:
        failures.append(f"expected {EXPECTED_FRAMEWORK_COUNT} framework associations, found {len(frameworks)}")

    if WORKFLOW.read_bytes() != IOS_MIRROR.read_bytes():
        failures.append("iOS-safe workflow mirror does not exactly match canonical workflow")
    if ios_status.get("status") != "synchronized":
        failures.append("iOS workflow mirror status is not synchronized")
    ios_boundary = ios_status.get("boundary", {})
    if ios_boundary.get("canonical_workflow_remains_source_of_truth") is not True:
        failures.append("iOS mirror status does not preserve canonical-workflow source-of-truth boundary")
    if ios_boundary.get("mirror_is_activation_evidence") is not False:
        failures.append("iOS mirror status incorrectly grants activation evidence")
    if ios_boundary.get("mirror_must_not_be_used_as_current_workflow_until_synced") is not False:
        failures.append("synchronized iOS mirror status still carries stale-use prohibition")

    route_markers = [
        "--source-only",
        "--built-site",
        "--build-dir",
        "source-route-contract.json",
        "built-route-verification.json",
        "public-route-verification.json",
        "SOURCE_ONLY",
        "BUILT_SITE",
        "DEPLOYED_PUBLIC_ROUTE",
        "EXPECTED_FRAMEWORK_COUNT = 36",
    ]
    for marker in route_markers:
        require_marker(route_validator, marker, failures, "route-validator contract marker")

    workflow_markers = [
        "python scripts/check_external_framework_public_routes.py --source-only",
        "name: external-framework-source-route-contract",
        "path: reports/external-frameworks/source-route-contract.json",
        "run: npm run build",
        "run: test \"${{ steps.site-build.outcome }}\" = \"success\"",
        "python scripts/check_external_framework_public_routes.py --built-site --build-dir build",
        "name: external-framework-built-route-verification",
        "path: reports/external-frameworks/built-route-verification.json",
        "uses: actions/upload-pages-artifact@v3",
        "uses: actions/deploy-pages@v4",
        "python scripts/check_external_framework_public_routes.py",
        "name: external-framework-public-route-verification",
        "path: reports/external-frameworks/public-route-verification.json",
    ]
    for marker in workflow_markers:
        require_marker(workflow, marker, failures, "workflow proof marker")

    require_order(
        workflow,
        [
            "python scripts/check_external_framework_public_routes.py --source-only",
            "- name: Setup Node",
            "run: npm run build",
            "run: test \"${{ steps.site-build.outcome }}\" = \"success\"",
            "python scripts/check_external_framework_public_routes.py --built-site --build-dir build",
            "uses: actions/upload-pages-artifact@v3",
            "uses: actions/deploy-pages@v4",
            "python scripts/check_external_framework_public_routes.py\n",
        ],
        failures,
        "source-build-deploy-public proof chain",
    )

    require_order(
        workflow,
        [
            "python scripts/check_external_framework_public_routes.py --source-only",
            "name: external-framework-source-route-contract",
        ],
        failures,
        "source-route artifact binding",
    )
    require_order(
        workflow,
        [
            "python scripts/check_external_framework_public_routes.py --built-site --build-dir build",
            "name: external-framework-built-route-verification",
            "uses: actions/upload-pages-artifact@v3",
        ],
        failures,
        "built-route artifact binding",
    )
    require_order(
        workflow,
        [
            "python scripts/check_external_framework_public_routes.py\n",
            "name: external-framework-public-route-verification",
        ],
        failures,
        "deployed-route artifact binding",
    )

    handoff_markers = [
        "36/36 source wiring",
        "source-route contract",
        "36/36 generated-route verification",
        "36/36 public route/content verification",
        "framework-specific evidence completion",
        "source-route contract PASS != successful Docusaurus build",
        "route verification != release",
    ]
    for marker in handoff_markers:
        require_marker(handoff, marker, failures, "handoff boundary marker")

    print("EXTERNAL FRAMEWORK PUBLICATION PROOF CONTRACT:", "FAIL" if failures else "PASS")
    print(f"framework_associations={len(frameworks)}/{EXPECTED_FRAMEWORK_COUNT}")
    print("proof_stages=source_route_contract,built_route_verification,deployed_public_route_verification")
    print("pages_artifact_requires_built_route_verification=true")
    print(f"ios_workflow_mirror_synchronized={WORKFLOW.read_bytes() == IOS_MIRROR.read_bytes()}")
    print("authority_effect=NONE")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
