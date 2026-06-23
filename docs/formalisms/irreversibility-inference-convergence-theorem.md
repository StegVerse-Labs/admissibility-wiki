---
title: Irreversibility-Inference Convergence Theorem
---

# Irreversibility-Inference Convergence Theorem

## Canonical Source Repository

`Admissible-Existence/IICT`

## Definition

The Irreversibility-Inference Convergence Theorem, or IICT, is a theorem candidate under Commit-Time Admissibility.

IICT proposes that governance systems subjected to repeated admissibility optimization converge toward structures that minimize the distance between irreversible commitment and the final admissible inference while preserving reconstructability.

## Relationship to CTA

IICT is for Commit-Time Admissibility. It does not replace Commit-Time Admissibility.

Commit-Time Admissibility asks whether a transition still has standing at the moment of commitment.

IICT asks whether repeated admissibility optimization causes governance systems to converge toward structures that make commit-time standing necessary or optimal.

## Core Theorem Candidate

A governance system subjected to repeated admissibility optimization will converge toward structures that minimize the distance between irreversible commitment and the final admissible inference while preserving reconstructability.

## Core Terms

| Term | Definition |
|---|---|
| Inference Window | The interval in which authority, policy, evidence, context, delegation, and memory are still valid enough to support a standing determination. |
| Point of Irreversibility | The point after which an action cannot be fully recalled, reversed, re-bound, or restored to its prior admissible state. |
| Governance Distance | The distance between the final valid inference and the point of irreversibility. |
| Final Valid Inference | The most recent inference that still retains standing under current authority, policy, evidence, context, delegation, and memory conditions. |
| Irreversible Commitment | The crossing point where a proposed transition becomes practically, procedurally, or materially non-recoverable without a new recovery or remediation process. |
| Reconstructability | The ability to recover the evidence, receipts, policy references, state, context, and decision path needed to explain or replay why a transition did or did not have standing. |
| Admissibility Geometry | The structural relationship among authority, policy, evidence, context, delegation, memory, inference timing, and irreversible action. |

## Transition Element Construction

```text
Inference Window Declaration
  -> Irreversibility Point Declaration
  -> Governance Distance Measurement
  -> Convergence Observation
  -> Theorem Evaluation
```

## Expected Structural Classes

- clean admissible path
- stale but reconstructable path
- authority gap
- delegation leak
- memory contamination
- context collapse
- fail-closed recovery path

## Validation Candidates

Current baseline validation is maintained in the source repository:

```text
tests/run_iict_tests.py
tests/fixtures/iict_cases.json
```

Expected current result:

```text
IICT baseline tests passed: 5 cases
```

## Mirror Handoff

Current root handoff:

```text
IICT_MIRROR_HANDOFF.md
```

The handoff identifies source files, downstream mirror targets, validation command, expected result, install order, and boundary statements.

## Related Formalisms

- [Commit-Time Admissibility](./commit-time-admissibility.md)
- [Transition Table](./transition-table.md)
- [Runtime Transition Governance](./runtime-transition-governance.md)
- [Decision Continuity](./decision-continuity.md)
- [State Transition Continuity Model](./state-transition-continuity-model.md)
- [Admissible-Existence Validation Factory](./admissible-existence-validation-factory.md)

## Publisher Artifacts

Publisher currently carries `sv-iict-2026` as a draft paper record. The draft record does not imply peer review completion or theorem proof.

## Non-Claims

```text
The wiki does not prove IICT by listing it.
IICT baseline tests do not prove the theorem.
IICT does not replace Commit-Time Admissibility.
A theorem-supporting case is not final theorem validation.
A public page is not proof of admissibility by itself.
```
