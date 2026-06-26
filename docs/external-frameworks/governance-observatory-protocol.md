---
title: Governance Observatory Protocol
---

# Governance Observatory Protocol

## Purpose

The External Frameworks section functions as a governance observatory.

It records how independently developed governance frameworks can be observed, mapped, and evaluated through StegVerse without requiring those frameworks to change their own terminology, claims, artifacts, or operating model.

## Done State

This protocol is satisfied when an external framework page:

1. states the external framework in its own terms;
2. separates published claims from StegVerse observations;
3. identifies native artifacts without treating them as StegVerse artifacts;
4. maps those artifacts into general governance primitives only where the mapping is explicit;
5. preserves the boundary that historical artifacts do not grant execution authority;
6. produces or references a non-authorizing Commitment Candidate when execution is proposed;
7. routes the candidate to SPE for commit-time standing determination;
8. reports ALLOW, DENY, or FAIL-CLOSED without expanding the external framework's claims.

## Core Assumption

External framework interoperability is not treated as framework adoption.

A framework may remain fully external while still producing artifacts that can be observed through the StegVerse governed-transition grammar.

## Two-Part Page Boundary

Each external framework page should keep two sections visibly separate.

```text
EXTERNAL FRAMEWORK RECORD

- framework purpose
- published source
- native terminology
- native artifacts
- stated claims
- stated non-claims
- allowed public usage, if known

STEGVERSE OBSERVATION RECORD

- translation into governance primitives
- commitment-candidate fields
- standing inputs
- SPE result
- assumptions
- non-assumptions
- receipts or replay package
```

The first section describes the framework. The second section records StegVerse's independent observation.

## General Evaluation Pattern

```text
External Framework
        |
        | native artifacts
        v
Published Output
        |
        | no modification of framework semantics
        v
StegVerse Translation Layer
        |
        | general governance primitives
        v
Commitment Candidate
        |
        | non-authorizing execution proposal
        v
Standing-Proof-Engine
        |
        | ALLOW / DENY / FAIL-CLOSED
        v
Evaluation Report
```

## Non-Authority Rule

No external artifact becomes execution authority by being included in the wiki.

```text
Declaration != execution authority
Evidence != execution authority
Trace != execution authority
Review != execution authority
Policy reference != execution authority
Commitment Candidate != execution authority
```

Only a current standing determination can support an execution boundary.

## Minimal Interoperability Contract

An external framework can participate in the observatory if it can provide at least one of the following without changing its own meaning:

- declaration;
- evidence;
- trace;
- review;
- policy reference;
- delegation reference;
- context reference;
- recoverability reference;
- other artifact relevant to a proposed transition.

StegVerse then records whether those artifacts can be mapped into the common governed-transition grammar.

## Governance Primitives

Mappings should prefer general terms rather than domain-specific implementations.

Core primitives include:

- actor;
- target;
- action;
- scope;
- authority;
- delegation;
- policy;
- evidence;
- context;
- recoverability;
- standing;
- consequence;
- continuity;
- constraint;
- ECAT;
- ICAT;
- BCAT;
- GCAT;
- %Existence.

## Result Semantics

SPE results should be recorded without overclaiming.

| Result | Meaning |
|---|---|
| ALLOW | Current standing was reconstructed sufficiently for the proposed commitment under the stated policy and context. |
| DENY | Current standing was reconstructed and does not authorize the proposed commitment. |
| FAIL-CLOSED | Current standing cannot be safely reconstructed, required inputs are missing, or the recoverability state is insufficient. |

## Observatory Non-Claims

```text
Observation is not endorsement.
Crosswalk is not adoption.
Mapping is not equivalence.
Historical review is not present authority.
A successful external framework output is not a StegVerse ALLOW.
A StegVerse result does not expand the external framework's published claims.
```

## Research Question

The repeated observatory question is:

```text
Can this external framework express its outputs in the common grammar of governed transitions while preserving its own internal semantics?
```

If multiple independent frameworks satisfy that question, the result supports the broader hypothesis that governed systems share a common transition grammar across domains.
