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
-> Site navigation and deployment verification
```

## Installed files

```text
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
scripts/check_governed_llm_demo_docs.py
sidebars.js update
README.md update
docs/governance/governed-llm-activation-map.md update
ADMISSIBILITY_MIRROR_HANDOFF.md update
```

## Local verification

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## Deployment verification

```bash
python scripts/check_governed_llm_deployment_status.py
```

## Boundary

Site mirror publication is not provider governance, execution authority, commit-time standing, external indexing, or master-record persistence.

## Next mirror input

Only mirror generated adapter or SDK demo outputs after the adapter and SDK repositories produce matching receipt-bound artifacts.
