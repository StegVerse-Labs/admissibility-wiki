---
title: Optimization Target Binding at Commit
---

# Optimization Target Binding at Commit

## Problem

AI governance discussions often identify ownership, policy, accountability, and risk categories while leaving the system's optimization target implicit.

An implemented framework can be internally consistent, operational, and faithful to its written methodology while still producing an inadmissible transition. Design-time correctness does not establish commit-time authority.

## Core rule

A consequence-binding transition MUST NOT be authorized unless the optimization target is:

1. explicit before execution;
2. bound to the current transition request and current state;
3. derived from an identified policy and delegation source;
4. protected against unauthorized mutation;
5. evaluated together with current evidence, constraints, and authority;
6. subject to an enforceable DENY or FAIL-CLOSED result before the actuator boundary.

Making an objective visible is insufficient when it is inherited from prior context, cached from an earlier evaluation, inferred from undocumented criteria, or detached from the state that will be changed.

## Minimal commitment candidate

```text
transition_id
action
actor
target
current_state_reference
optimization_target
optimization_criteria
policy_reference
delegation_reference
evidence_references
validity_window
recoverability_profile
mutation_provenance
execution_boundary
```

## Commit-time predicate

Let:

```text
T = proposed transition
O = explicit optimization target
S_c = current state at commit
P = current policy reconstruction
D = current delegation reconstruction
E = current evidence set
R = denial reachability and enforceability
```

Authorization requires:

```text
EXPLICIT(O)
AND BOUND(O, T, S_c)
AND DERIVED_FROM(O, P, D)
AND MUTATION_PROVENANCE_VALID(O)
AND EVIDENCE_CURRENT(E)
AND TRANSITION_ADMISSIBLE(T, O, S_c, P, D, E)
AND DENIAL_REACHABLE(R)
AND DENIAL_ENFORCEABLE(R)
```

If any term is false or cannot be reconstructed, the result is `FAIL_CLOSED`.

## Failure classes

- `IMPLICIT_OPTIMIZATION_TARGET`: the objective cannot be enumerated before execution.
- `STALE_TARGET_BINDING`: the objective was valid for an earlier state but was not rebound to current state.
- `UNAUTHORIZED_TARGET_MUTATION`: the objective or its criteria changed without valid authority.
- `INHERITED_AUTHORIZATION`: execution relies on prior approval rather than current standing.
- `OBJECTIVE_POLICY_DIVERGENCE`: the implemented target no longer matches reconstructed policy.
- `DENIAL_UNREACHABLE`: a negative result cannot prevent the consequence-binding operation.

## Governance distinction

```text
System matches framework
!= optimization target is explicit
!= target is currently authorized
!= resulting transition is admissible
!= denial can still control execution
```

The relevant governance authority is therefore not merely who owns the system, but who defined the target, who may mutate it, how that authority is reconstructed, and whether the current transition can still be refused before it becomes real.

## Source posture

This formalism was prompted by a conversation-supplied LinkedIn exchange concerning explicit optimization targets, production governance systems, and execution-time validity. It records the derived StegVerse governance distinction; it does not certify, validate, or characterize any named external system.

## Authority boundary

`admissibility-wiki` owns the public vocabulary and explanation. Executable proof fixtures and expected outcomes belong in `Data-Continuation/formalism-tests`. Site and Publisher may mirror or index this formalism only after repository validation and public-route verification pass.
