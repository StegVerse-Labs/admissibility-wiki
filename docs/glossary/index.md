---
title: Glossary
---

# Glossary

## Purpose

The glossary defines stable StegVerse vocabulary for admissibility, transition governance, proof paths, receipts, evidence posture, review posture, and related convergence terms.

Glossary entries are public reference records. They should not silently imply origin, priority, equivalence, incorporation, or authority.

## Uniform Record Rule

Every glossary entry must expose the same citation, chronology, attribution, relationship, and review fields, even when a field is not yet populated.

The values `null`, `none`, `unknown`, `partial`, `disputed`, `unresolved`, and `in progress` are meaningful governance entries. They should be written explicitly instead of omitted.

For non-obvious StegVerse ecosystem terms, `in progress` may be used as a temporary status placeholder until source artifacts, dates, links, and relationship records are confirmed.

Each glossary entry should preserve:

```yaml
record:
  term:
  definition:
  term_class:
  first_known_stegverse_reference:
    artifact:
    date:
    link:
  original_drawing_or_seed_artifact:
    artifact:
    date:
    link:
    status:
  external_references:
    equivalent:
      - term:
        source:
        date:
        link:
        status:
    overlapping:
      - term:
        source:
        date:
        link:
        status:
    adjacent:
      - term:
        source:
        date:
        link:
        status:
    broader_than:
      - term:
        source:
        date:
        link:
        status:
    narrower_than:
      - term:
        source:
        date:
        link:
        status:
    contradicts:
      - term:
        source:
        date:
        link:
        status:
    unresolved:
      - term:
        source:
        date:
        link:
        status:
  known_contributors:
    - name:
      contribution:
      date:
      reference:
  chronology_status:
  attribution_status:
  evidence_status:
  review_status:
  relationship_status:
  commit_time_relevance:
  current_wiki_state:
  non_claim:
  open_questions:
```

## Governed Terminology Reconciliation

External terms are reconciled under the [Terminology Reconciliation](./terminology-reconciliation.md) glossary entry and the external-frameworks [Governed Terminology Reconciliation Rule](../external-frameworks/terminology-reconciliation-rule.md).

A relationship may be recorded only as:

| Class | Glossary use |
|---|---|
| Synonymous | Direct substitution is safe without changing governance semantics, authority reconstruction, transition meaning, or commit-time behavior. |
| Adjacent | The term is related but differs in scope, authority, timing, assumptions, or governance semantics. |
| New | The term adds external-native vocabulary that is not presently represented by an Admissibility term. |
| Unresolved | The relationship has insufficient evidence and must remain undecided. |

No glossary relationship may silently inherit execution authority, admissibility, standing, certification, governance proofs, or external-framework claims.

## Current Glossary Entries

| Entry | Current state | Record posture |
|---|---:|---|
| [Admissibility](./admissibility.md) | active | in progress |
| [Transition](./transition.md) | active | in progress |
| [Authority Class](./authority-class.md) | active | in progress |
| [Policy Reference](./policy-reference.md) | active | in progress |
| [Evidence Posture](./evidence-posture.md) | active | in progress |
| [Review Posture](./review-posture.md) | active | in progress |
| [Drift](./drift.md) | active | in progress |
| [Commit-Time Authority](./commit-time-authority.md) | active | in progress |
| [Commit-Time Validity](./commit-time-validity.md) | active | in progress |
| [Receipt-Bound Execution](./receipt-bound-execution.md) | active | in progress |
| [Governance Boundary](./governance-boundary.md) | active | in progress |
| [Reconstructability](./reconstructability.md) | active | in progress |
| [Terminology Reconciliation](./terminology-reconciliation.md) | active | in progress |

## Entry Status Placeholders

| Value | Meaning |
|---|---|
| active | The entry is part of the public glossary surface. |
| in progress | The entry is accepted as a StegVerse ecosystem term, but its chronology, citation, contributor, or external relationship metadata is still being populated. |
| unknown | No source-confirmed value has been located yet. |
| none | The field has been reviewed and no applicable value is presently asserted. |
| partial | Some evidence exists, but it is not complete enough to close the record. |
| disputed | A chronology, attribution, definition, or relationship claim is contested. |
| unresolved | A relationship or claim has been identified but not decided. |

## External Terminology Leads

Social posts, comment threads, and informal messages may identify candidate terms or contributor claims, but they should be recorded as leads only.

A lead becomes a glossary relationship only after a stable source artifact, dated passage, public specification, repository, paper, or other reviewable reference is provided.

## Non-Claim

A glossary entry does not prove that StegVerse originated a term, that an external contributor incorporated StegVerse language, or that two terms are equivalent.

It only provides a structured place to define the term, preserve uncertainty, cite sources, and map convergence without erasing chronology or attribution boundaries.
