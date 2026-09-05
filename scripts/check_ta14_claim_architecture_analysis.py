#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json"
LEDGER = ROOT / "static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json"
PAGE = ROOT / "docs/external-frameworks/ta-14-claim-architecture-analysis.md"
HANDOFF = ROOT / "docs/external-frameworks/TA14_CLAIM_ARCHITECTURE_ANALYSIS_MIRROR_HANDOFF.md"
SIDEBAR = ROOT / "sidebars.js"
ASSOCIATIONS = ROOT / "static/external-frameworks/sidebar-page-associations.v1.json"

ALLOWED = {
    "CLAIM_OBSERVED",
    "ARCHITECTURE_SUPPORT_OBSERVED",
    "BEHAVIOR_OBSERVED",
    "IMPLEMENTATION_EVIDENCE_OBSERVED",
    "PARTIALLY_SUPPORTED",
    "PUBLICLY_UNRESOLVED",
    "CONTRADICTED_BY_PUBLIC_ARCHITECTURE",
    "NOT_YET_FOUND",
    "OUT_OF_SCOPE",
}

REQUIRED_CLAIMS = {f"TA14-CA-{n:03d}" for n in range(1, 14)}
REQUIRED_FAMILIES = {
    "eight_stage_route",
    "admissibility_before_consequence",
    "authority_and_standing_lifecycle",
    "binding_and_commit",
    "fail_closed_execution_boundary",
    "continuity_and_custody",
    "outcome_correspondence",
    "replay_and_reconstruction",
    "cross_domain_scope",
    "complete_mediation_non_bypassability",
    "parent_architecture",
    "independent_reciprocal_evaluation",
    "registry_provenance_versioned_governance_records",
}
REQUIRED_PAGE_MARKERS = [
    "# TA-14 Claim-versus-Architecture Analysis",
    "## Claim-to-architecture matrix",
    "## Material publicly unresolved claims",
    "## Open discriminating tests",
    "## Correction policy",
    "ta-14.claim-architecture-analysis.v1.json",
    "ta-14.claim-architecture-source-ledger.v1.json",
    "Registry / provenance / versioned records",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for path in (ANALYSIS, LEDGER, PAGE, HANDOFF, SIDEBAR, ASSOCIATIONS):
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")

analysis = json.loads(ANALYSIS.read_text())
ledger = json.loads(LEDGER.read_text())
associations = json.loads(ASSOCIATIONS.read_text())
page = PAGE.read_text()
handoff = HANDOFF.read_text()
sidebar = SIDEBAR.read_text()

claims = analysis.get("claims")
if not isinstance(claims, list):
    fail("analysis claims must be a list")

ids = {claim.get("claim_id") for claim in claims}
if ids != REQUIRED_CLAIMS:
    fail(f"claim IDs mismatch: expected {sorted(REQUIRED_CLAIMS)}, got {sorted(ids)}")
families = {claim.get("claim_family") for claim in claims}
if families != REQUIRED_FAMILIES:
    fail("initial claim-family coverage is incomplete or contains drift")

for claim in claims:
    status = claim.get("status")
    if status not in ALLOWED:
        fail(f"{claim.get('claim_id')} has invalid status {status}")
    if status == "PUBLICLY_UNRESOLVED" and not claim.get("open_test"):
        fail(f"{claim.get('claim_id')} is PUBLICLY_UNRESOLVED without an open test")
    for field in ("claim_family", "claim_summary", "claimed_architectural_location", "confidence", "reasoning_summary"):
        if not claim.get(field):
            fail(f"{claim.get('claim_id')} missing {field}")

if analysis.get("framework_id") != "ta-14":
    fail("analysis framework_id must be ta-14")
if analysis.get("authority_effect") != "NONE":
    fail("analysis authority_effect must remain NONE")
if analysis.get("source_ledger") != "static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json":
    fail("analysis source ledger binding is missing or incorrect")
if not analysis.get("method_rules", {}).get("parentage_requires_positive_evidence"):
    fail("parentage positive-evidence rule must be enabled")
if analysis.get("comparative_boundary", {}).get("stegverse_comparison_state") != "SECONDARY_PENDING_TA14_INTERNAL_ANALYSIS":
    fail("StegVerse comparison must remain secondary in v1")

for marker in REQUIRED_PAGE_MARKERS:
    if marker not in page:
        fail(f"public page missing marker: {marker}")

route = "external-frameworks/ta-14-claim-architecture-analysis"
if route not in sidebar:
    fail("analysis page is not bound into External Frameworks sidebar")
association_entries = associations.get("entries", [])
matching = [entry for entry in association_entries if entry.get("sidebar_route") == route]
if len(matching) != 1 or matching[0].get("page_type") != "support":
    fail("analysis page is not correctly bound into sidebar association ledger")
if associations.get("counts", {}).get("sidebar_entries") != len(association_entries):
    fail("sidebar association count is stale")

if "source_revision_ledger: INSTALLED" not in handoff:
    fail("handoff does not record installed source revision ledger")
if "validator: INSTALLED" not in handoff:
    fail("handoff does not record installed validator")
if "navigation_binding: INSTALLED" not in handoff:
    fail("handoff does not record installed navigation binding")

sources = ledger.get("sources")
if not isinstance(sources, list) or not sources:
    fail("source ledger must contain sources")
source_ids = {source.get("source_id") for source in sources}
if "TA14-SRC-20260904-001" not in source_ids:
    fail("supplied 2026-09-04 TA-14 public page is not recorded in source ledger")

external = next(source for source in sources if source.get("source_id") == "TA14-SRC-20260904-001")
if external.get("exact_byte_snapshot") == "NOT_CAPTURED" and external.get("content_hash") is not None:
    fail("external source cannot claim a content hash without exact-byte snapshot")

print("PASS: TA-14 claim-versus-architecture analysis is internally consistent, source-bound, and navigation-bound")
