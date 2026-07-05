# LLM Free Tier iOS Mirror Sync

## Purpose

This note records the iOS-safe workflow mirror requirement for the LLM free-tier trust chain.

The canonical workflow now validates:

```text
python scripts/check_llm_free_tier_trust_chain.py
```

and verifies the deployed public page:

```text
https://stegverse-labs.github.io/admissibility-wiki/governance/llm-free-tier-trust-chain
```

## Canonical path

```text
.github/workflows/validate-chain-continuation.yml
```

## iOS-safe mirror path

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

## Required mirror delta

The iOS-safe mirror should include the same LLM free-tier validation additions as the canonical workflow:

```text
Validate LLM free-tier trust chain
  -> python scripts/check_llm_free_tier_trust_chain.py

Verify LLM free-tier trust chain
  -> curl --fail --location --retry 12 --retry-delay 10 --retry-all-errors https://stegverse-labs.github.io/admissibility-wiki/governance/llm-free-tier-trust-chain
```

## Boundary

This note does not create deployment authority, publish the site, issue receipts, or modify workflow permissions. It records the required iOS-safe mirror equivalence so the mirror can be checked without relying on prior chat context.
