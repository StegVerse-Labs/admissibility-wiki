# Site Mirror Handoff

## Current source of truth

This file is the documentation mirror handoff source of truth for `StegVerse-Labs/admissibility-wiki/docs/` until superseded.

## Active goal

Goal 3: Governed LLM end-to-end demonstrator public documentation and Site mirror sync.

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

## Installed files

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
scripts/check_governed_llm_demo_docs.py
scripts/write-public-activation-receipt.mjs
scripts/check-public-activation-receipt-writer.mjs
sidebars.js update
README.md update
docs/governance/governed-llm-activation-map.md update
ADMISSIBILITY_MIRROR_HANDOFF.md update
.github/workflows/validate-chain-continuation.yml update
iosnoperiod/github/workflows/validate-chain-continuation.yml update
```

## Local verification

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
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

Site mirror publication is not provider governance, execution authority, commit-time standing, external indexing, or master-record persistence.

## Next mirror input

Only mirror generated adapter or SDK demo outputs after the adapter and SDK repositories produce matching receipt-bound artifacts.
