---
title: Commit-Time Interoperability Contract
---

# Commit-Time Interoperability Contract

## Purpose

This page defines the minimal contract used to evaluate external governance artifacts through StegVerse without converting the external framework into StegVerse.

The contract keeps two boundaries clear:

```text
Historical governance artifacts may support evaluation, but they do not authorize execution.
An ALLOW standing determination establishes admissibility, but it is not an execution command.
```

## Done State

An interoperability run is complete when:

1. the external artifact is identified;
2. the artifact's native claim is preserved;
3. any translation into StegVerse primitives is recorded;
4. a Commitment Candidate is created or referenced;
5. the Commitment Candidate remains non-authorizing;
6. SPE reconstructs current standing at commit time;
7. the result is recorded as ALLOW, DENY, or FAIL-CLOSED in a Standing Determination Receipt;
8. execution remains a distinct downstream boundary;
9. assumptions and non-claims are explicit.

## Contract Layers

| Layer | Function | Authority Boundary |
|---|---|---|
| External framework artifact | Declares, evidences, traces, reviews, or otherwise describes part of a governance path. | Does not grant StegVerse execution authority. |
| Translation mapping | Expresses relevant artifact fields as general governance primitives. | Does not alter the external framework's native meaning. |
| Commitment Candidate | Identifies the proposed actor, target, action, scope, context, and validity window. | Does not authorize execution and must not inherit authority from any prior artifact, reviewer, agent, evidence packet, or approval. |
| SPE standing determination | Reconstructs current standing from policy, delegation, evidence, execution context, validity state, and recoverability. | Returns ALLOW, DENY, or FAIL-CLOSED as an admissibility determination, not an execution command. |
| Standing Determination Receipt | Records the SPE result and the reconstructed basis for that result. | Auditable proof artifact distinct from the non-authorizing Commitment Candidate; does not itself execute the transition. |
| Execution boundary | The point where consequence may bind. | Must remain separate from standing determination and may proceed only under the governing execution policy. |

## Commitment Candidate Fields

A Commitment Candidate should include the minimum fields needed to propose a specific crossing point.

| Field | Purpose |
|---|---|
| transition_id | Identifies the proposed transition. |
| requested_action | States the action being proposed. |
| actor | Identifies who or what would act. |
| target | Identifies what would be affected. |
| scope | States the boundary of the requested action. |
| policy_reference | Points to the policy claimed to govern the transition. |
| delegation_reference | Points to the delegation or authority source, if any. |
| evidence_references | Points to evidence, traces, reviews, or declarations. |
| execution_context | States current context at the proposed crossing point. |
| validity_window | States when the request is valid, if at all. |
| recoverability_profile | Describes whether the boundary remains recoverable if authority, context, or execution conditions degrade. |

## Required Separation

```text
External review artifact -> historical evidence
Commitment Candidate -> proposed crossing, no authority
SPE -> current standing determination
Standing Determination Receipt -> auditable result artifact
Execution -> consequence binding
```

No layer should silently inherit authority from an earlier layer.

## Result Semantics

```text
ALLOW
  Current standing is reconstructable and the proposed crossing is admissible
  under the governing policy. This is not an execution command.

DENY
  Current standing is reconstructable and known to reject the proposed crossing.

FAIL-CLOSED
  Admissibility cannot be safely established because required current state is
  incomplete, ambiguous, stale, unreachable, unverifiable, corrupted, tampered,
  contradictory, or unrecoverable.
```

FAIL-CLOSED is not a stronger DENY. DENY is a known negative determination. FAIL-CLOSED means the system cannot safely determine admissibility from the available current state.

## Commit-Time Reconstruction Basis

Current standing must be freshly reconstructed against the specific:

```text
actor
target
action
scope
policy version
delegation chain
evidence state
execution context
validity window
recoverability state
```

Historical review may remain reconstructable and useful, but it cannot substitute for this commit-time reconstruction.

## Fail-Closed Triggers

SPE should return FAIL-CLOSED when current standing cannot be safely reconstructed.

Common triggers include:

- missing policy reference;
- ambiguous or unresolvable policy version;
- expired, missing, partially revoked, or unreachable delegation;
- actor substitution;
- target substitution, aliasing, or resource-identity ambiguity;
- scope mismatch;
- stale evidence;
- evidence hash mismatch or tampered referenced evidence;
- missing or unreachable historical review artifact when it is required by policy;
- changed policy version;
- degraded recoverability;
- rollback target change or unavailable recovery path;
- context mismatch;
- invalid or expired validity window;
- clock skew or unavailable trusted time source;
- tool or action semantic drift between review and commit;
- incomplete receipt chain;
- contradiction between supplied artifacts and current standing.

A policy may classify a fully reconstructable invalid state as DENY. It must not classify an unresolved reconstruction state as ALLOW.

## External Framework Examples

| Framework | Native contribution | Commitment use |
|---|---|---|
| GLM | Declared claims, non-claims, scope, composition, and interpretation frame. | May inform policy, scope, and context references. |
| EVIDE | Post-event evidentiary deposit and reconstructability support. | May inform evidence and continuity references. |
| DecisionAssure | Trace integrity and causal-continuity package. | May inform evidence, chronology, drift, and causal-continuity references. |
| MindForge | Historical governance review evidence. | May inform review posture and evidence references, but not execution authority. Discussion-derived MindForge mappings are not an official specification, certification, endorsement, or implementation claim. |

## Non-Claims

```text
This contract does not certify external frameworks.
This contract does not require external frameworks to adopt StegVerse terminology internally.
This contract does not treat upstream artifacts as authorization.
This contract does not convert a review-time PASS into commit-time ALLOW.
This contract does not convert commit-time ALLOW into an execution command.
This contract does not prove broad compatibility beyond the evaluated artifact package.
Discussion-derived external-framework mappings are not official specifications or endorsements.
```

## Minimal Test Pattern

```text
Input: external artifact package
Map: artifact fields to governance primitives
Build: non-authorizing Commitment Candidate
Evaluate: SPE reconstructs current standing
Return: ALLOW / DENY / FAIL-CLOSED
Record: Standing Determination Receipt, assumptions, non-claims, and replay path
Execute: only through a separate governed execution boundary
```

## Core Principle

A system is not admissible merely because it can prevent failure.

A consequential transition is admissible only if execution authority remains reconstructable and valid at the moment consequence binds.