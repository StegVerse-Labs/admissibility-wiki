#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "static/data/governed-framework-reviews/ta-14.claim-architecture-analysis.v1.json"
LEDGER = ROOT / "static/data/governed-framework-reviews/ta-14.claim-architecture-source-ledger.v1.json"
PAGE = ROOT / "docs/external-frameworks/ta-14-claim-architecture-analysis.md"
HANDOFF = ROOT / "docs/external-frameworks/TA14_CLAIM_ARCHITECTURE_ANALYSIS_MIRROR_HANDOFF.md"
SIDEBAR = ROOT / "sidebars.js"

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

REQUIRED_CLAIMS = {f"TA14-CA-{n:03d}" for n in range(1, 13)}
REQUIRED_PAGE_MARKERS = [
    "# TA-14 Claim-versus-Architecture Analysis",
    "## Claim-to-architecture matrix",
    "## Material publicly unresolved claims",
    "## Open discriminating tests",
    "## Correction policy",
    "ta-14.claim-architecture-analysis.v1.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for path in (ANALYSIS, LEDGER, PAGE, HANDOFF, SIDEBAR):
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")

analysis = json.loads(ANALYSIS.read_text())
ledger = json.loads(LEDGER.read_text())
page = PAGE.read_text()
handoff = HANDOFF.read_text()
sidebar = SIDEBAR.read_text()

claims = analysis.get("claims")
if not isinstance(claims, list):
    fail("analysis claims must be a list")

ids = {claim.get("claim_id") for claim in claims}
if ids != REQUIRED_CLAIMS:
    fail(f"claim IDs mismatch: expected {sorted(REQUIRED_CLAIMS)}, got {sorted(ids)}")

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
if not analysis.get("method_rules", {}).get("parentage_requires_positive_evidence"):
    fail("parentage positive-evidence rule must be enabled")
if analysis.get("comparative_boundary", {}).get("stegverse_comparison_state") != "SECONDARY_PENDING_TA14_INTERNAL_ANALYSIS":
    fail("StegVerse comparison must remain secondary in v1")

for marker in REQUIRED_PAGE_MARKERS:
    if marker not in page:
        fail(f"public page missing marker: {marker}")

if "external-frameworks/ta-14-claim-architecture-analysis" not in sidebar:
    fail("analysis page is not bound into External Frameworks sidebar")

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

print("PASS: TA-14 claim-versus-architecture analysis is internally consistent and navigation-bound")
