---
title: Commit-Time Interoperability Contract
---

# Commit-Time Interoperability Contract

## Purpose

This page defines the minimal contract used to evaluate external governance artifacts through StegVerse without converting the external framework into StegVerse.

The contract keeps one boundary clear:

```text
Historical governance artifacts may support evaluation, but they do not authorize execution.
```

## Done State

An interoperability run is complete when:

1. the external artifact is identified;
2. the artifact's native claim is preserved;
3. any translation into StegVerse primitives is recorded;
4. a Commitment Candidate is created or referenced;
5. the Commitment Candidate remains non-authorizing;
6. SPE reconstructs current standing at commit time;
7. the final result is recorded as ALLOW, DENY, or FAIL-CLOSED;
8. assumptions and non-claims are explicit.

## Contract Layers

| Layer | Function | Authority Boundary |
|---|---|---|
| External framework artifact | Declares, evidences, traces, reviews, or otherwise describes part of a governance path. | Does not grant StegVerse execution authority. |
| Translation mapping | Expresses relevant artifact fields as general governance primitives. | Does not alter the external framework's native meaning. |
| Commitment Candidate | Identifies the proposed actor, target, action, scope, context, and validity window. | Does not authorize execution. |
| SPE standing determination | Reconstructs current standing from policy, delegation, evidence, context, and recoverability state. | May return ALLOW, DENY, or FAIL-CLOSED. |
| Execution boundary | The point where consequence may bind. | Must follow the SPE result under the stated policy. |

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
Commitment Candidate -> proposed crossing
SPE -> current standing determination
Execution -> consequence binding
```

No layer should silently inherit authority from an earlier layer.

## Fail-Closed Triggers

SPE should return FAIL-CLOSED when current standing cannot be safely reconstructed.

Common triggers include:

- missing policy reference;
- expired or missing delegation;
- actor substitution;
- target substitution;
- scope mismatch;
- stale evidence;
- changed policy version;
- degraded recoverability;
- context mismatch;
- invalid or expired validity window;
- incomplete receipt chain;
- contradiction between supplied artifacts and current standing.

## External Framework Examples

| Framework | Native contribution | Commitment use |
|---|---|---|
| GLM | Declared claims, non-claims, scope, composition, and interpretation frame. | May inform policy, scope, and context references. |
| EVIDE | Post-event evidentiary deposit and reconstructability support. | May inform evidence and continuity references. |
| DecisionAssure | Trace integrity and causal-continuity package. | May inform evidence, chronology, drift, and causal-continuity references. |
| MindForge | Historical governance review evidence. | May inform review posture and evidence references, but not execution authority. |

## Non-Claims

```text
This contract does not certify external frameworks.
This contract does not require external frameworks to adopt StegVerse terminology internally.
This contract does not treat upstream artifacts as authorization.
This contract does not convert a review-time PASS into commit-time ALLOW.
This contract does not prove broad compatibility beyond the evaluated artifact package.
```

## Minimal Test Pattern

```text
Input: external artifact package
Map: artifact fields to governance primitives
Build: non-authorizing Commitment Candidate
Evaluate: SPE reconstructs current standing
Return: ALLOW / DENY / FAIL-CLOSED
Record: assumptions, non-claims, receipts, and replay path
```

## Core Principle

A system is not admissible merely because it can prevent failure.

A consequential transition is admissible only if execution authority remains reconstructable and valid at the moment consequence binds.
