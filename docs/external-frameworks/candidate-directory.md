---
title: External Framework Candidate Directory
---

# External Framework Candidate Directory

## Purpose

This directory makes the full external-framework observatory scope visible.

The main External Frameworks index contains registered pages, crosswalks, mappings, fixtures, and internal mirror records. This directory contains the additional source-required candidates that are already documented in the expanded intake registry but do not yet have full framework pages.

```text
registered page != intake candidate
intake candidate != sourced framework
source required != rejected
candidate visibility != validation
candidate directory != execution authority
```

## Current Coverage

```text
registered framework and crosswalk entries: 19
additional source-required candidates: 42
total visible observatory entries: 61
intake classes represented: 10
```

The total is a discovery and work-planning count. It is not a framework ranking, compatibility score, certification count, or validation claim.

## Policy As Code

| Candidate | Status | Intended Intake Role |
|---|---|---|
| Open Policy Agent | source_required | Policy-as-code and authorization decision point candidate. |
| Cedar Policy | source_required | Authorization policy language candidate. |
| Rego | source_required | Policy language candidate for rule mapping. |

## Identity And Authority

| Candidate | Status | Intended Intake Role |
|---|---|---|
| SPIFFE/SPIRE | source_required | Workload identity and trust-domain candidate. |
| OpenID Connect | source_required | Identity assertion and authentication-context candidate. |
| OAuth 2.0 | source_required | Delegated authorization candidate. |
| W3C Decentralized Identifiers | source_required | Decentralized identity candidate. |
| W3C Verifiable Credentials | source_required | Credential proof and claim-evidence candidate. |

## Provenance And Trace

| Candidate | Status | Intended Intake Role |
|---|---|---|
| in-toto | source_required | Supply-chain provenance and layout-verification candidate. |
| SLSA | source_required | Software supply-chain assurance candidate. |
| Sigstore | source_required | Artifact signing and transparency-log candidate. |
| OpenLineage | source_required | Data-lineage and reconstruction candidate. |
| W3C PROV | source_required | Provenance-model candidate. |

## Risk And Assurance

| Candidate | Status | Intended Intake Role |
|---|---|---|
| NIST Cybersecurity Framework | source_required | Cybersecurity risk-management candidate. |
| NIST SP 800-53 | source_required | Security and privacy controls candidate. |
| NIST SP 800-207 Zero Trust Architecture | source_required | Zero-trust architecture candidate. |
| SOC 2 | source_required | Assurance and control-reporting candidate. |
| Cloud Security Alliance CCM | source_required | Cloud control-matrix candidate. |
| NIST Secure Software Development Framework | source_required | Secure-development lifecycle candidate. |
| OSCAL | source_required | Machine-readable control and assessment candidate. |
| AI Verify | source_required | AI testing and governance toolkit candidate. |

## Threat And Security

| Candidate | Status | Intended Intake Role |
|---|---|---|
| STRIDE | source_required | Threat-modeling candidate. |
| MITRE ATT&CK | source_required | Adversarial-technique knowledge candidate. |
| MITRE D3FEND | source_required | Defensive-technique knowledge candidate. |

## Privacy And Data Governance

| Candidate | Status | Intended Intake Role |
|---|---|---|
| GDPR | source_required | Privacy and consent-governance candidate. |
| NIST Privacy Framework | source_required | Privacy risk-management candidate. |
| ISO/IEC 27701 | source_required | Privacy information-management candidate. |

## Model Evaluation And Monitoring

| Candidate | Status | Intended Intake Role |
|---|---|---|
| Model Cards | source_required | Model documentation and intended-use candidate. |
| Datasheets for Datasets | source_required | Dataset documentation and provenance candidate. |
| MLCommons AI Safety | source_required | AI safety-evaluation candidate. |
| HELM | source_required | Model-evaluation benchmark candidate. |
| garak | source_required | LLM vulnerability-scanning candidate. |
| promptfoo | source_required | LLM evaluation and regression-testing candidate. |

## Runtime Governance

| Candidate | Status | Intended Intake Role |
|---|---|---|
| Guardrails AI | source_required | LLM output-validation and guardrail candidate. |
| Llama Guard | source_required | LLM safety-classifier candidate. |
| NeMo Guardrails | source_required | LLM guardrail and conversation-control candidate. |

## Agent Protocols

| Candidate | Status | Intended Intake Role |
|---|---|---|
| Agent2Agent Protocol | source_required | Agent-interoperability protocol candidate. |
| Model Context Protocol | source_required | Tool and context protocol candidate. |
| OpenAPI | source_required | Tool-contract and API-description candidate. |

## Regulatory And Standards

| Candidate | Status | Intended Intake Role |
|---|---|---|
| OECD AI Principles | source_required | International AI-governance principle candidate. |
| UNESCO Recommendation on AI Ethics | source_required | International AI-ethics framework candidate. |
| NIST AI RMF Generative AI Profile | source_required | Generative-AI risk-profile candidate. |

## Promotion Path

Each candidate remains in `source_required` until the existing promotion gates are satisfied:

```text
canonical source
source version or publication date
published scope
published non-claims or bounded StegVerse non-claims
artifact type
relationship class
benchmark relevance
authority boundary
evidence posture
```

After those gates, a candidate may move through:

```text
source_required
-> sourced_intake
-> page_candidate
-> mapping_candidate
-> fixture_candidate
```

No candidate is promoted solely because it appears in this directory.

## Non-Claims

```text
This directory does not certify external frameworks.
This directory does not claim that all candidates are comparable.
This directory does not claim compatibility with StegVerse.
This directory does not grant execution authority.
This directory does not turn an unsourced candidate into usable evidence.
```

Candidate visibility is observatory work. Standing must still be reconstructed from current source, evidence, authority, policy, delegation, admissibility, and commit-time conditions.
