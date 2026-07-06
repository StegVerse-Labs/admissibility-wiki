---
title: External Framework Failure Class Catalog
---

# External Framework Failure Class Catalog

## Purpose

This catalog defines reusable failure classes for external-framework evaluation.

A failure class describes the kind of governance weakness or divergence observed. It is not a verdict about the entire framework.

## Classification Rule

Use the least broad class that accurately describes the observed behavior.

If the observation lacks test parameters, raw outputs, timestamps, or source version, mark the observation as partial and do not generalize beyond the captured case.

## Canonical Failure Classes

| ID | Name | Definition | Typical Signal | StegVerse Relationship |
|---|---|---|---|---|
| FC-001 | Semantic Equivalence Divergence | Equivalent or higher-risk consequence-bearing transitions receive different governance outcomes because they are expressed with different labels, wrappers, or tool paths. | `transfer_funds` blocks while `move_value` allows comparable value movement. | Commit-Time Validity; Consequence-Binding Transition Review. |
| FC-002 | Authority Drift | Authority changes, expires, or mutates without a corresponding standing update. | Previously authorized action remains allowed after authority changes. | Commit-Time Authority; Drift. |
| FC-003 | Stale Evidence | A decision depends on evidence outside its validity window. | Old receipt, old approval, or stale policy remains sufficient. | Evidence Posture; Commit-Time Validity. |
| FC-004 | Delegation Leakage | Delegated authority exceeds its granted scope, target, actor, amount, or duration. | Delegate can act outside assigned policy boundary. | Authority Class; Delegation Reference. |
| FC-005 | Replay Divergence | Replay of the same governed artifact produces a different outcome without recorded context change. | Same transition replays ALLOW then DENY, or vice versa. | Replayability; Reconstructability. |
| FC-006 | Recoverability Loss | The transition cannot be independently reconstructed after the fact. | Missing trace, missing receipt, missing policy source, or incomplete artifact chain. | Recoverability; Receipt-Bound Execution. |
| FC-007 | Fail-Open Runtime Error | Runtime evaluator errors, times out, or becomes unavailable while execution remains possible. | ERROR produces execution permission or no blocking posture. | Fail-Closed; Governance Boundary. |
| FC-008 | Source-Claim Mismatch | Public claims, implementation behavior, and observed behavior diverge. | Website claims broad blocking; demo or repo behavior is narrower. | Evidence Provenance; Comparative Fairness. |
| FC-009 | Non-Claim Boundary Collapse | An analysis page, report, or result implies certification, endorsement, or authority not supported by evidence. | Compatibility page reads as validation or endorsement. | Non-Claims; Standing Boundary. |
| FC-010 | Policy Granularity Gap | Policy checks are too coarse to distinguish material risk differences. | High-value external movement and low-value internal movement receive the same posture. | Policy Reference; Consequence Review. |
| FC-011 | Actor Ambiguity | The evaluated actor, user, system, delegate, or authority source is unclear or conflated. | `self`, customer ID, service account, and delegate are not distinguished. | Identity; Authority Class. |
| FC-012 | Evidence Class Confusion | Framework claims, implementation evidence, observed behavior, and StegVerse analysis are presented as the same kind of evidence. | A website claim is treated as an observed result. | Evidence Provenance; Claim Traceability. |

## Required Failure Record Fields

A failure record should include:

```text
failure_class_id
framework
source_or_test_id
input_sequence_or_artifact
observed_result
expected_boundary
missing_artifacts
claim_strength
StegVerse interpretation
next_required_action
```

## Claim Strength Levels

| Level | Meaning |
|---|---|
| Internal Note | Conversation memory or incomplete observation only. |
| Partial Observation | Some parameters recorded, but raw output or source version missing. |
| Public Observation Candidate | Parameters, output, source version, and timestamp present. |
| Reproduced Failure | Independently reproduced from attached parameters. |
| Interoperability Finding | Routed through StegVerse Commitment Candidate or SPE path. |

## Non-Claims

```text
A failure class does not certify that an external framework is unsafe.
A failure class does not prove general incompatibility.
A failure class does not replace framework-native context.
A failure class does not create StegVerse execution authority.
```

## Mandatory Footer

Failure classes are evidence labels. They help preserve and compare observed behavior without overstating standing. Publication of a failure class does not establish final authority, certification, or global validation.
