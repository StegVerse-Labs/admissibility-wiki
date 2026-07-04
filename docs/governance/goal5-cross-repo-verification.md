---
title: Goal 5 Cross-Repo Verification
---

# Goal 5 Cross-Repo Verification

This page records the single-command verification chain for the Goal 5 portable governed return-path / runtime-target compatibility surface.

## Purpose

Goal 5 reduces manual verification by making each repository expose one canonical command that verifies its local part of the proof chain.

The commands are repo-local and fixture-bound. They do not activate live providers, grant execution authority, persist master records, or certify external systems.

## Workflow cap

Each repository must retain no more than two GitHub Actions workflows.

The preferred workflow pattern is:

```text
.github/workflows/validate.yml
  -> canonical repo validation and Goal verifier

.github/workflows/tasks.yml
  -> optional stable task declaration / repo automation surface
```

Goal-specific workflows should not be added. Goal verification must be folded into the existing validate workflow or the iOS mirror of that workflow until canonical workflow activation is authorized.

## Repository command manifest

| Repository | Role | Canonical command | CI ownership |
| --- | --- | --- | --- |
| `StegVerse-002/micro-node-runtime` | transition-table-native portable micro-node runtime | `python tools/verify_goal5.py` | folded into `iosnoperiod/github/workflows/validate.yml` until canonical workflow activation |
| `StegVerse-org/core-node-runtime-demo` | larger runtime comparison against micro-node contract | `python tools/verify_goal5.py` | folded into existing `.github/workflows/validate.yml` |
| `StegVerse-org/LLM-adapter` | external LLM adapter governed return-path proof | `python scripts/verify_goal4.py` | installed as single `.github/workflows/validate.yml` |
| `StegVerse-org/StegVerse-SDK` | SDK validation of adapter-originated micro-node fixtures | `python scripts/verify_goal4.py` | installed as single `.github/workflows/validate.yml` |
| `StegVerse-Labs/admissibility-wiki` | public documentation and Site verification | `python scripts/check_governed_llm_pages.py && python scripts/check_governed_llm_demo_docs.py && npm run build` | should be folded into one existing or new validate/build workflow, not a separate Goal workflow |

## CI-owned execution model

```text
push / pull_request / workflow_dispatch
-> repo validate workflow
-> canonical Goal verifier
-> JSON or build output
-> artifact or workflow log
-> handoff records latest passing commit
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
workflow_count_exceeds_two == false
```

## Completion rule

Goal 5 is repo-local complete when every canonical command above passes through CI-owned validation without requiring local clone or Codespaces execution.

Deployment reachability remains separate from local repo completion.
