---
title: Term Discovery Policy
---

# Term Discovery Policy

## Purpose

The Admissibility Wiki entity should periodically search for new terms, ideas, definitions, and formal structures that are exactly or strongly correlated with existing wiki terms and formalisms.

The goal is to accelerate governed AI adoption by finding independently defined concepts across companies, researchers, standards bodies, public institutions, and formal projects, then presenting them as review candidates for relationship mapping.

## Scope

Discovery may identify candidates for:

```text
Equivalent Terms
Synonymous Relationship Candidates
Overlapping Terms
Adjacent Terms
Broader Terms
Narrower Terms
Contradictory Terms
Unresolved Terms
```

## Origin Requirement

A candidate origin must be a formalized artifact, not an informal social-media comment.

Acceptable origin types include:

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
whitepaper with stable publisher/source
```

Non-authoritative discovery sources may help find leads, but they cannot be treated as origins.

Examples of non-origin leads:

```text
LinkedIn comment
social-media post
conference comment
podcast statement
news article summarizing another source
private message
chat transcript
```

If a lead points to a formalism, the formalism may be evaluated as the origin. The lead itself must not be listed as the origin.

## Candidate Relationship Thresholds

### Exact Or Synonymous Candidate

Use only when the candidate formalism appears to define substantially the same concept, boundary, timing, authority relationship, evidence requirement, and consequence posture.

### Strong Correlation Candidate

Use when the candidate formalism shares the same practical governance role but differs in scope, vocabulary, timing, authority model, or proof requirement.

### Overlap Or Adjacent Candidate

Use when the candidate formalism is nearby but does not match enough dimensions to support synonymy.

## Required Candidate Fields

```text
candidate_id
created_at
search_cycle_id
wiki_term_or_formalism
candidate_term
candidate_relationship
origin_type
origin_title
origin_url
origin_repository
origin_publisher
origin_stability
claim_summary
match_dimensions
mismatch_dimensions
overclaiming_risk
review_status
non_claims
```

## Review Rule

A candidate is not accepted into a glossary page, formalism page, ontology, or relationship summary until a decision record accepts it.

The wiki entity may create candidate records, but it must not promote a candidate to equivalent or synonymous status without review.

## Non-Claims

```text
Discovery is not acceptance.
Correlation is not equivalence.
A social post is not a formalism origin.
A candidate record does not prove admissibility.
A candidate record does not create source authority.
A candidate record does not grant execution authority.
```

## Cadence Recommendation

```text
weekly: scan known source families and subscribed formalism repositories
monthly: scan standards bodies, academic repositories, public specifications, and governance frameworks
quarterly: summarize accepted, denied, deferred, and unresolved relationship candidates
```

## Next Safe Build Target

Create a machine-readable candidate queue and validator for term-discovery records.
