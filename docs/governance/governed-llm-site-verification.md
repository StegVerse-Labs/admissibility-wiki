# Governed LLM Site Verification

## Purpose

This page defines the local verification path for governed LLM public documentation and navigation discoverability.

## Checked Surfaces

```text
docs/governance/governed-llm-reconstructive-search.md
docs/governance/governed-llm-activation-map.md
docs/governance/governed-llm-site-verification.md
docs/governance/governed-llm-deployment-status.md
sidebars.js
docusaurus.config.js
README.md
```

## Local Verification Command

Run:

```bash
python scripts/check_governed_llm_pages.py
```

Expected result:

```text
GOVERNED LLM PAGES: PASS - docs and navigation references present
```

## Deployment Verification Command

Run after GitHub Pages deployment has completed:

```bash
python scripts/check_governed_llm_deployment_status.py
```

Expected deployed result:

```text
GOVERNED LLM DEPLOYMENT: PASS - deployed pages reachable
```

## Boundary

This verifies local documentation and navigation references only.

It does not prove deployed GitHub Pages status, Cloudflare cache state, or external indexing. Deployment reachability must be checked separately.

## Site Exposure

The governed LLM activation map is exposed through:

```text
Governance sidebar
Top navbar
Footer Core links
README pointer
```
