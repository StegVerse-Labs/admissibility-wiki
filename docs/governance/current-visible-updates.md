---
title: Current Visible Updates
---

# Current Visible Updates

## Purpose

This page exists so public readers can quickly confirm whether the live wiki deployment includes the latest repository changes.

## Current Update Set

The current repository build includes:

- Admissible-Existence formalism registry records;
- a visible Formalisms page;
- a formalism registry validator;
- a term-discovery policy;
- a term-discovery runbook;
- a machine-readable term candidate queue;
- a term candidate queue validator;
- validation wiring for formalism and term-discovery checks.

## Primary Pages

- [Formalisms](../formalisms/index.md)
- [Term Discovery Policy](./term-discovery-policy.md)
- [Term Discovery Runbook](./term-discovery-runbook.md)

## Machine-Readable Artifacts

```text
static/formalisms/formalism-registry.v0.1.json
static/discovery/term-candidate-queue.v0.1.json
```

## Validation Commands

```text
node scripts/check-formalism-registry.mjs
node scripts/check-term-candidate-queue.mjs
npm run validate
```

## Deployment Check

If this page is visible in the live wiki, the public Pages deployment includes the latest visible update set.

If this page is not visible in the live wiki after a successful deploy, the public Pages artifact is stale or the deploy workflow has not completed.

## Non-Claims

This page is a deployment visibility marker only. It does not create source authority, proof authority, execution authority, continuity standing, or admissibility standing.
