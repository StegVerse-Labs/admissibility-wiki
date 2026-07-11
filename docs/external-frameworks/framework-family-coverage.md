---
title: External Framework Family Coverage
---

# External Framework Family Coverage

## Purpose

This page turns the expanded external-framework intake into a governed coverage map and promotion queue.

The registry is intentionally broader than the current set of full framework pages. Coverage means the family is represented in intake. It does not mean every candidate is sourced, mapped, tested, compatible, or validated.

```text
family coverage != validation
candidate count != framework quality
promotion priority != endorsement
promotion queue != execution authority
```

## Current Intake Coverage

| Framework family | Candidate count | Structural status | Promotion posture |
|---|---:|---|---|
| risk_and_assurance | 8 | represented | promote machine-readable and AI-specific controls first |
| model_eval_and_monitoring | 6 | represented | promote evaluation, regression, and vulnerability-test surfaces |
| identity_and_authority | 5 | represented | promote delegation, workload identity, and credential evidence |
| provenance_and_trace | 5 | represented | promote lineage, signing, and supply-chain evidence |
| policy_as_code | 3 | represented | promote policy decision and authorization languages |
| threat_and_security | 3 | represented | promote adversarial and defensive knowledge mappings |
| privacy_and_data_governance | 3 | represented | promote consent, retention, and privacy-control sources |
| runtime_governance | 3 | represented | promote runtime guardrail and safety-classifier surfaces |
| regulatory_and_standards | 3 | represented | promote current official standards and regulatory profiles |
| agent_protocols | 3 | represented | promote tool, context, and agent interoperability protocols |

Current total: **42 source-required candidates across 10 intake classes**.

## Promotion Priority Tiers

### Tier 1 — Direct transition-boundary relevance

```text
Open Policy Agent
Cedar Policy
OSCAL
SPIFFE/SPIRE
W3C Verifiable Credentials
in-toto
SLSA
Sigstore
Model Context Protocol
Agent2Agent Protocol
```

These candidates are closest to policy evaluation, authority/delegation, provenance, receipts, and governed tool/agent transitions.

### Tier 2 — Security, evaluation, and runtime evidence

```text
MITRE ATT&CK
MITRE D3FEND
NIST SP 800-53
NIST SP 800-207
NIST SSDF
NIST AI RMF Generative AI Profile
MLCommons AI Safety
HELM
garak
promptfoo
Guardrails AI
Llama Guard
NeMo Guardrails
```

These candidates can improve benchmark case design, threat context, regression testing, monitoring, and runtime safety comparison.

### Tier 3 — Documentation, privacy, and broader governance context

```text
W3C PROV
OpenLineage
OpenID Connect
OAuth 2.0
W3C Decentralized Identifiers
GDPR
NIST Privacy Framework
ISO/IEC 27701
Model Cards
Datasheets for Datasets
OECD AI Principles
UNESCO Recommendation on AI Ethics
AI Verify
```

These candidates strengthen documentation, identity, privacy, provenance, and assurance context but generally require adapters before runtime benchmark treatment.

## Structural Promotion Rule

A candidate advances only through the existing source-gated promotion criteria:

```text
source_required
-> sourced_intake
-> page_candidate
-> mapping_candidate
-> fixture_candidate
```

No candidate skips canonical source, scope, non-claims, relationship classification, benchmark relevance, authority boundary, or evidence-posture review.

## Coverage Gaps To Monitor

The current registry is broad, but not closed. Future intake should watch for underrepresented families such as:

```text
formal verification and theorem-proving frameworks
capability-based security and object-capability systems
confidential computing and trusted execution evidence
hardware-rooted attestation
data usage control and sticky policy systems
multi-agent coordination and delegation standards
sector-specific safety cases
human oversight and appeal mechanisms
incident disclosure and post-event accountability
cross-border data and jurisdictional governance
```

## Non-Claims

```text
This coverage map does not certify candidates.
This coverage map does not rank framework quality.
This coverage map does not claim compatibility.
This coverage map does not grant execution authority.
This coverage map does not make promotion automatic.
```

Standing must be reconstructed from current source, evidence, authority, policy, delegation, admissibility, and commit-time conditions.
