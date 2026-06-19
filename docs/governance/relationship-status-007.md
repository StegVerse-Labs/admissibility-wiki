---
title: NIST AI RMF Relationship Status
---

# NIST AI RMF Relationship Status

## Purpose

This status receipt records the current state of `proposal.example.007` and `decision.example.007` without changing the broader task-sync file.

## Current State

```text
proposal_id: proposal.example.007
decision_id: decision.example.007
target_page: docs/glossary/governance-boundary.md
external_source_family: NIST AI Risk Management Framework
relationship: overlapping
disposition: ALLOW_AS_OVERLAP
equivalent_status: not accepted
glossary_mutation: completed
```

## Built Artifacts

```text
static/governance/proposals/proposal.example.007.json
static/governance/decisions/decision.example.007.json
static/governance/replay/decision.example.007.txt
static/governance/evidence/decision.example.007/README.md
docs/glossary/governance-boundary.md
```

## Accepted Boundary

NIST AI RMF governance and AI risk-management language may be listed under `Overlapping Terms` for Governance Boundary.

It must not be listed under `Equivalent Terms` unless a future decision record explicitly accepts equivalence.

## Non-Claims

```text
This status does not claim NIST endorsement.
This status does not make NIST AI RMF equivalent to Governance Boundary.
This status does not make NIST AI RMF a StegVerse execution-authority boundary.
This status does not create admissibility standing.
```

## Next Safe Action

Do not recreate proposal 007.

Future relationship work should use a new ID only if it covers a materially new source family and does not duplicate proposals 005, 006, 007, or 008.
