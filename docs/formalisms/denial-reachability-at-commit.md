---
title: Denial Reachability at the Commit Boundary
---

# Denial Reachability at the Commit Boundary

## Status

`PUBLIC_CONCEPTUAL_FORMALISM / NON_EXECUTION_AUTHORITY`

This page defines a necessary condition for governable consequence-binding action. It does not itself grant execution authority, certify a runtime, or replace the proof authority of `Data-Continuation/formalism-tests`.

## Core rule

At the exact boundary where an outcome becomes real, authorization is valid only when both conditions are resolved from the current state:

1. the proposed transition is admissible; and
2. denial remains reachable and enforceable.

If denial is no longer reachable, the action is not being authorized at that boundary. It is being inherited from prior momentum, prior commitment, architecture, latency, or an earlier decision.

Therefore:

> Authorization without a reachable refusal path is not a decision. It is a forced transition.

## Why re-derivation alone is insufficient

Re-deriving authority against live state is necessary but not sufficient. A system may recompute policy, identity, delegation, evidence freshness, or environmental state after the control surface has already lost the practical ability to stop execution.

Such a system may still emit `ALLOW`, but the result is cosmetic because the deny outcome cannot be made real.

A valid commit-time decision must therefore prove not only that `ALLOW` can be justified, but that `DENY` remains an available outcome of the same boundary.

## Commit-boundary predicate

For a transition candidate `τ` evaluated in current state `s`:

```text
COMMIT_PERMITTED(τ, s) :=
  ADMISSIBLE(τ, s)
  AND AUTHORITY_CURRENT(τ, s)
  AND STATE_SUFFICIENT(τ, s)
  AND DENIAL_REACHABLE(τ, s)
  AND DENIAL_ENFORCEABLE(τ, s)
```

If either denial predicate is false:

```text
COMMIT_PERMITTED(τ, s) = false
DECISION_POSTURE = FAIL_CLOSED
FAILURE_CLASS = INHERITED_AUTHORIZATION
```

## Reachability and enforceability

`DENIAL_REACHABLE` means the present system state still contains a valid path to a deny result before consequence binds.

`DENIAL_ENFORCEABLE` means the deny result can actually prevent the actuator, transaction, publication, dispatch, mutation, or other consequence-binding operation.

A merely representable deny state is insufficient. The refusal must be capable of changing what happens next.

## Governability condition

A system remains governable at a transition boundary only while both continuation and refusal remain possible outcomes under current authority.

The relevant control surface is therefore not merely the set of admissible next states. It is the subset in which the system retains an effective choice between:

```text
ALLOW -> execute the admissible transition
DENY  -> prevent the transition from becoming real
```

Once refusal is unreachable or unenforceable, the system has crossed from governance into inevitability, even if an authorization calculation still runs.

## Failure classes

### Inherited authorization

The runtime reports or reconstructs authorization after the deny path has already disappeared.

### Momentum capture

Prior scheduling, buffering, delegation, propagation, or actuator commitment makes the current boundary unable to stop the action.

### Cosmetic gating

A policy or authority check remains present, but its output cannot affect execution.

### Late refusal

A deny result is produced only after consequence has bound, converting prevention into recovery or post-hoc control.

### Split-boundary insufficiency

State sufficiency, authority, and enforcement are resolved in separate layers without a single boundary that can still deny the action.

## Evidence requirements

A claim that denial remained reachable should be supported by evidence identifying:

- the exact consequence-binding boundary;
- the current transition candidate and state reference;
- the authority and delegation reconstructed at that boundary;
- the deny path available from that state;
- the enforcement mechanism that would stop the action;
- the latest time at which denial remains effective;
- the observed `ALLOW`, `DENY`, `ESCALATE`, or `FAIL_CLOSED` result;
- a receipt or trace proving that the result controlled execution.

A policy evaluation log without enforcement evidence does not prove denial reachability.

## Relationship to StegVerse decisions

This condition refines commit-time admissibility:

```text
proposal
-> evidence and authority reconstruction
-> current-state sufficiency
-> denial-reachability proof
-> admissibility decision
-> enforceable ALLOW or DENY
-> consequence binds only after ALLOW
-> receipt and reconstruction evidence
```

It also preserves the distinction:

```text
before commit: governance can prevent
post commit: governance can only recover, compensate, or reconstruct
```

## Non-claims

This formalism does not claim that every system can prove denial reachability with zero latency, that all actions are reversible, or that the presence of a stop mechanism alone proves admissibility.

It claims only that where a system represents an outcome as presently authorized, the ability to refuse must still be real at that same boundary. Otherwise the authorization is inherited rather than decided.

## Durable rule

```text
RULE DR-1:
A consequence-binding transition MUST NOT be authorized unless denial remains reachable and enforceable from the current state until the authorization result controls execution.

RULE DR-2:
If denial is unreachable or unenforceable, the transition MUST fail closed and be classified as inherited authorization, forced transition, or an equivalent governed failure class.

RULE DR-3:
Post-hoc cancellation, rollback, audit, monitoring, or recovery MUST NOT be represented as proof that denial was reachable at commit time.
```
