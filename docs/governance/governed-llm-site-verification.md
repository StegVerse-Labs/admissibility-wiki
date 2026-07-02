# Governed LLM Site Verification

## Purpose

This page defines the local verification path for governed LLM public documentation and navigation discoverability.

## Checked Surfaces

```text
docs/governance/governed-llm-reconstructive-search.md
docs/governance/governed-llm-activation-map.md
sidebars.js
docusaurus.config.js
README.md
```

## Verification Command

Run:

```bash
python scripts/check_governed_llm_pages.py
```

Expected result:

```text
GOVERNED LLM PAGES: PASS - docs and navigation references present
```

## Boundary

This verifies local documentation and navigation references only.

It does not prove deployed GitHub Pages status, Cloudflare cache state, or external indexing.

## Site Exposure

The governed LLM activation map is exposed through:

```text
Governance sidebar
Top navbar
Footer Core links
README pointer
```
