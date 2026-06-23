---
title: Commit-Time Admissibility
---

# Commit-Time Admissibility

## Canonical Source Repository

`Admissible-Existence/CTA`

## Definition

Commit-Time Admissibility is the governing formalism for determining whether a proposed transition still has standing at the moment it crosses into commitment.

CTA does not ask only whether a transition was previously reviewed, approved, or explainable. It asks whether the transition may bind now.

## Scope

CTA applies to consequence-bearing transitions where review, policy, delegation, evidence, context, memory, or recoverability may change between review and commitment.

## Purpose

CTA separates historical review from present standing.

A review artifact may preserve prior reasoning. A commitment candidate presents a transition for possible commitment. Standing reconstruction determines whether standing still exists at commit time.

## Core Constructs

- Review Artifact
- Commitment Candidate
- Standing Reconstruction
- Commit-Time Determination
- Receipt Chain
- Commitment or Denial

## Transition Element Construction

```text
Review Artifact
  -> Commitment Candidate
  -> Standing Reconstruction
  -> Commit-Time Determination
  -> Receipt Chain
  -> Commitment or Denial
```

## Required Standing Inputs

- transition identity
- requested action
- actor identity
- target scope
- authority class
- policy reference
- delegation reference, if delegated
- evidence references
- execution context
- validity window
- recoverability profile
- memory posture, if memory is used
- current state hash or equivalent state reference
- decision result
- receipt reference

## Decision Outcomes

- `ALLOW` — current standing exists and the transition may bind under declared conditions.
- `DENY` — current standing does not exist.
- `FAIL_CLOSED` — required standing cannot be reconstructed or evaluated safely.
- `ESCALATE` — the evaluator cannot decide without higher or different review.
- `REFUSE` — the request is outside declared scope or lacks a valid transition basis.

## Validation Candidates

Current baseline validation is maintained in the source repository:

```text
tests/run_cta_tests.py
tests/fixtures/cta_cases.json
```

Expected current result:

```text
CTA baseline tests passed: 5 cases
```

## Mirror Handoff

Current root handoff:

```text
CTA_MIRROR_HANDOFF.md
```

The handoff identifies source files, downstream mirror targets, validation command, expected result, install order, and boundary statements.

## Related Formalisms

- [Irreversibility-Inference Convergence Theorem](./irreversibility-inference-convergence-theorem.md)
- [Transition Table](./transition-table.md)
- [Runtime Transition Governance](./runtime-transition-governance.md)
- [Decision Continuity](./decision-continuity.md)
- [Continuity Handoff Formalism](./continuity-handoff-formalism.md)
- [Admissible-Existence Validation Factory](./admissible-existence-validation-factory.md)

## Non-Claims

```text
The wiki does not define CTA source standing.
The wiki does not prove CTA by listing it.
CTA baseline tests do not prove the complete formalism.
A review artifact does not create present standing by itself.
CTA repository existence does not create standing.
IICT does not replace CTA.
```
