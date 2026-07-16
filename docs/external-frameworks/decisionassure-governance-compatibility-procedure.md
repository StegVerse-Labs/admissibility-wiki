---
title: DecisionAssure Governance Compatibility Procedure
---

# DecisionAssure Governance Compatibility Procedure

## Purpose

This procedure tests whether DecisionAssure trace integrity, causal-continuity, drift, corruption, and verifier evidence can be translated into StegVerse commit-time evaluation without converting a trace result into standing or execution authority.

## Current evidence state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
authorized_artifact_package_attached: false
public_canonical_source_attached: false
native_verifier_execution_observed: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
simulation_only: true
```

The current page is an artifact-package-required intake record. Prior discussion or a described trace does not establish an authorized package, pinned verifier, runtime behavior, independent reproduction, or general compatibility.

## Contract artifacts

```text
fixture: tests/fixtures/external-frameworks/decisionassure-governance-compatibility-cases.v1.json
evaluator: scripts/run_decisionassure_governance_compatibility.py
expected receipt: reports/external-frameworks/decisionassure/decisionassure-stegverse-governance-compatibility-receipt.json
```

## Required case families

| Family | DecisionAssure evidence | Expected StegVerse decision |
|---|---|---|
| Positive alignment | Causal continuity persisted and every current commit-time condition holds | `ALLOW` |
| Framework negative result | Corrupt or causally dead trace | `DENY / TRACE_CORRUPTION` |
| Authority or delegation failure | Continuity claimed after delegation drift | `DENY / AUTHORITY_DRIFT` |
| Stale or missing evidence | Internally consistent but stale trace | `FAIL_CLOSED / STALE_TRACE_EVIDENCE` |
| Malformed or runtime error | Verifier error or undefined output | `FAIL_CLOSED / TRACE_VERIFIER_ERROR` |
| Semantic divergence guard | Continuity persisted under a superseded policy | `DENY / POLICY_DRIFT` |

## Translation boundary

```text
trace integrity -> bounded reconstruction evidence
causal continuity -> bounded continuity evidence
drift indicator -> commit-time review input
corruption indicator -> denial or fail-closed input
verifier result -> artifact-specific evidence
```

None of those results independently establishes actor identity, current delegation, policy legitimacy, evidence freshness, execution context, recoverability, consequence authority, or commit-time admissibility.

## Runtime completion requirements

Bounded runtime compatibility may be promoted only after attaching:

```text
- an authorized DecisionAssure artifact package or public canonical source
- a pinned verifier implementation and version
- the trace schema and canonicalization rules
- complete input trace and pre/post state hashes
- policy, delegation, identity, and context references
- raw verifier output and exit status
- artifact, verifier, schema, and output hashes
- exact replay commands
- a fresh-runner receipt
- independently inspected StegVerse translation evidence
```

## Non-claims

A DecisionAssure `ALLOW`, `DENY`, `CORRUPT`, continuity finding, drift signal, or verifier output is not inherited StegVerse authority. This authored simulation is not native runtime observation, source authentication, independent reproduction, certification, endorsement, standing, release authority, or execution authority.
