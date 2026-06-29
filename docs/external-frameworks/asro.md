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
```

## Source

Public source: `https://aisystemsreliability.org/`

Public repository: `https://github.com/magicianzcardstockllc/asro`

The public source is treated as the canonical public source supplied for ASRO framing. The repository is treated as the public artifact source for the ASRO v1.0 release-candidate materials described by the source site.

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

## Next Safe Build Target

Connect ASRO to the governance observatory protocol and test whether ASRO-style governance-state attestation can be routed into a Commitment Candidate without granting execution authority to the attestation record itself.
