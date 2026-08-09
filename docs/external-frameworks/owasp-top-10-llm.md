---
title: OWASP Top 10 for LLM Applications External Framework Crosswalk
---

# OWASP Top 10 for LLM Applications External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: LLM/GenAI application risk and vulnerability guidance
Current evaluated resource: OWASP Top 10 for LLM Applications 2025
Current broader project: OWASP GenAI Security Project
Evidence posture: VERSIONED_PUBLIC_GUIDANCE + BOUNDED_STEGVERSE_CROSSWALK
Runtime posture: NOT_APPLICABLE_AS_AUTHORITY_ENGINE
Standing: no standing created
Execution authority: none
```

## Official Source And Version

This evaluation is pinned to the **OWASP Top 10 for LLM Applications 2025** resource and records the OWASP GenAI Security Project as the current broader project context.

```text
2025 resource: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
current project: https://genai.owasp.org/
project evolution: https://genai.owasp.org/2025/03/26/project-owasp-promotes-genai-security-project-to-flagship-status/
evaluated list: 2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps
```

The evaluated LLM/GenAI Top 10 remains distinct from the later OWASP Top 10 for Agentic Applications. Project evolution does not silently change the identity of the evidence used by this crosswalk.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Sources | Versioned OWASP Top 10 for LLM Applications 2025 resource plus current OWASP GenAI Security Project context. | present_versioned_public_guidance | No source-identity gap for the bounded 2025-list crosswalk. |
| Official Implementation Sources | OWASP Top 10 is security guidance rather than an authorization runtime implementation. | not_applicable_external_guidance | A target application's implementation evidence must be evaluated separately. |
| Observed Behavior | No native OWASP runtime authorization or consequence-binding behavior is claimed. | not_applicable_for_runtime_result | Runtime behavior is not a property of the guidance document itself. |
| Reproduced Behavior | No independent runtime reproduction is claimed. | not_applicable_for_runtime_result | Target-specific security testing would be a separate evidence packet. |
| StegVerse Analysis | Risk categories and mitigations are mapped to Evidence Posture, Review Posture, Governance Boundary, Drift, Policy Reference, Receipt-Bound Execution, and Fail-Closed behavior. | risk_category_crosswalk | Canonical merged-state validation remains the local gate. |
| Interoperability Assessment | Six StegVerse case families test whether risk evidence can influence review without becoming identity, delegation, standing, or authority. | bounded_crosswalk_pending_merged_validation | No OWASP certification or endorsement is claimed. |
| Standing | Security guidance and this page create no standing. | none_created | Standing must be independently reconstructed at the governed transition. |

Evidence classification:

```text
F1: official OWASP Top 10 for LLM Applications 2025 resource and current OWASP GenAI Security Project context.
S1: StegVerse interpretation of OWASP LLM/GenAI risk categories and mitigations as security-review evidence rather than authority.
S2: six-family StegVerse mapping to Evidence Posture, Review Posture, Governance Boundary, Drift, Policy Reference, Receipt-Bound Execution, and Fail-Closed behavior.
H1: any claim that OWASP guidance itself proves target security, grants standing, establishes delegation, certifies StegVerse, or authorizes consequence remains prohibited unless separately evidenced.
```

## Framework-Term Definitions

| Native OWASP Term | Definition For This Wiki | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| OWASP Top 10 for LLM Applications | Versioned external LLM/GenAI application risk and vulnerability guidance; this evaluation is pinned to the 2025 list. | new | Preserved as framework-native security terminology; not an admissibility engine. |
| Top 10 risk category | Published class of LLM/GenAI application security risk. | adjacent | Supports Review Posture and Evidence Posture. |
| Prompt injection | Attack class in which instructions or context are manipulated to influence model/application behavior. | adjacent | Related to Governance Boundary, Drift, scope integrity, and Fail-Closed behavior. |
| Insecure output handling | Risk arising when model output is insufficiently validated or constrained before downstream use. | adjacent | Related to Commit-Time Validity and Receipt-Bound Execution. |
| Mitigation guidance | Recommended practice or control intended to reduce an identified risk. | adjacent | May inform Policy Reference and Boundary Conditions; recommendation is not proof of implementation or effectiveness. |
| LLM application security review | Review of security risks and mitigations around an LLM/GenAI application. | adjacent | Supports Review Posture and Reconstructability; review does not become authority. |
| OWASP GenAI Security Project | Current broader OWASP project context containing multiple GenAI security resources. | new | Context for source lineage; broader project scope must not silently alter the evaluated resource identity. |
| Agentic Applications Top 10 | Separate OWASP resource addressing agentic-system risks. | distinct | Must not be conflated with the evaluated 2025 LLM/GenAI Top 10 evidence packet. |

## What The Framework Claims And Demonstrates

The 2025 OWASP Top 10 provides security-risk categories, vulnerability descriptions, and mitigations for LLM and generative-AI applications. The broader GenAI Security Project publishes additional security resources, but this evaluation does not treat those resources as one undifferentiated authority source.

OWASP risk guidance can identify security-relevant conditions. It does **not** establish actor identity, delegation, StegVerse standing, commit-time admissibility, or authority to bind consequence.

## StegVerse Evidence Installed

The repository contains a bounded six-family governance compatibility contract for this framework. The fixture is StegVerse-authored crosswalk machinery and does not imply that OWASP executed or endorsed StegVerse tests.

```text
manifest: docs/external-frameworks/owasp-top-10-llm.json
governance fixture: tests/fixtures/external-frameworks/owasp-top-10-llm-governance-compatibility-cases.v1.json
case families: 6
simulation_only: true
canonical validation path: .github/workflows/validate-chain-continuation.yml
```

The six bounded test families cover:

| Family | StegVerse Boundary Tested |
|---|---|
| positive alignment | Risk context may support ALLOW only if independent authority, policy, scope, freshness, and mitigation predicates are satisfied. |
| framework denial / negative result | A blocking security condition maps to DENY within the evaluated scope. |
| authority / delegation failure | Security guidance cannot restore absent or expired authority. |
| stale / missing evidence | Stale or incomplete risk evidence fails closed. |
| malformed / undefined result | Undefined mapping or malformed evidence fails closed. |
| semantic divergence guard | Evidence or mitigation for one application scope cannot authorize another scope. |

The canonical governance-compatibility validator has observed all six `owasp-top-10-llm` case families as repository tests. That proves execution of the StegVerse mapping contract, not runtime execution of OWASP guidance.

## Governance-Chain Placement

OWASP Top 10 evidence belongs upstream of commitment:

```text
versioned OWASP risk / vulnerability / mitigation reference
  -> Evidence Posture + Review Posture + Governance Boundary context
  -> candidate policy / mitigation expectations
  -> independent standing + delegation + scope + freshness reconstruction
  -> commit-time admissibility decision
  -> consequence binding only when separately authorized
