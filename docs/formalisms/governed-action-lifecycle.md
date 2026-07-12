---
title: Governed Action Lifecycle
---

# Governed Action Lifecycle

## Status

Canonical explanatory lifecycle connecting proposal, commit-time revalidation, bounded execution, recovery, and reconstruction.

## Purpose

AI governance should not be modeled as a single approval event or as a promise that an intelligent system will always be correct.

A consequential action moves through multiple governance responsibilities. Those responsibilities are related, but they are not interchangeable.

```text
proposal
  -> commit-time revalidation
  -> bounded execution
  -> consequence observation
  -> recovery, correction, or accountability
  -> reconstruction
```

## 1. Proposal

A model, person, institution, or automated process proposes an action using the evidence and context available at an earlier decision time.

Proposal establishes a candidate transition. It does not create execution authority.

## 2. Commit-Time Revalidation

Immediately before commitment, the system evaluates whether the original basis for action still retains standing.

The revalidation scope includes:

- evidence freshness and sufficiency;
- policy validity;
- actor and delegation authority;
- consent;
- execution scope;
- current context;
- consequence and irreversibility;
- available recovery paths.

The governing relationship is:

\[
ValidAt(t_0) \not\Rightarrow ValidAt(t_c)
\]

A prior approval does not automatically survive materially changed conditions.

The commit-time governance function returns:

\[
\Gamma(T_{t_c}) \rightarrow \{ALLOW, DENY, DEFER, ESCALATE\}
\]

Only `ALLOW` permits the declared bounded execution path. `DENY`, `DEFER`, and `ESCALATE` are governed outcomes rather than operational failures.

## 3. Bounded Execution

An admitted action must remain inside the authority, scope, rate, consequence, and destination boundaries that were evaluated.

Execution success is not proof that the transition was admissible:

\[
OperationalSuccess \not\Rightarrow Admissible
\]

The execution boundary should preserve interruption, observation, and rollback where the action class allows them.

## 4. Consequence Observation

The system observes whether the realized outcome remains within the expected and authorized consequence envelope.

Observation should distinguish:

- expected result;
- actual result;
- material deviation;
- emerging harm;
- authority or policy drift during execution;
- loss of recoverability;
- downstream propagation.

A change during execution may require interruption, containment, or a new governed transition rather than automatic continuation.

## 5. Recovery, Correction, and Accountability

Commit-time validation cannot eliminate all error. Recovery governance therefore defines what happens when an admitted action still produces an incorrect, harmful, or unforeseen result.

The response set may include:

\[
\mathcal{R}=\{rollback, repair, compensate, contain, appeal, learn\}
\]

Recovery does not retroactively make an inadmissible action legitimate. Likewise, a valid pre-commit decision does not erase obligations created by a harmful result.

## 6. Reconstruction

Reconstruction determines what occurred and whether each lifecycle responsibility was satisfied.

A reconstructable record should allow an independent reviewer to derive:

- what was proposed;
- what evidence, policy, delegation, consent, and context existed at commitment;
- what disposition was calculated;
- what execution boundary was authorized;
- what actually occurred;
- what recovery paths were available and used;
- what obligations remain.

Reconstructability is necessary but not sufficient:

\[
Reconstructable \not\Rightarrow LegitimateAtCommit
\]

## 7. Responsibility Separation

| Lifecycle responsibility | Governing question |
|---|---|
| Proposal | What action is being considered? |
| Commit-time revalidation | Does the action still have standing now? |
| Bounded execution | Is execution staying within the admitted boundary? |
| Consequence observation | Is the realized result diverging from the authorized envelope? |
| Recovery governance | What correction, containment, compensation, appeal, or accountability is now required? |
| Reconstruction | Can the complete basis and consequence path be independently derived? |

## 8. Relationship to Other Formalisms

- [Inference-Window and Irreversibility-Bounded Governance](./inference-window-irreversibility-governance.md) defines the operational commit-time evaluation model.
- [Commit-Time Admissibility](./commit-time-admissibility.md) establishes the requirement that standing be evaluated at commitment.
- [Irreversibility-Inference Convergence Theorem](./irreversibility-inference-convergence-theorem.md) is a theorem candidate about architectural convergence under repeated admissibility optimization.
- [Decision Continuity](./decision-continuity.md) addresses preservation of decision standing and downstream obligations.

## 9. Claims Boundary

This lifecycle does not guarantee correctness, prove legal compliance, grant execution authority, or establish that every action can be recovered.

It defines where governance responsibilities occur and prevents pre-commit revalidation, execution, recovery, and reconstruction from being collapsed into a single success claim.

> The objective is not perfect prediction or recovery alone. It is preventing stale justification from becoming irreversible action while preserving a governed destination for errors that cannot be eliminated.
