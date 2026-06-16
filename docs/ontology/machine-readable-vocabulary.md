---
title: Machine-Readable Vocabulary
---

# Machine-Readable Vocabulary

The Admissibility Wiki includes a machine-readable vocabulary artifact for tools, agents, validators, docs generators, and future StegVerse ingestion engines.

## Artifact

```text
static/ontology/admissibility-vocabulary.v0.1.json
```

When the site is built, this artifact should be reachable at:

```text
https://admissibility.stegverse.org/ontology/admissibility-vocabulary.v0.1.json
```

## Purpose

The vocabulary artifact gives each core term:

- a stable identifier;
- a human label;
- a concise definition;
- a category;
- related terms;
- an implementation posture.

## Posture Values

Posture values should distinguish between:

```text
conceptual
implemented
experimental
proposed
external
```

## Editorial Rule

The JSON artifact should not overstate maturity.

A term can be central to StegVerse vocabulary while still being experimental or proposed in implementation.

## Usage Examples

Agents can use the artifact to:

- link a term to the correct wiki page;
- prevent vocabulary drift;
- map repo artifacts to public definitions;
- generate onboarding summaries;
- validate whether a document uses terms consistently.
