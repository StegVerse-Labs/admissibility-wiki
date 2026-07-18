---
title: Policy Cards Governance Compatibility Procedure
---

# Policy Cards Governance Compatibility Procedure

## State

```text
Contract: authored
Runtime observation: pending
Native implementation: not attached
Compatibility observation: false
Manual tasks required: none
User action required: false
```

## Purpose

This procedure evaluates a bounded translation from Policy Cards terminology into StegVerse commit-time governance outcomes without treating a machine-readable policy declaration as execution authority.

## Inputs

- `docs/external-frameworks/policy-cards.md`
- `tests/fixtures/external-frameworks/policy-cards-governance-compatibility-cases.v1.json`
- `scripts/run_policy_cards_governance_compatibility.py`

## Deterministic Case Families

The contract includes exactly six required families: positive alignment, framework denial or negative result, authority or delegation failure, stale or missing evidence, malformed or undefined input, and semantic-divergence guard.

## Translation Boundary

A Policy Card may supply policy, constraint, allow/deny, or evidentiary material. Its presence or result does not establish current standing, delegation, commit-time admissibility, release authority, or execution authority. StegVerse therefore evaluates authority and current evidence independently and fails closed when either is absent.

## Evidence Posture

The public paper source is reviewed. No implementation package, schema snapshot, native runtime output, fresh-runner replay, or independent implementation reproduction is claimed. The evaluator is a deterministic StegVerse simulation and cannot establish native-framework compatibility.

## Output

The evaluator writes:

`reports/external-frameworks/policy-cards/policy-cards-stegverse-governance-compatibility-receipt.json`

The receipt preserves:

```text
native_execution_observed: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
manual_tasks_required: []
user_action_required: false
downstream_mutation_authority: false
```

## Next Evidence Gate

Attach a pinned, authorized Policy Cards implementation or schema package with raw inputs and outputs, hashes, timestamps, and replay evidence before any native-execution or compatibility-observed claim is permitted. Absence of that package remains automation-owned and creates no user task.
