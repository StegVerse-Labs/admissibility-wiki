---
title: Canonical Decision Enum Registry
---

# Canonical Decision Enum Registry

## Purpose

This registry prevents public wiki, runtime, interop, and downstream documentation from drifting into incompatible decision-value sets.

The registry does not make every value interchangeable. It identifies which surface owns each value and whether the value belongs to runtime transition review, wiki governance, interop failure posture, or downstream status display.

## Page Status

```text
active
```

## Page Posture

```text
governance registry
```

## Boundary

This page is a vocabulary registry. It does not grant production status, runtime standing, SPE standing resolution, or public-page authority.

## Runtime Transition Surface

Runtime transition decisions are intentionally narrow.

```text
ALLOW
DENY
DEFER
```

These values answer whether a governed transition may continue at the checked boundary under the current evidence, authority, and policy posture.

## Wiki Governance Surface

Wiki governance decisions resolve public documentation proposals and page changes. They are not runtime transition decisions.

```text
ALLOW
ALLOW_AS_OVERLAP
DENY
DEFER
ESCALATE
REFUSE
SUPERSEDE
```

`ALLOW_AS_OVERLAP`, `ESCALATE`, `REFUSE`, and `SUPERSEDE` are documentation governance outcomes. They must not be presented as runtime transition values.

## Interop Failure and Status Terms

Interop and downstream systems may need status values that describe why standing could not be established or why a transition did not continue.

```text
FAIL-CLOSED
FAIL_CLOSED
CONDITIONAL
```

These terms are status labels unless a destination schema explicitly maps them to a local field. They must not be silently mixed into the runtime transition enum.

## Surface Mapping

| Value | Runtime transition | Wiki governance | Interop/downstream status | Notes |
| --- | --- | --- | --- | --- |
| `ALLOW` | yes | yes | mapped only | Scope must be stated. |
| `DENY` | yes | yes | mapped only | Scope must be stated. |
| `DEFER` | yes | yes | mapped only | No final proceed state yet. |
| `ALLOW_AS_OVERLAP` | no | yes | no | Documentation overlap or mapping only. |
| `ESCALATE` | no | yes | mapped only | Moves review to a higher review path. |
| `REFUSE` | no | yes | mapped only | Request is outside the page-governance boundary. |
| `SUPERSEDE` | no | yes | mapped only | Replaced by newer record or authority. |
| `FAIL-CLOSED` | no | no | yes | Hyphenated status form. |
| `FAIL_CLOSED` | no | no | yes | Underscore machine-readable status form. |
| `CONDITIONAL` | no | no | yes | Must name the conditions. |

## Required Use Rule

Any page, schema, status file, or receipt that publishes a decision or status value must identify the enum surface it uses.

Allowed surface labels:

```text
runtime_transition_decision
wiki_governance_decision
interop_failure_posture
downstream_status_label
```

## Dead-Basis Discipline

A value copied from one surface to another without an explicit mapping is a dead-basis risk. The visible word may remain the same while the standing basis has changed.

## Machine-Readable Registry

Machine-readable registry:

```text
static/ontology/canonical-decision-enum-registry.v0.1.json
```

## Related Pages

- [Decision Record](./decision-record.md)
- [Proposal Lifecycle](./proposal-lifecycle.md)
- [Commit-Time Admissibility](../formalisms/commit-time-admissibility.md)
- [Governed Transition Map](./governed-transition-map.md)
