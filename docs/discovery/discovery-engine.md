---
title: Formalism Discovery Engine
---

# Formalism Discovery Engine

## Purpose

The Formalism Discovery Engine is the wiki layer responsible for discovering candidate terminology, concept, and relationship matches across formal origins.

It does not create source authority. It does not automatically merge terms. It produces reviewable candidates with provenance.

## Done Condition

This layer is minimally active when the wiki can:

```text
1. Read approved public-safe formalism sources.
2. Build a term index with source origin references.
3. Generate candidate relationships between terms and concepts.
4. Preserve evidence for each candidate.
5. Place candidates into a review queue.
6. Require explicit review before any synonym, equivalence, dependency, or conflict claim is promoted.
```

## Scope

The engine may observe:

```text
formalism pages
formalism registries
publication artifacts
proof candidates
validation candidates
reference implementation metadata
external crosswalk records
```

The engine must not treat LinkedIn comments, social posts, or informal discussions as formal origins unless they point to a formal artifact elsewhere.

## Core Objects

| Object | Role |
|---|---|
| Formalism | Canonical or external source being indexed. |
| Term | Named expression found in a source. |
| Concept | Meaning-bearing cluster derived from terms and definitions. |
| Relationship | Candidate connection between terms, concepts, or formalisms. |
| Evidence | Source text, hash, path, or citation supporting a candidate. |
| Origin | Formal source location from which evidence was derived. |
| Review | Human or governed process that accepts, rejects, or reclassifies a candidate. |
| Decision | Final reviewed relationship posture. |

## Candidate Lifecycle

```text
observed
indexed
candidate_generated
review_required
accepted
rejected
superseded
```

## Authority Boundary

Candidate discovery is not equivalence.

A relationship candidate may indicate possible similarity, dependency, conflict, or overlap. It does not create a wiki claim until reviewed.

## Non-Claims

```text
The discovery engine does not define formal terms.
The discovery engine does not prove relationship equivalence.
The discovery engine does not merge external frameworks into StegVerse.
The discovery engine does not promote candidates without review.
```
