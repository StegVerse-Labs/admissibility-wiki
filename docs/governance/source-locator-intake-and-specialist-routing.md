---
title: Source Locator Intake and Specialist Routing
---

# Source Locator Intake and Specialist Routing

## Purpose

This page defines the deterministic path for re-evaluating deferred external records when a stable source becomes available.

The path separates locator verification from specialist review and from governance promotion.

```text
source locator submission
-> locator verification
-> evidence and bibliography reconciliation
-> specialist review routing
-> review outputs
-> promotion decision
```

## Locator Verification Results

| Result | Meaning |
|---|---|
| `CONFIRMED` | The locator resolves to the declared source and supplies stable source identity. |
| `PARTIAL` | The locator is stable and relevant but does not supply the complete source or all required bibliographic fields. |
| `UNRESOLVED` | No stable locator is available or the locator cannot be verified. |
| `CONFLICTING` | The locator resolves to material that conflicts with the declared source identity or record. |
| `REJECTED` | The locator is invalid, unrelated, unsafe, or outside the declared intake scope. |

## Allowed Locator Types

```text
URL
DOI
arXiv identifier
repository path
publisher record
citation record
```

## Specialist Review Classes

| Review class | Scope |
|---|---|
| `physics_foundations` | Emergent spacetime, quantum foundations, relativity, modular time, and entanglement-gravity arguments. |
| `mathematical_formalism` | Operators, assumptions, derivations, domains, limitations, and equivalence claims. |
| `admissibility_governance` | Transition Table roles, authority boundaries, evidence posture, and promotion standing. |

## Current Route

```text
route_id: route-lai-operational-architecture-v0-1
current_gate: SOURCE_LOCATOR_REQUIRED
current_result: DEFER
required_reviews:
  - physics_foundations
  - mathematical_formalism
  - admissibility_governance
re-evaluation trigger: locator becomes CONFIRMED or PARTIAL with a stable retrievable source
```

## Deterministic Re-evaluation Rule

When the locator result changes to `CONFIRMED` or qualifying `PARTIAL`, the route must:

1. confirm the source identity against the bibliographic intake;
2. compare the durable evidence summary with the retrievable source;
3. identify drift, omissions, or contradictions;
4. route the source to all required specialist classes;
5. preserve each review result separately;
6. issue a new promotion decision; and
7. supersede, but never erase, the earlier deferred decision.

## Non-Claims

Locator verification does not validate a source theory. Specialist routing does not imply specialist endorsement. A routing record does not create acceptance authority or execution authority.
