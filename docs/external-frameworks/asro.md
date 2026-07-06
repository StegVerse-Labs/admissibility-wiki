---
title: ASRO External Framework Crosswalk
---

# ASRO External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: independent AI governance-state attestation
Wiki role: evidence-layer observatory, comparison, and relationship review
Citation status: sourced
Evidence provenance status: Batch 2 refactor installed
```

## Source

Public source: `https://aisystemsreliability.org/`

Public repository: `https://github.com/magicianzcardstockllc/asro`

The public source is treated as the canonical public source supplied for ASRO framing. The repository is treated as the public artifact source for the ASRO v1.0 release-candidate materials described by the source site.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Sources | Public ASRO source URL. | present | Versioned source snapshot and source hash. |
| Official Implementation Sources | Public ASRO repository URL. | present_repository_reference | Specific release, commit hash, and artifact package snapshot. |
| Observed Behavior | Commitment Candidate fixture is referenced; no reproduced runtime/attestation run is claimed here. | commitment_candidate_material_present_or_pending | Raw attestation output, verifier payload, timestamp, source version, and hash. |
| Reproduced Behavior | No independent reproduction is claimed. | not_started | Reproduction fixture and deterministic ASRO verification run. |
| StegVerse Analysis | Host-side measurement, edge-side witnessing, verifier reconciliation, governance-state changes, and selective attestation are mapped to admissibility primitives. | governance_state_attestation_crosswalk | SPE review over concrete attestation artifacts. |
| Interoperability Assessment | ASRO evidence may support a Commitment Candidate without becoming execution authority. | pending_or_partial_commitment_candidate | Completed fixture validation report and compatibility report. |
| Standing | Sourced provisional. | provisional | Release/commit hash and validation artifact package. |

Evidence classification:

```text
F1: ASRO public source URL and framework-native public framing.
F2: ASRO public repository reference.
V1: ASRO non-authorizing Commitment Candidate fixture reference.
S1: StegVerse interpretation of ASRO as governance-state attestation evidence.
S2: mapping to Evidence Posture, Policy Reference, Governance Boundary, Reconstructability, Receipt-Bound Execution, Review Posture, Drift, Commit-Time Validity, and FAIL-CLOSED behavior.
I1: pending until the ASRO artifact is routed through a validated Commitment Candidate/SPE fixture.
```

## Definition

ASRO, the AI Systems Reliability Operator, is treated in this wiki as an external evidence and attestation framework for independently witnessing whether an AI system remained within its declared governance state over time.

ASRO is not treated as an admissibility engine, safety certification, legal-compliance guarantor, or output-quality evaluator.

## Framework-Term Definitions

| Native ASRO Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| ASRO | Independent attestation layer for AI governance-state continuity. | new | Preserved as framework-native terminology. |
| Host Meter Agent | Operator-side measurement component that observes governance-state declarations and changes. | adjacent | Related to Evidence Posture and Receipt-Bound Execution. |
| Edge Meter Agent | User-side or dependent-party witnessing component for governance-state attestation. | adjacent | Related to external witness evidence and reconstructability. |
| ASRO Verifier | Independent reconciliation component comparing host-side measurement and edge-side witnessing. | adjacent | Related to independent authority reconstruction evidence, but not execution authority itself. |
| Governance state | The declared policies, tools, constraints, configuration, or rules under which the AI system claims to operate. | adjacent | Related to Policy Reference, Governance Boundary, and Commit-Time Validity. |
| Selective attestation | Failure mode where a system attests enough to preserve plausible compliance while hiding governance-relevant change. | adjacent | Related to drift, evidence incompleteness, and FAIL-CLOSED review posture. |

## Relationship To Admissibility

ASRO is listed as a crosswalk target for governance-state attestation and independent witnessing.

Admissibility review remains separate and asks whether a proposed transition may bind consequence at commit time.

In StegVerse terms, ASRO evidence may support a Commitment Candidate by supplying independently witnessed governance-state records. Those records remain evidence. They do not become execution authority.

## Crosswalk Targets

| ASRO Candidate Function | Wiki / AE Relationship |
|---|---|
| Host-side governance-state measurement | Evidence Posture; Policy Reference; Governance Boundary |
| Edge-side witnessing | Reconstructability; Receipt-Bound Execution |
| Independent verifier reconciliation | Review Posture; independent authority reconstruction evidence |
| Governance-state change record | Drift; Commit-Time Validity; Receipt-Bound Execution |
| Selective-attestation threat model | FAIL-CLOSED behavior; evidence sufficiency review |

## Commitment Candidate Fixture

ASRO is now connected to a non-authorizing Commitment Candidate fixture:

```text
docs/external-frameworks/asro-commitment-candidate.json
```

The fixture records how an ASRO governance-state attestation artifact may be routed into StegVerse review without converting the attestation into execution authority.

The fixture's default posture is `FAIL-CLOSED` unless current policy, delegation, evidence, context, and recoverability are independently reconstructed at the commit boundary.

## Three-Part Boundary

```text
ASRO asks: Was the system operating under the governance state it claimed?
Admissibility asks: May this transition bind consequence at commit time?
EVIDE asks: What evidence remains after the event?
```

## Non-Claims

```text
ASRO is not a StegVerse canonical formalism.
ASRO does not prove transition admissibility.
ASRO does not grant execution authority inside StegVerse.
ASRO source citation is not acceptance of equivalence.
ASRO attestation evidence may support review, but review does not become authority.
```

## Challenge Path

A reader may challenge this reflection by identifying the claim, challenged field, reason, supporting evidence, and requested correction or standing change.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.

## Next Safe Build Target

Build a validation guard for ASRO's commitment-candidate fixture so the registry, manifest, page, and non-authorizing authority boundary remain synchronized.
