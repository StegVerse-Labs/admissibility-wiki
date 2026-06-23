---
title: Discovery Index
---

# Discovery Index

## Purpose

This page is the public entry point for the Formalism Discovery Engine layer.

The discovery layer indexes formalism terms, generates candidate relationships, preserves origins, and requires review before any relationship is promoted.

## Discovery Documents

| Page | Purpose |
|---|---|
| [Formalism Discovery Engine](./discovery-engine.md) | Defines the discovery layer boundary and lifecycle. |
| [Discovery Relationship Types](./relationship-types.md) | Defines candidate relationship vocabulary. |
| [Discovery Review Queue](./review-queue.md) | Defines review and promotion requirements. |
| [Relationship Decision Validation](./relationship-decision-validation.md) | Defines validation expectations for reviewed relationship decisions. |

## Machine-Readable Stores

| Store | Purpose |
|---|---|
| `static/discovery/discovered-terms.json` | Indexed terms with formal origins. |
| `static/discovery/candidate-relationships.json` | Review-required relationship candidates. |
| `static/discovery/relationship-decisions.json` | Reviewed relationship decisions. |

## Executable Paths

```text
npm run discovery:build
npm run validate:discovery-stores
npm run validate
```

## Promotion Boundary

```text
Indexed term != canonical definition
Candidate relationship != accepted relationship
Confidence score != proof
Source origin != endorsement
Review decision != replacement of source authority
```

## Non-Claims

```text
The discovery index does not define formal terms.
The discovery index does not assert synonymy.
The discovery index does not assert equivalence.
The discovery index does not expose private source content.
```
