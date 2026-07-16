---
title: Morrison Runtime Governance Compatibility Procedure
---

# Morrison Runtime Governance Compatibility Procedure

## Purpose

This procedure tests whether Morrison Runtime `ALLOW`, `BLOCK`, or `ERROR` outputs can enter StegVerse as bounded pre-execution evidence without becoming inherited authority at the commit boundary.

## Current evidence state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
source_reviewed: true
historical_parameterized_observation_present: true
raw_runtime_artifact_package_attached: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
simulation_only: true
```

The sourced Morrison Runtime page and parameterized semantic-equivalence case establish vocabulary and a bounded observation posture. They do not establish a pinned implementation, raw audit payload, complete runtime configuration, deterministic replay, or independent reproduction.

## Contract artifacts

```text
fixture: tests/fixtures/external-frameworks/morrison-runtime-governance-compatibility-cases.v1.json
evaluator: scripts/run_morrison_runtime_governance_compatibility.py
expected receipt: reports/external-frameworks/morrison-runtime/morrison-runtime-stegverse-governance-compatibility-receipt.json
```

## Required case families

| Family | Morrison evidence | Expected StegVerse decision |
|---|---|---|
| Positive alignment | Runtime `ALLOW` and all current commit-time conditions | `ALLOW` |
| Framework negative result | Runtime `BLOCK` | `DENY / RUNTIME_TRAJECTORY_BLOCKED` |
| Authority or delegation failure | Runtime `ALLOW` with expired delegation | `DENY / AUTHORITY_DRIFT` |
| Stale or missing evidence | Runtime `ALLOW` with stale audit evidence | `FAIL_CLOSED / STALE_RUNTIME_EVIDENCE` |
| Malformed or runtime error | Runtime `ERROR` or no verdict | `FAIL_CLOSED / RUNTIME_VERDICT_UNAVAILABLE` |
| Semantic divergence guard | Runtime `ALLOW` for a non-equivalent trajectory scope | `DENY / TRAJECTORY_SEMANTIC_DIVERGENCE` |

## Translation boundary

```text
Morrison ALLOW -> runtime policy evidence
Morrison BLOCK -> runtime denial evidence
Morrison ERROR -> unavailable or unresolved runtime evidence
Morrison audit payload -> scoped reconstruction evidence
```

None of those artifacts independently establishes actor identity, current delegation, current policy legitimacy, evidence freshness, semantic equivalence, recoverability, consequence authority, or StegVerse commit-time admissibility.

## Runtime completion requirements

Bounded runtime compatibility may be promoted only after attaching:

```text
- a pinned Morrison Runtime repository commit, release, or executable
- the exact runtime policy and forbidden-region configuration
- versioned planner or tool-trajectory inputs
- raw ALLOW, BLOCK, ERROR, and audit outputs
- semantic-equivalence and alternate-tool-label vectors
- package, configuration, input, and output hashes
- exact replay commands
- a fresh-runner receipt
- an independently inspected StegVerse translation receipt
```

## Non-claims

A Morrison `ALLOW` is not StegVerse `ALLOW`. A Morrison `BLOCK` is not delegated StegVerse execution authority. An error is not safe fallback permission. Historical or parameterized observations without raw runtime artifacts are not deterministic reproduction. This authored simulation is not certification, endorsement, standing, release authority, or execution authority.