```

A risk classification can strengthen or weaken the evidence available to an admissibility gate. It does not become execution authority merely because it is security-relevant.

## Claims Versus Demonstrated Abilities

| Question | Current Evidence |
|---|---|
| Is a specific OWASP resource identified? | Yes: Top 10 for LLM Applications 2025. |
| Is current broader project context recorded? | Yes: OWASP GenAI Security Project. |
| Is the Agentic Top 10 kept distinct? | Yes. |
| Are risk and mitigation concepts mappable into review evidence? | Yes. |
| Has StegVerse installed a six-family mapping contract? | Yes. |
| Has the canonical validator exercised those six families? | Yes, as StegVerse tests. |
| Does this prove a production application is secure? | No. |
| Does OWASP guidance establish actor standing or delegation? | No. |
| Is certification or OWASP endorsement claimed? | No. |
| Is execution authority granted? | No. |

## Non-Capabilities And Non-Claims

```text
OWASP Top 10 for LLM Applications is not a StegVerse canonical formalism.
OWASP guidance does not prove transition admissibility.
A risk category does not establish actor identity or delegation.
A mitigation recommendation does not prove that a mitigation is implemented or effective in a specific target.
Security review does not become execution authority.
The StegVerse compatibility fixture is simulation/crosswalk evidence, not OWASP certification or endorsement.
Publication creates no standing.
```

## Current Completion Gate

The versioned source identity, current project context, six-family mapping contract, governance-chain placement, terminology reconciliation, evidence-provenance contract, and non-authority boundaries are installed. The remaining local gate is canonical validation of the merged page/manifest state. If the OWASP-specific manifest, terminology, page, provenance, benchmark, and governance-compatibility checks pass, this evaluation can reach `LOCAL_WORK_COMPLETE_BOUNDED_SECURITY_CROSSWALK` without inventing runtime or certification evidence.

## Challenge Path

A reader may challenge the evaluated resource, version, risk mapping, mitigation interpretation, scope, failure posture, or authority boundary by supplying inspectable evidence for correction.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing that can be reconstructed from the referenced evidence, authority, and admissibility conditions.
