---
title: Goal 5 Cross-Repo Verification
---

# Goal 5 Cross-Repo Verification

This page records the single-command verification chain for the Goal 5 portable governed return-path / runtime-target compatibility surface.

## Purpose

Goal 5 reduces manual verification by making each repository expose one canonical command that verifies its local part of the proof chain.

The commands are repo-local and fixture-bound. They do not activate live providers, grant execution authority, persist master records, or certify external systems.

## Repository command manifest

| Repository | Role | Canonical command | Expected top-level result |
| --- | --- | --- | --- |
| `StegVerse-002/micro-node-runtime` | transition-table-native portable micro-node runtime | `python tools/verify_goal5.py` | JSON report with `complete: true` |
| `StegVerse-org/core-node-runtime-demo` | larger runtime comparison against micro-node contract | `python tools/verify_goal5.py` | JSON report with `complete: true` |
| `StegVerse-org/LLM-adapter` | external LLM adapter governed return-path proof | `python scripts/verify_goal4.py` | JSON report with `complete: true` |
| `StegVerse-org/StegVerse-SDK` | SDK validation of adapter-originated micro-node fixtures | `python scripts/verify_goal4.py` | JSON report with `complete: true` |
| `StegVerse-Labs/admissibility-wiki` | public documentation and Site verification | `python scripts/check_governed_llm_pages.py && python scripts/check_governed_llm_demo_docs.py && npm run build` | local docs/build pass |

## Suggested execution order

```bash
cd micro-node-runtime
python tools/verify_goal5.py

cd ../core-node-runtime-demo
python tools/verify_goal5.py

cd ../LLM-adapter
python scripts/verify_goal4.py

cd ../StegVerse-SDK
python scripts/verify_goal4.py

cd ../admissibility-wiki
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

## Proof chain

```text
micro-node-runtime
-> core-node-runtime-demo
-> LLM-adapter
-> StegVerse-SDK
-> admissibility-wiki
```

## Required non-claims

```text
fixture_bound == true
live_provider_activation == false
execution_authority_granted == false
master_record_persistence_claimed == false
external_system_certified == false
```

## Completion rule

Goal 5 is repo-local complete when every canonical command above passes in a live clone or Codespaces environment and the generated/published Site state reflects the same command manifest.

Deployment reachability remains separate from local repo completion.
