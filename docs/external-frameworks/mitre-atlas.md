---
title: MITRE ATLAS External Framework Crosswalk
---

# MITRE ATLAS External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: adversarial AI threat knowledge base
Wiki role: threat-model observatory, evidence comparison, and relationship review
Citation status: sourced
```

## Source

Official source: `https://atlas.mitre.org/`

The official source is treated as the canonical public source for MITRE ATLAS framing.

## Definition

MITRE ATLAS is treated in this wiki as an external adversarial AI threat-knowledge framework for describing tactics, techniques, mitigations, case studies, and threat-informed AI system risk review.

MITRE ATLAS is not treated as an admissibility engine, execution-authority source, certification authority, or commit-time standing proof.

## Framework-Term Definitions

| Native MITRE ATLAS Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| MITRE ATLAS | External adversarial AI threat-knowledge framework. | new | Preserved as framework-native terminology. |
| Tactic | High-level adversarial objective or phase. | adjacent | Related to threat posture and review context, not execution authority. |
| Technique | Specific adversarial behavior or method. | adjacent | Related to Evidence Posture, Drift, and Review Posture. |
| Mitigation | Control or action intended to reduce a threat or technique. | adjacent | Related to Policy Reference and Governance Boundary. |
| Case study | Documented example of adversarial AI behavior or incident pattern. | adjacent | Related to Reconstructability and evidence comparison. |
| Threat-informed review | Review using known tactics, techniques, and mitigations as context. | adjacent | Supports Review Posture but does not replace SPE standing determination. |

## Relationship To Admissibility

MITRE ATLAS is listed as a crosswalk target for adversarial AI threat context.

Admissibility review remains separate and asks whether a proposed transition may bind consequence at commit time.

In StegVerse terms, MITRE ATLAS evidence may support a Commitment Candidate by identifying threat context, relevant technique classes, and mitigation expectations. Those records remain evidence. They do not become execution authority.

## Crosswalk Targets

| MITRE ATLAS Candidate Function | Wiki / AE Relationship |
|---|---|
| Tactic classification | Review Posture; Governance Boundary |
| Technique classification | Evidence Posture; Drift; Commit-Time Validity |
| Mitigation mapping | Policy Reference; Boundary Conditions |
| Case-study reference | Reconstructability; Evidence Posture |
| Threat-informed review | Review Posture; Fail-Closed behavior |

## Three-Part Boundary

```text
MITRE ATLAS asks: Which adversarial AI tactics, techniques, mitigations, or case studies are relevant?
Admissibility asks: May this transition bind consequence at commit time?
EVIDE asks: What evidence remains after the event?
```

## Non-Claims

```text
MITRE ATLAS is not a StegVerse canonical formalism.
MITRE ATLAS does not prove transition admissibility.
MITRE ATLAS does not grant execution authority inside StegVerse.
MITRE ATLAS source citation is not acceptance of equivalence.
Threat-informed review may support evidence and review posture, but review does not become authority.
```

## Next Safe Build Target

Connect MITRE ATLAS tactics and techniques to the governance observatory protocol and test whether threat-context evidence can be routed into a Commitment Candidate without granting execution authority to the threat record itself.
