from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "llm-free-tier-trust-chain.md"
SIDEBAR = ROOT / "sidebars.js"
README = ROOT / "README.md"
SITE_HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
AUTOMATION_HANDOFF = ROOT / "ADMISSIBILITY_AUTOMATION_HANDOFF.md"
REFERENCES = ROOT / "static" / "status" / "llm-free-tier-trust-chain-artifact-references.v1.json"

REQUIRED_PAGE_TEXT = [
    "LLM Free Tier Trust Chain",
    "StegVerse-org/LLM-adapter",
    "free_tier_trust metadata",
    "StegVerse-Labs/Site",
    "ecosystem-chat.html",
    "scripts/check_site_llm_free_tier_trust.py",
    "StegVerse-org/StegVerse-SDK",
    "quota availability is not admissibility",
    "receipt_export_is_permanent_retention == false",
    "reconstruction_grants_commit_time_standing == false",
]
REQUIRED_ARTIFACT_REFERENCES = {
    "adapter.capabilities.json",
    "site-public-mirror-status-guard.yml",
    "validate_free_tier_metadata",
    "sdk-demo-test.yml",
}
REQUIRED_SIDEBAR_TEXT = ["governance/llm-free-tier-trust-chain"]
REQUIRED_README_TEXT = [
    "docs/governance/llm-free-tier-trust-chain.md",
    "bounded free-tier trust chain",
]
REQUIRED_HANDOFF_TEXT = [
    "LLM free-tier trust chain",
    "docs/governance/llm-free-tier-trust-chain.md",
    "scripts/check_llm_free_tier_trust_chain.py",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    errors: list[str] = []
    page_text = _read(PAGE)
    sidebar_text = _read(SIDEBAR)
    readme_text = _read(README)
    handoff_text = _read(SITE_HANDOFF) + "\n" + _read(AUTOMATION_HANDOFF)

    for path, label in [
        (PAGE, "page"),
        (SIDEBAR, "sidebar"),
        (README, "readme"),
        (REFERENCES, "artifact_references"),
    ]:
        if not path.exists():
            errors.append("missing_" + label)
    if not SITE_HANDOFF.exists() and not AUTOMATION_HANDOFF.exists():
        errors.append("missing_handoff")

    for item in REQUIRED_PAGE_TEXT:
        if item not in page_text:
            errors.append("page_missing:" + item)
    for item in REQUIRED_SIDEBAR_TEXT:
        if item not in sidebar_text:
            errors.append("sidebar_missing:" + item)
    for item in REQUIRED_README_TEXT:
        if item not in readme_text:
            errors.append("readme_missing:" + item)
    for item in REQUIRED_HANDOFF_TEXT:
        if item not in handoff_text:
            errors.append("handoff_missing:" + item)

    if REFERENCES.exists():
        data = json.loads(REFERENCES.read_text(encoding="utf-8"))
        if data.get("schema") != "llm_free_tier_trust_chain_artifact_references.v1":
            errors.append("artifact_references_schema_mismatch")
        if data.get("doctrine") != "docs/governance/llm-free-tier-trust-chain.md":
            errors.append("artifact_references_doctrine_mismatch")
        entries = data.get("references", [])
        artifacts = {entry.get("artifact") for entry in entries}
        for artifact in sorted(REQUIRED_ARTIFACT_REFERENCES - artifacts):
            errors.append("artifact_reference_missing:" + artifact)
        if len(entries) != len({(entry.get("repository"), entry.get("artifact")) for entry in entries}):
            errors.append("duplicate_artifact_reference")
        for entry in entries:
            if entry.get("authority_effect") != "NONE":
                errors.append("artifact_reference_authority_effect_must_be_NONE:" + str(entry.get("artifact")))
        boundaries = data.get("boundaries", {})
        for key in [
            "artifact_reference_is_live_deployment",
            "artifact_reference_is_current_main_validation",
            "artifact_reference_is_execution_authority",
            "artifact_reference_is_master_records_custody",
        ]:
            if boundaries.get(key) is not False:
                errors.append("artifact_reference_boundary_must_be_false:" + key)

    if errors:
        print("LLM FREE TIER TRUST CHAIN: FAIL - " + ", ".join(errors))
        return 1
    print("LLM FREE TIER TRUST CHAIN: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
