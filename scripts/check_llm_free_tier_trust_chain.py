from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "governance" / "llm-free-tier-trust-chain.md"
SIDEBAR = ROOT / "sidebars.js"
README = ROOT / "README.md"
HANDOFF = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"

REQUIRED_PAGE_TEXT = [
    "LLM Free Tier Trust Chain",
    "StegVerse-org/LLM-adapter",
    "free_tier_trust metadata",
    "adapter.capabilities.json",
    "StegVerse-Labs/Site",
    "ecosystem-chat.html",
    "scripts/check_site_llm_free_tier_trust.py",
    "site-public-mirror-status-guard.yml",
    "StegVerse-org/StegVerse-SDK",
    "validate_free_tier_metadata",
    "sdk-demo-test.yml",
    "quota availability is not admissibility",
    "receipt_export_is_permanent_retention == false",
    "reconstruction_grants_commit_time_standing == false",
]

REQUIRED_SIDEBAR_TEXT = [
    "governance/llm-free-tier-trust-chain",
]

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
    handoff_text = _read(HANDOFF)

    if not PAGE.exists():
        errors.append("missing_page")
    if not SIDEBAR.exists():
        errors.append("missing_sidebar")
    if not README.exists():
        errors.append("missing_readme")
    if not HANDOFF.exists():
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

    if errors:
        print("LLM FREE TIER TRUST CHAIN: FAIL - " + ", ".join(errors))
        return 1
    print("LLM FREE TIER TRUST CHAIN: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
