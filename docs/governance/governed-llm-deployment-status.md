# Governed LLM Deployment Status

## Purpose

This page distinguishes local Site verification from deployed GitHub Pages confirmation for the governed LLM public documentation set.

## Local Verification

Local verification checks whether the repository contains the required pages and navigation references.

```bash
python scripts/check_governed_llm_pages.py
```

Expected local result:

```text
GOVERNED LLM PAGES: PASS - docs and navigation references present
```

## Deployment Verification

Deployment verification checks whether the expected public GitHub Pages routes are reachable.

```bash
python scripts/check_governed_llm_deployment_status.py
```

Expected deployed result after GitHub Pages has published:

```text
GOVERNED LLM DEPLOYMENT: PASS - deployed pages reachable
```

If the result is pending, the local repo may still be correct while GitHub Pages build, cache, or deployment propagation has not completed.

## Checked Public Routes

The deployment checker uses the configured Docusaurus base URL and verifies these governed LLM route paths:

```text
/governance/governed-llm-reconstructive-search
/governance/governed-llm-activation-map
/governance/governed-llm-site-verification
```

## Boundary

```text
Local verification is not deployed confirmation.
Deployed confirmation is not external indexing.
GitHub Pages reachability is not Cloudflare cache confirmation.
```
