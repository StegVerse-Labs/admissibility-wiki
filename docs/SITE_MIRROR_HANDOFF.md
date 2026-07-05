# Site Mirror Handoff

## Current source of truth

This file is the documentation mirror handoff source of truth for `StegVerse-Labs/admissibility-wiki/docs/` until superseded.

## Active goal

Goal 4: public documentation for the bounded LLM free-tier trust chain across LLM-adapter, Site, and SDK.

Goal 3 documented the governed LLM end-to-end demonstrator public documentation and Site mirror sync. Goal 4 now documents the free-tier trust chain that proves the public LLM entry path is not merely static demonstration material while preserving non-authority, non-admissibility, non-retention, and non-standing boundaries.

## Current proof path

```text
fixture query
-> LLM-adapter governed session packet
-> SDK validation
-> SDK intake routing
-> SDK manifest binding
-> SDK receipt handoff
-> wiki public demo overview
-> wiki public demo verification
-> canonical scheduled workflow
-> build-pages
-> deploy-pages
-> verify-public-pages
-> public-activation-receipt artifact
```

## Goal 4 free-tier trust chain

```text
StegVerse-org/LLM-adapter
  -> emits free_tier_trust metadata
  -> exposes adapter.capabilities.json free-tier fields

StegVerse-Labs/Site
  -> displays bounded free-tier trust envelope on ecosystem-chat.html
  -> guards the display with scripts/check_site_llm_free_tier_trust.py
  -> includes the checker in site-public-mirror-status-guard.yml

StegVerse-org/StegVerse-SDK
  -> validates free_tier_trust metadata shape
  -> validates quota / receipt / replay / reconstruction non-claims
  -> exposes validate_free_tier_metadata
  -> verifies ingestion in sdk-demo-test.yml

StegVerse-Labs/admissibility-wiki
  -> documents the chain in docs/governance/llm-free-tier-trust-chain.md
  -> checks the page with scripts/check_llm_free_tier_trust_chain.py
```

## Installed files

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
docs/governance/llm-free-tier-trust-chain.md
scripts/check_governed_llm_demo_docs.py
scripts/check_llm_free_tier_trust_chain.py
scripts/write-public-activation-receipt.mjs
scripts/check-public-activation-receipt-writer.mjs
sidebars.js update
README.md update
docs/governance/governed-llm-activation-map.md update
ADMISSIBILITY_MIRROR_HANDOFF.md update
.github/workflows/validate-chain-continuation.yml update
iosnoperiod/github/workflows/validate-chain-continuation.yml update
docs/SITE_MIRROR_HANDOFF.md update
```

## Local verification

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
python scripts/check_llm_free_tier_trust_chain.py
node scripts/check-public-activation-receipt-writer.mjs
npm run build
```

## Deployment verification

```text
Scheduled canonical workflow run completed successfully.
validate-chain-continuation: PASS
build-pages: PASS
deploy-pages: PASS
verify-public-pages: PASS
artifacts: 3
```

## Remaining hardening

```text
Inspect workflow artifacts and archive public-activation-receipt.
Resolve non-blocking workflow warnings.
Confirm public pages remain reachable after cache propagation.
Prepare release/tag candidate after warning cleanup and artifact review.
```

## Boundary

Site mirror publication and LLM free-tier documentation are not provider governance, execution authority, commit-time standing, external indexing, master-record persistence, permanent receipt retention, replay authority, reconstruction authority, or upgrade-based admissibility.

## Next mirror input

Only mirror generated adapter or SDK demo outputs after the adapter and SDK repositories produce matching receipt-bound artifacts. For free-tier trust metadata, use the adapter `free_tier_trust` response field and SDK `validate_free_tier_metadata` ingestion result as the source contract.
