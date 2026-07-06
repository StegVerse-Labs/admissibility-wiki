---
title: External Framework Page Template
---

# External Framework Page Template

Use this template when creating or refactoring an external-framework page.

The governing standard is [External Framework Evaluation Standard](./evaluation-standard.md).

## Status

```text
Relationship type: external framework intake | crosswalk | cooperative validation target
Canonical StegVerse formalism source: Admissible-Existence
External framework role: <role>
Wiki role: sourced observatory record, compatibility map, and bounded validation path
Citation status: intake | sourced | artifact package required | public source required
Validation posture: provisional | cooperative | reproduced | public-ready
Runtime-result posture: no public result claim unless parameters and outputs are attached
```

## Source

### Official Framework Sources

| Evidence Code | Source | URL / Reference | Notes |
|---|---|---|---|
| F1 | Official website |  |  |
| F1 | Official docs or paper |  |  |
| F2 | Official repository or implementation |  |  |
| F2 | Release, package, or commit |  |  |

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Sources |  | missing / partial / present |  |
| Official Implementation Sources |  | missing / partial / present |  |
| Observed Behavior |  | missing / partial / present |  |
| Reproduced Behavior |  | missing / partial / present |  |
| StegVerse Analysis |  | missing / partial / present |  |
| Interoperability Assessment |  | missing / partial / present |  |
| Standing |  | provisional / reconstructable / reproduced / public-ready |  |

## Definition

Describe the framework in framework-native terms first.

Then describe the limited relationship to Admissibility without claiming equivalence.

## Framework-Term Definitions

| Native Framework Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
|  |  | synonymous / adjacent / new / unresolved |  |

## Relationship To Admissibility

```text
<Framework> asks: <native framework question>
StegVerse Admissibility asks: May this transition bind consequence at commit time?
```

## Execution Authority Boundary

```text
No <Framework> artifact, output, recommendation, trace, proof, runtime result, or evaluation constitutes execution authority inside StegVerse.
```

## Observed Behavior or Observation Boundary

Use one of these patterns.

### No Public Observation Yet

```text
Status: no public runtime-result claim
Prompt-by-prompt parameters attached: no
Runtime configuration attached: no
Screenshots or returned audit payloads attached: no
Timestamps and source hashes attached: no
External reproducibility: not established
```

### Parameterized Observation

```text
Input sequence:
<sequence>

Observed framework result:
<result>

Missing artifacts:
<missing fields>
```

## Parameterized Test Cases

| Case ID | Input / Artifact | Observed Result | Expected Boundary | Evidence Class | Missing Fields |
|---|---|---|---|---|---|
|  |  |  |  | O1 / O2 / R1 |  |

## StegVerse Analysis

| Criterion | StegVerse Question | Result / Status |
|---|---|---|
| Identity | Is the actor known and current? |  |
| Authority | Is authority current at commit time? |  |
| Policy | Is the policy source current and scoped? |  |
| Delegation | Is delegation current and bounded? |  |
| Evidence | Is evidence available, current, and reconstructable? |  |
| Standing | Can standing be reconstructed? |  |
| Recoverability | Can the transition be recovered or reviewed? |  |
| Replayability | Can the transition be replayed deterministically? |  |
| Reconstructability | Can the evidence chain be independently reconstructed? |  |
| Commit-Time Validity | Is the boundary valid now? |  |
| Failure Behavior | Does the framework fail closed? |  |
| Interoperability | Can output route into Commitment Candidate or SPE? |  |
| Governed Return Path | Can result return with receipt-bound semantics? |  |

## Interoperability Assessment

```text
External artifact
-> Commitment Candidate
-> SPE current-standing reconstruction
-> ALLOW / DENY / FAIL-CLOSED
-> governed return path
```

## Commit-Time Interoperability Contract

Minimum fields:

```text
transition_id
actor
requested_action
target_system
scope
framework_verdict_or_artifact
framework_rule_or_layer
framework_audit_reference
policy_reference
delegation_reference
evidence_references
execution_context
validity_window
recoverability_profile
source_timestamp
source_hash_or_receipt
```

## Failure Classes

| Failure Class | Applies? | Evidence | Notes |
|---|---|---|---|
| FC-001 Semantic Equivalence Divergence | yes / no / unknown |  |  |
| FC-002 Authority Drift | yes / no / unknown |  |  |
| FC-003 Stale Evidence | yes / no / unknown |  |  |
| FC-004 Delegation Leakage | yes / no / unknown |  |  |
| FC-005 Replay Divergence | yes / no / unknown |  |  |
| FC-006 Recoverability Loss | yes / no / unknown |  |  |
| FC-007 Fail-Open Runtime Error | yes / no / unknown |  |  |
| FC-008 Source-Claim Mismatch | yes / no / unknown |  |  |
| FC-009 Non-Claim Boundary Collapse | yes / no / unknown |  |  |
| FC-010 Policy Granularity Gap | yes / no / unknown |  |  |
| FC-011 Actor Ambiguity | yes / no / unknown |  |  |
| FC-012 Evidence Class Confusion | yes / no / unknown |  |  |

## Evaluation Result Posting

Generated or fixture-bound results must be posted from:

```text
docs/external-frameworks/reports/<framework-id>.compatibility.json
```

Manual claims on this page must not outrun the report.

## Crosswalk Targets

| Framework Function | Wiki / AE Relationship |
|---|---|
|  |  |

## AE Reflection Metadata

```text
Claim ID: CLM-FWK-<ID>-0001
Packet ID: ARF-FWK-<ID>-0001
Evidence grade: <grade>
Admissibility result: PROVISIONAL
Standing: PROVISIONAL
Reflection status: <status>
Source artifacts: <count and type>
Last evaluation: <timestamp>
```

## Validation Completion Criteria

```text
public source URLs remain available
compatibility report parses
observed tests are reconstructed with full parameters or excluded from public result claims
parameterized boundary cases include raw output, timestamp, source version, and audit payload
cooperative validation suite is run against captured inputs
runtime outputs are routed into Commitment Candidate fixtures
SPE results are generated from those fixtures
non-claim language is preserved
```

## Non-Claims

```text
<Framework> is not a StegVerse canonical formalism.
<Framework> does not prove transition admissibility.
<Framework> does not grant execution authority.
This page does not certify <Framework>.
This page does not claim general compatibility.
This page does not claim live integration, production activation, or customer deployment.
Observed behavior alone does not establish admissibility.
```

## Challenge Path

A reader may challenge this reflection by identifying the claim, challenged field, reason, supporting evidence, and requested correction or standing change.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.

## Next Safe Build Target

Identify the next evidence artifact, compatibility report update, or reconstruction step required before the page can advance standing.
