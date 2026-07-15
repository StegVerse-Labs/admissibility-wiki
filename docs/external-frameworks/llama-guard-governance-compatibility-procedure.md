---
title: Llama Guard Governance Compatibility Procedure
---
# Llama Guard Governance Compatibility Procedure

## Current state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_runtime_execution_observed: false
governance_compatibility_observed: false
simulation_only: true
case_families: 6
```

This procedure tests how Llama Guard safety-classification evidence may enter a StegVerse governed transition. It does not treat a model label as policy legitimacy, standing, or execution authority.

## Contract artifacts

```text
fixture: tests/fixtures/external-frameworks/llama-guard-governance-compatibility-cases.v1.json
evaluator: scripts/run_llama_guard_governance_compatibility.py
result path: reports/external-frameworks/llama-guard/llama-guard-stegverse-governance-compatibility-receipt.json
status ledger: static/external-frameworks/governance-compatibility-testing-status.v1.json
```

## Required native evidence before runtime promotion

A future runtime packet must pin:

```text
canonical model-family and taxonomy references
model package, weights, tokenizer, and immutable hashes
prompt template and runtime parameters
shared content vectors
raw classifier outputs and parsing behavior
runtime, device, and timestamp evidence
replay commands
fresh-runner replay receipt
```

The recorded distribution page is source-discovery evidence only. It is not a complete model-governance or release-authority record.

## Six required cases

| Family | Simulated native result | Expected StegVerse result | Boundary |
|---|---|---|---|
| Positive alignment | `safe` | `ALLOW` | Only when every independent commit-time condition is satisfied. |
| Framework negative result | `unsafe` | `DENY` | Negative safety evidence remains bounded to the declared taxonomy and scope. |
| Authority or delegation failure | `safe` | `DENY` | A safe label cannot repair revoked delegation. |
| Stale or missing evidence | `safe` | `FAIL_CLOSED` | Stale model, taxonomy, prompt, or transition evidence cannot authorize action. |
| Malformed or runtime error | `error` | `FAIL_CLOSED` | Missing or malformed output is not permission. |
| Semantic divergence guard | `safe` | `DENY` | A safe label is not StegVerse `ALLOW` when target scope diverges. |

## Translation rule

```text
classifier output -> bounded safety evidence
safety evidence -> one input to commit-time evaluation
classifier safe != StegVerse ALLOW
classifier unsafe != universal policy authority
model execution != current delegation
```

StegVerse independently evaluates identity, current delegation, policy reference, evidence freshness, target scope, recoverability, and execution context.

## Failure posture

Unknown labels, taxonomy mismatch, source ambiguity, parser failure, model failure, stale configuration, or missing provenance must produce `FAIL_CLOSED` or a narrower denial. No fallback path may reinterpret uncertainty as authorization.

## Promotion criteria

The state may advance only after a pinned Llama Guard implementation executes the shared vectors, raw outputs and configuration are retained, replay occurs on a fresh runner, and the six expected governed outcomes match. Independent implementation or provider reproduction remains a separate stronger evidence class.

## Non-claims

This authored procedure and its simulation evaluator do not establish native runtime behavior, general compatibility, certification, complete safety coverage, standing, transition admissibility, or execution authority.
