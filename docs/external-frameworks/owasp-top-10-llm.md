---
title: OWASP Top 10 for LLM Applications External Framework Crosswalk
---

# OWASP Top 10 for LLM Applications External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: LLM application risk and vulnerability guidance
Wiki role: risk-control observatory, evidence comparison, and relationship review
Citation status: sourced
Evidence provenance status: Batch 3 refactor installed
```

## Source

Official source: `https://owasp.org/www-project-top-10-for-large-language-model-applications/`

The official source is treated as the canonical public source for OWASP Top 10 for LLM Applications framing.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Sources | Official OWASP project source URL. | present | Versioned source snapshot and source hash. |
| Official Implementation Sources | OWASP Top 10 for LLM Applications is treated here as external guidance rather than a runtime implementation. | not_applicable_or_external_guidance | Specific version/snapshot if used in a test. |
| Observed Behavior | No runtime behavior is claimed. | not_applicable_for_runtime_result | Not a runtime-result page. |
| Reproduced Behavior | No independent reproduction is claimed. | not_applicable | Reproduction only if a mapping fixture is created. |
| StegVerse Analysis | Risk categories, prompt injection, output handling, mitigations, and application security review are mapped to admissibility primitives. | risk_category_crosswalk | Concrete Commitment Candidate fixture with risk-category references. |
| Interoperability Assessment | OWASP risk evidence may support review posture, not authority. | pending_mapping_to_application_review_posture | Fixture and compatibility report. |
| Standing | Sourced provisional. | provisional | Source snapshot and mapping artifact. |

Evidence classification:

```text
F1: official OWASP project source URL and framework-native guidance claims.
S1: StegVerse interpretation of OWASP LLM risk categories as review-context evidence.
S2: mapping to Review Posture, Evidence Posture, Governance Boundary, Drift, Fail-Closed behavior, Commit-Time Validity, Receipt-Bound Execution, Policy Reference, Boundary Conditions, and Reconstructability.
H1: future mapping fixture until concrete risk-category references are attached.
```

## Definition

OWASP Top 10 for LLM Applications is treated in this wiki as an external LLM-application risk and vulnerability guidance framework.

It is not treated as an admissibility engine, execution-authority source, certification authority, or commit-time standing proof.

## Framework-Term Definitions

| Native OWASP Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| OWASP Top 10 for LLM Applications | External LLM-application risk and vulnerability guidance framework. | new | Preserved as framework-native terminology. |
| Top 10 risk category | Published risk or vulnerability category for LLM applications. | adjacent | Related to Review Posture and Evidence Posture. |
| Prompt injection | Attack class where model instructions or context are manipulated to alter behavior. | adjacent | Related to Governance Boundary, Drift, and Fail-Closed behavior. |
| Insecure output handling | Risk where model output is trusted or acted on without sufficient controls. | adjacent | Related to Commit-Time Validity and Receipt-Bound Execution. |
| Mitigation guidance | Recommended control or practice for reducing an identified LLM-application risk. | adjacent | Related to Policy Reference and Boundary Conditions. |
| LLM application security review | Review of application-level risks around an LLM system. | adjacent | Supports Review Posture but does not replace SPE standing determination. |

## Relationship To Admissibility

OWASP Top 10 for LLM Applications is listed as a crosswalk target for LLM-application risk, vulnerability, and mitigation context.

Admissibility review remains separate and asks whether a proposed transition may bind consequence at commit time.

In StegVerse terms, OWASP evidence may support a Commitment Candidate by identifying risk category, vulnerability class, mitigation expectation, and control gap context. Those records remain evidence. They do not become execution authority.

## Crosswalk Targets

| OWASP Candidate Function | Wiki / AE Relationship |
|---|---|
| Risk category classification | Review Posture; Evidence Posture |
| Prompt-injection analysis | Governance Boundary; Drift; Fail-Closed behavior |
| Output-handling review | Commit-Time Validity; Receipt-Bound Execution |
| Mitigation mapping | Policy Reference; Boundary Conditions |
| Application security review | Review Posture; Reconstructability |

## Three-Part Boundary

```text
OWASP asks: Which LLM-application risks or mitigations are relevant?
Admissibility asks: May this transition bind consequence at commit time?
EVIDE asks: What evidence remains after the event?
```

## Non-Claims

```text
OWASP Top 10 for LLM Applications is not a StegVerse canonical formalism.
OWASP Top 10 for LLM Applications does not prove transition admissibility.
OWASP Top 10 for LLM Applications does not grant execution authority inside StegVerse.
OWASP source citation is not acceptance of equivalence.
Security-risk review may support evidence and review posture, but review does not become authority.
```

## Challenge Path

A reader may challenge this reflection by identifying the claim, challenged field, reason, supporting evidence, and requested correction or standing change.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.

## Next Safe Build Target

Connect OWASP risk categories to the governance observatory protocol and test whether LLM-application risk evidence can be routed into a Commitment Candidate without granting execution authority to the risk record itself.
