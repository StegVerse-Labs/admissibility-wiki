---
title: Evidence Provenance Rollout
---

# Evidence Provenance Rollout

## Purpose

This page begins the same evaluation process across all registered external frameworks.

It applies the [External Framework Evaluation Standard](./evaluation-standard.md) to every framework in the registry and records the first-pass evidence posture for each page.

The machine-readable rollout matrix is:

```text
docs/external-frameworks/evidence-provenance-rollout.json
```

## Evaluation Classes

```text
F1 Framework Claim
F2 Framework Implementation
O1 Direct Observation
O2 Parameterized Observation
R1 Reproduced Result
S1 StegVerse Analysis
S2 Transition Mapping
I1 Interoperability Result
V1 Validation Artifact
H1 Hypothesis
```

## First-Pass Rollout Matrix

| Framework | Source Status | Observed Behavior | StegVerse Analysis | Standing | Next Action |
|---|---|---|---|---|---|
| GLM | sourced | not started | provisional crosswalk | sourced provisional | Add Evidence Provenance and classify claims as F1/S1/S2. |
| EVIDE | sourced | not started | provisional crosswalk | sourced provisional | Add Evidence Provenance and classify reconstructability claims. |
| DecisionAssure | artifact package required | artifact dependent | partial trace crosswalk | fail-closed pending artifact | Separate artifact-package claims from StegVerse trace analysis. |
| MindForge | artifact package required | artifact dependent | partial review-evidence crosswalk | fail-closed pending artifact | Separate historical review evidence from execution authority. |
| Morrison Runtime | sourced with parameterized boundary case partial | O2 partial | semantic-equivalence boundary case | bounded partial observation | Attach raw audit payload, timestamp, runtime configuration, and source hash. |
| CARE Runtime | official source required | not started | intake only | source-blocked fail-closed | Identify official source before any compatibility claim. |
| AAR | sourced | not started | provisional crosswalk | sourced provisional | Add source/analysis split. |
| ASRO | sourced | commitment candidate material present or pending | governance-state attestation crosswalk | sourced provisional | Classify ASRO commitment candidate artifacts as V1/I1 where present. |
| MITRE ATLAS | sourced | not applicable for runtime result | threat-context crosswalk | sourced provisional | Map threat knowledgebase evidence without runtime claims. |
| OWASP Top 10 for LLM Applications | sourced | not applicable for runtime result | risk-category crosswalk | sourced provisional | Map risk categories without certification claims. |
| Agent Governance Playbook | sourced | not started | agent-continuation crosswalk | sourced provisional | Classify release/source evidence and continuation-governance analysis. |
| Emergency Stop Convention | sourced | not started | emergency-stop fail-closed crosswalk | sourced provisional | Map emergency-stop semantics to fail-closed boundary classes. |
| NIST AI RMF | sourced | not applicable for runtime result | risk-management crosswalk | sourced provisional | Separate NIST source claims from StegVerse analysis. |
| ISO/IEC 42001 | sourced | not applicable for runtime result | AI management-system crosswalk | sourced provisional | Classify standard-source claims and StegVerse controls separately. |
| EU AI Act | sourced | not applicable for runtime result | legal-obligation crosswalk | sourced provisional | Separate legal-source summary from StegVerse governance analysis. |
| Policy Cards | sourced | not started | runtime policy artifact crosswalk | sourced provisional | Build policy-card Commitment Candidate fixture. |
| Runtime Governance for AI Agents | sourced | not started | runtime path-governance crosswalk | sourced provisional | Compare path-governance claims to semantic-equivalence boundary testing. |
| Admissible Existence Seed Cycle | first framework cycle complete | seed-cycle artifacts present | canonical seed-cycle mirror | cycle complete, non-authorizing | Preserve as mirror record; do not treat publication as standing. |

## Rollout Rule

Each framework page should be refactored to include the same Evidence Provenance structure before stronger interoperability claims are made.

```text
Official Framework Sources
Official Implementation Sources
Observed Behavior
Reproduced Behavior
StegVerse Analysis
Interoperability Assessment
Standing
```

## Boundary

```text
This rollout is not certification.
This rollout is not endorsement.
This rollout does not grant execution authority.
This rollout does not convert source availability into validation.
This rollout does not generalize observed behavior beyond captured evidence.
```

## Next Safe Build Target

Refactor pages in batches:

```text
Batch 1: GLM, EVIDE, Morrison Runtime
Batch 2: DecisionAssure, MindForge, ASRO
Batch 3: MITRE ATLAS, OWASP Top 10 for LLM Applications, NIST AI RMF, ISO/IEC 42001, EU AI Act
Batch 4: Policy Cards, Runtime Governance for AI Agents, Agent Governance Playbook, Emergency Stop Convention, CARE Runtime, AAR
Batch 5: Admissible Existence Seed Cycle
```
