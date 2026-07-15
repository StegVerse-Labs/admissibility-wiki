---
title: Validation
---

# Validation

The Admissibility Wiki uses one canonical repository workflow to protect the public vocabulary, generated status surfaces, documentation topology, build, deployment chain, and public verification boundaries.

## Canonical Workflow

```text
.github/workflows/validate-chain-continuation.yml
```

The workflow is intended to run on:

- pushes;
- pull requests;
- workflow dispatch;
- the repository-owned hourly schedule.

The iOS-readable mirror is inert:

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

It is not an additional active workflow.

## Validation Scope

Validation is not limited to ontology parsing. The aggregate chain may include:

- vocabulary and ontology structure;
- Docusaurus build and navigation integrity;
- formalism and translation-record registries;
- governed ecosystem transition status;
- governed LLM pages, demonstrations, trust-chain, and deployment posture;
- external-framework reports, terminology, result generation, and evidence classifications;
- proposal, decision-record, mirror-handoff, and repository-standard checks;
- workflow-sprawl prevention;
- bounded observation, health, transition, trend, frequency, stability, comparison, and history artifacts;
- terminal workflow-observation rollup;
- hash-bound Pages-build receipt;
- Pages deployment and automatic public endpoint verification.

The exact current command inventory belongs to `package.json`, the canonical workflow, and the mirror handoff. This page must not freeze an obsolete partial list as the full validation contract.

## Local Aggregate Entry Point

```bash
npm run validate
```

Individual validators may be run for deterministic repair, but a passing individual validator is not equivalent to a passing canonical chain.

## Healthy State

A complete healthy state requires separable evidence for:

```text
source validation
-> generated artifact completeness
-> Docusaurus build
-> terminal rollup completeness
-> Pages-build receipt binding
-> artifact custody
-> Pages deployment
-> public endpoint verification
```

These states must not be collapsed. In particular:

```text
local validator pass != canonical workflow pass
canonical workflow pass != deployment pass
deployment pass != public endpoint verification
public verification != proof authority
build receipt != Master-Records custody
```

## Current Evidence Posture

The current mirror handoff records:

```text
canonical workflow pass: not claimed
Pages deployment pass: not claimed
terminal rollup public reachability: not claimed
manual user tasks required: none
release/tag authority: not granted
```

Repository-owned automation remains responsible for recurring validation, deployment, public re-observation, and artifact renewal.

## Failure Handling

When repository-owned evidence exposes a deterministic failure:

1. identify the first exact failing command or malformed generated artifact;
2. repair that failure without weakening existing checks;
3. preserve the single-workflow policy;
4. preserve fail-closed behavior for missing evidence;
5. allow the next repository-owned trigger to regenerate and re-observe the chain.

Do not create a manual user task to rerun workflows, construct receipts, check public routes, move files, or perform archival. Do not add a second active workflow to bypass the failing chain.

## Terminal Envelope Boundary

The terminal workflow-observation rollup closes the derivative status chain. Missing required artifacts produce a fail-closed incomplete state rather than another recursive summary layer or a user task.

Expected terminal properties include:

```text
terminal_envelope: true
recursive_derivative_expansion_allowed: false
manual_tasks_required: []
user_action_required: false
```

## Authority Boundary

Validation protects repository consistency. It does not grant:

- proof authority;
- execution authority;
- admissibility standing;
- custody transfer;
- cross-repository mutation authority;
- release or tag authority.
