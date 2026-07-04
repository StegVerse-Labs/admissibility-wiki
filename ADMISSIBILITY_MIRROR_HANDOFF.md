# Admissibility Wiki Mirror Handoff

## Status

This file is the current handoff and task source of truth for `StegVerse-Labs/admissibility-wiki`.

## Current priority

Goal 4: Portable governed return-path public documentation sync.

Goal 3 established the governed LLM end-to-end demonstrator public documentation and Site mirror sync. Goal 4 records the public proof chain for returning a governed result to the originating customer path across micro-node runtime, adapter, SDK, and Site layers.

## Source repositories

```text
StegVerse-002/micro-node-runtime
  -> transition-table-native portable micro-node runtime

StegVerse-org/core-node-runtime-demo
  -> larger-runtime comparison against micro-node contract

StegVerse-org/LLM-adapter
  -> fixture-bound governed return-path proof

StegVerse-org/StegVerse-SDK
  -> SDK-side validation of adapter-originated micro-node fixtures
```

## Existing governed LLM public pages

```text
docs/governance/governed-llm-reconstructive-search.md
docs/governance/governed-llm-activation-map.md
docs/governance/governed-llm-demo-overview.md
docs/governance/governed-llm-demo-verification.md
docs/governance/governed-llm-site-verification.md
docs/governance/governed-llm-deployment-status.md
docs/governance/portable-governed-return-path.md
docs/governance/governed-llm-archive-handoff.md
scripts/check_governed_llm_pages.py
scripts/check_governed_llm_demo_docs.py
scripts/check_governed_llm_deployment_status.py
```

## Goal 4 installation state

```text
docs/governance/portable-governed-return-path.md -> installed and synced with adapter/SDK Goal 4 commands
sidebars.js -> linked
README.md -> governed LLM and proof-path index present
StegVerse-org/LLM-adapter/LLM_ADAPTER_MIRROR_HANDOFF.md -> Goal 4 active
StegVerse-org/StegVerse-SDK/STEGVERSE_SDK_MIRROR_HANDOFF.md -> Goal 4 active
```

## Required invariant

```text
public_demo_page_claims_live_provider_governance == false
public_demo_page_claims_execution_authority == false
public_demo_page_claims_external_indexing == false
public_return_path_claims_runtime_execution == false
demo_is_fixture_first == true
adapter_and_sdk_remain_source_of_implementation_truth == true
```

## Verification commands

```bash
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

Adapter Goal 4 verification:

```bash
python scripts/verify_micro_node_return_path.py
pytest tests/test_micro_node_return_path.py -v
pytest tests/ -v
```

SDK Goal 4 verification:

```bash
python scripts/verify_micro_node_return_path.py
pytest tests/test_micro_node_return_path.py -v
```

## Boundary

The wiki mirrors evidence-bounded ecosystem status. Publication does not create certification, endorsement, execution authority, commit-time standing, provider governance, live runtime execution, or master-record persistence.

## Archive posture

Repo-local archive posture is ready after the Site checks and Docusaurus build pass. Deployment reachability and cross-repo generated receipts remain separate follow-up checks.
