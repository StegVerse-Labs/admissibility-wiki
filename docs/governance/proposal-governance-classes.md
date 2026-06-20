---
title: Proposal Governance Classes
---

# Proposal Governance Classes

## Purpose

Proposal governance classes define the review route for Admissibility Wiki submissions before any public display consequence is allowed.

The classes prevent low-risk editorial changes from carrying the cost of formalism review while preserving full reconstructability for meaning-changing proposals.

## Class Summary

```text
CLASS_E_EDITORIAL: low-risk editorial correction
CLASS_G_GOVERNANCE: standard meaning or mapping governance
CLASS_F_FORMALISM: formalism, ontology, authority, or transition-origin change
```

## Required Bundle Field

Every proposal manifest should include or be assigned:

```json
{
  "proposal_governance_class": "E|G|F",
  "class_assignment": {
    "assigned_at": "intake|review|reclassification",
    "assigned_by": "system|maintainer|governance_entity",
    "reason": "short reason"
  }
}
```

If the submitter omits the class, intake may assign a provisional class.

If review determines the assigned class is wrong, the proposal may be reclassified. Reclassification must be receipt-bound.

## Class E — Editorial

Class E is for non-substantive changes.

Examples:

```text
typo
formatting
broken link
citation formatting
navigation correction
layout correction
minor wording fix that does not change meaning
```

Route:

```text
proposal
↓
ingestion/CGE -> master-records
↓
editorial review
↓
decision record
↓
ingestion/CGE -> master-records
↓
public display consequence
```

Sandbox is not required unless the editorial change is reclassified.

## Class G — Governance

Class G is for standard terminology and mapping governance.

Examples:

```text
new term
term revision
overlap claim
adjacency claim
external framework mapping
new evidence source
relationship dispute
```

Route:

```text
proposal
↓
ingestion/CGE -> master-records
↓
sandbox candidate-path testing
↓
ingestion/CGE -> master-records
↓
StegVerse-Labs/proposal-governance-core-lite
↓
decision record
↓
ingestion/CGE -> master-records
↓
public display consequence
```

Sandbox preserves candidate outcomes before the decision path is selected.

## Class F — Formalism

Class F is for highest-impact changes.

Examples:

```text
equivalence claim
transition-origin modification
ontology mutation
proof-path modification
authority model modification
admissibility rule modification
formalism creation
```

Route:

```text
proposal
↓
ingestion/CGE -> master-records
↓
sandbox candidate-path generation
↓
ingestion/CGE -> master-records
↓
StegVerse-Labs/proposal-governance-core-lite
↓
formalism review
↓
decision record
↓
ingestion/CGE -> master-records
↓
public display consequence
```

Class F should preserve competing admissible and non-selected candidate paths.

## Global Invariants

```text
Every ingestion/CGE pass -> master-records
No sandbox output -> public display without a decision record
No proposal -> public display without a decision record
No receipt -> accepted standing
No queue placement -> decision authority
No LLM recommendation -> decision authority
```

## Public Display Rule

Public display is a consequence path, not a submission path.

The public display path is returned only after a decision record selects an admissible consequence.

## Related Pages

- [Proposal Intake Interface](./proposal-intake-interface.md)
- [Manifest Receipt Submission](./manifest-receipt-submission.md)
- [Proposal Intake Backend Contract](./proposal-intake-backend-contract.md)
- [Decision Record](./decision-record.md)
- [Intake API Final Activation Handoff](./intake-api-final-activation-handoff.md)
