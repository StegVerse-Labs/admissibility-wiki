---
title: Term Discovery Runbook
---

# Term Discovery Runbook

## Purpose

This runbook defines how the Admissibility Wiki entity should perform periodic discovery of new terms, ideas, and formal structures that may be synonymous, equivalent, strongly correlated, overlapping, adjacent, broader, narrower, contradictory, or unresolved relative to existing wiki terms and formalism records.

## Source Boundary

Discovery may begin from many signals, but candidate origins must be formalized artifacts.

Acceptable origins include:

```text
formalism repository
standards document
academic paper
technical report
public specification
machine-readable schema
reference implementation
policy framework
regulatory guidance
public ontology
stable whitepaper
```

Disallowed origins include:

```text
LinkedIn comment
social-media post
conference comment
podcast statement
news summary
private message
chat transcript
```

A disallowed source may be recorded only as a lead if it points to an acceptable formalized origin. It must not be listed as the candidate origin.

## Search Cadence

```text
weekly: known formalism repositories and subscribed source families
monthly: standards bodies, academic indexes, public specifications, policy frameworks, and ontologies
quarterly: relationship summary review and candidate disposition report
```

## Search Procedure

1. Select target wiki term or formalism record.
2. Search for exact phrasing, neighboring phrasing, and strong conceptual equivalents.
3. Discard results without a formalized origin.
4. Record candidate only when origin type is allowed.
5. Classify relationship conservatively.
6. Record match dimensions and mismatch dimensions.
7. Record overclaiming risk.
8. Leave review status as pending until a decision record accepts, denies, or defers it.

## Candidate Queue

Candidate records belong in:

```text
static/discovery/term-candidate-queue.v0.1.json
```

Validate with:

```text
node scripts/check-term-candidate-queue.mjs
```

The aggregate repo validation command also runs this check:

```text
npm run validate
```

## Relationship Acceptance Rule

A candidate must not update glossary, formalism, ontology, or relationship-summary text until a decision record accepts the relationship.

## Non-Claims

```text
Discovery is not acceptance.
Correlation is not equivalence.
A social post is not a formalism origin.
A candidate record does not prove admissibility.
A candidate record does not create source authority.
A candidate record does not grant execution authority.
```

## Next Safe Action

Populate the first real candidate records from formalized origins only, then create decision records before mutating any public glossary or formalism page.
