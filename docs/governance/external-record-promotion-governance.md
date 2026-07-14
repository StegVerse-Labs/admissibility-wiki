---
title: External Record Promotion Governance
---

# External Record Promotion Governance

## Purpose

This page defines how external bibliographic and translation records move between governance postures.

Promotion governs wiki record standing only. It does not validate a source paper, prove a physical theory, establish equivalence with GCAT or BCAT, replace specialist review, or create execution authority.

## Allowed Results

| Result | Meaning |
|---|---|
| `MAP` | The source-safe mapping is sufficiently structured for crosswalk use. |
| `ACCEPT` | The mapping has a confirmed source basis, sufficient evidence, declared review authority, and a standing decision record. |
| `DEFER` | The mapping is preserved but cannot advance until a named missing condition is satisfied. |
| `DISPUTE` | A material conflict or objection prevents settled use. |
| `ESCALATE` | Specialist or higher-authority review is required. |
| `REFUSE` | The request cannot be evaluated safely as framed or lies outside declared scope. |
| `SUPERSEDE` | A newer record replaces the prior record without erasing its history. |

## MAP Requirements

A record may receive `MAP` only when all of the following are present:

```text
source-safe native meaning
stable internal evidence reference
explicit Transition Table role
linked translation-record IDs
linked mathematics-crosswalk IDs when applicable
explicit source boundary
explicit non-claims
```

## ACCEPT Requirements

A record may receive `ACCEPT` only when all MAP requirements are satisfied and the record also has:

```text
source-confirmed bibliographic locator
sufficient evidence posture
declared reviewer authority class
decision record
no unresolved material contradiction
```

## Current Decision

```text
decision_id: decision-lai-intake-defer-v0-1
result: DEFER
target: Lai operational architecture bibliographic intake and five external translation records
reason: durable source-evidence summary exists, but stable external locator and independent bibliographic confirmation are still missing
resulting posture: deferred
owner: Admissibility Wiki proposal and decision governance
```

The decision preserves the records without promoting them to mapped or accepted.

## Decision Sequence

```text
source observation
-> evidence record
-> bibliographic intake
-> translation mapping
-> validation
-> authority-class review
-> MAP / ACCEPT / DEFER / DISPUTE / ESCALATE / REFUSE / SUPERSEDE
-> decision receipt and reconstruction path
```

## Non-Claims

A promotion decision governs wiki record posture. It does not decide whether the source physics is true, predictive, peer-reviewed, novel, or equivalent to StegVerse mathematics.
