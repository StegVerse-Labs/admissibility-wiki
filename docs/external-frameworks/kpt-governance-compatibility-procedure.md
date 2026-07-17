---
title: KPT Governance Compatibility Procedure
---

# KPT Governance Compatibility Procedure

## Status

```text
Contract state: CONTRACT_AUTHORED_RUNTIME_PENDING
Evaluation mode: deterministic simulation only
Official source status: unconfirmed
Native execution observed: false
General compatibility claimed: false
Manual task requirement: none
User action required: false
```

This procedure defines the bounded translation contract between KPT evidence and StegVerse commit-time admissibility. It does not claim that KPT has been executed, reproduced, certified, endorsed, or generally validated.

## Inputs

```text
tests/fixtures/external-frameworks/kpt-governance-compatibility-cases.v1.json
scripts/run_kpt_governance_compatibility.py
docs/external-frameworks/kpt.md
```

The six required case families are:

```text
positive_alignment
framework_denial_or_negative_result
authority_or_delegation_failure
stale_or_missing_evidence
malformed_undefined_or_runtime_error
semantic_divergence_guard
```

## Boundary

KPT public positioning, candidate-output decisions, trace evidence, and boundary-before-consequence language may enter StegVerse only as source-bounded evidence.

They do not establish:

```text
current actor standing
current delegation
current policy validity
action, influence, or target scope
commit-time admissibility
execution authority
release authority
downstream mutation authority
```

A profile description or screenshot-only intake remains `SOURCE_BLOCKED_FAIL_CLOSED`. A future official source or authorized artifact package may support native execution and replay, but a KPT allow or deny does not become StegVerse authority merely because it is public, valid, or runtime-produced.

## Deterministic evaluation

Run:

```text
python scripts/run_kpt_governance_compatibility.py
```

Expected local result:

```text
KPT GOVERNANCE COMPATIBILITY: PASS
cases=6 matched=6
```

The generated receipt is:

```text
reports/external-frameworks/kpt/kpt-stegverse-governance-compatibility-receipt.json
```

That receipt records contract simulation only. It must retain:

```text
native_execution_observed: false
official_source_confirmed: false
stegverse_governance_compatibility_observed: false
manual_tasks_required: []
user_action_required: false
authority_granted: false
execution_authority_granted: false
release_authority_granted: false
downstream_mutation_authority_granted: false
```

## Promotion requirements

Promotion beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` requires an owner-published official source or authorized artifact package, implementation and version identity, decision and trace schemas, runtime inputs and configuration, raw outputs, hashes, exact replay commands, and fresh-runner reproduction.

Until those artifacts are attached and directly observed, KPT remains source-blocked and runtime-unobserved. No manual user task is created by that state.
