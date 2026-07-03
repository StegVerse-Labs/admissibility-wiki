# Admissibility Wiki Mirror Handoff

## Status

This file is the current handoff and task source of truth for `StegVerse-Labs/admissibility-wiki`.

## Current priority

Goal 3: Governed LLM end-to-end demonstrator public documentation and Site mirror sync.

The wiki publishes the public explanation of the demonstrator after the adapter and SDK handoffs authorize the demo installation.

## Source repositories

```text
StegVerse-org/LLM-adapter
  -> runtime demonstrator source

StegVerse-org/StegVerse-SDK
  -> SDK intake and receipt handoff verification source
```

## Existing governed LLM public pages

```text
docs/governance/governed-llm-reconstructive-search.md
docs/governance/governed-llm-activation-map.md
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
docs/governance/governed-llm-site-verification.md
docs/governance/governed-llm-deployment-status.md
docs/governance/governed-llm-archive-handoff.md
scripts/check_governed_llm_pages.py
scripts/check_governed_llm_demo_docs.py
scripts/check_governed_llm_deployment_status.py
```

## Goal 3 installation state

```text
docs/governance/governed-llm-demo-overview.md -> installed
docs/governance/governed-llm-demo-verification.md -> installed
scripts/check_governed_llm_demo_docs.py -> installed and hardened
sidebars.js -> linked
README.md -> linked
docs/governance/governed-llm-activation-map.md -> updated with demo chain
```

## Required invariant

```text
public_demo_page_claims_live_provider_governance == false
public_demo_page_claims_execution_authority == false
public_demo_page_claims_external_indexing == false
demo_is_fixture_first == true
adapter_and_sdk_remain_source_of_implementation_truth == true
```

## Verification commands

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## Boundary

The wiki mirrors evidence-bounded ecosystem status. Publication does not create certification, endorsement, execution authority, commit-time standing, provider governance, or master-record persistence.

## Archive posture

Repo-local archive posture is ready after both local checkers and the Docusaurus build pass. Deployment reachability and cross-repo generated receipts remain separate follow-up checks.
