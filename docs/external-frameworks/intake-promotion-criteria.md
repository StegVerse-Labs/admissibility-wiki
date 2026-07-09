---
title: External Framework Intake Promotion Criteria
---

# External Framework Intake Promotion Criteria

## Purpose

This page defines how a source-required candidate from [Expanded External Framework Intake](./expanded-framework-intake.md) may be promoted into a sourced intake record, page candidate, benchmark mapping candidate, or fixture candidate.

Promotion is evidence-governance work. It is not endorsement, certification, equivalence, or execution authority.

## Promotion Gates

A candidate may not be promoted unless all required gates are satisfied.

| Gate | Required Evidence |
|---|---|
| canonical_source | Official website, standard, paper, repository, specification, or release artifact. |
| source_version | Version, publication date, release tag, commit, retrieval date, or stable URL. |
| published_scope | What the framework claims to do in its own terms. |
| published_non_claims | What it does not claim, or a documented StegVerse non-claim boundary if no explicit non-claims exist. |
| artifact_type | What artifact the framework emits or governs. |
| relationship_class | One of synonymous, adjacent, new, unresolved. |
| benchmark_relevance | Which benchmark dimensions may apply. |
| authority_boundary | Explicit statement that the candidate does not grant StegVerse authority. |
| evidence_posture | Whether the evidence is source-only, implementation evidence, observed behavior, or interoperability evidence. |

## Promotion States

| State | Meaning |
|---|---|
| source_required | Candidate has not yet supplied a canonical source. |
| sourced_intake | Canonical source exists; no full page yet. |
| page_candidate | Candidate is ready for a framework page. |
| mapping_candidate | Candidate is ready for benchmark mapping. |
| fixture_candidate | Candidate is ready for non-authorizing fixture examples. |
| deferred | Candidate is intentionally deferred with reason. |

## Required Promotion Record

Every promoted candidate must have a promotion record:

```text
candidate_id
name
canonical_source
source_version_or_date
published_scope
published_non_claims
artifact_type
relationship_class
benchmark_relevance
authority_boundary
evidence_posture
promotion_state
next_action
```

## Non-Claims

```text
promotion != certification
promotion != endorsement
promotion != equivalence
promotion != execution authority
promotion != StegVerse standing
promotion != benchmark pass
```

Promotion means the candidate has enough source material to be handled responsibly by the observatory. It does not mean the framework is correct, complete, compatible, or authorized.
