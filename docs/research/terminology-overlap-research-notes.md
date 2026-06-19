---
title: Terminology Overlap Research Notes
---

# Terminology Overlap Research Notes

## Purpose

This page records source-aware terminology overlap notes for the Admissibility Wiki.

The purpose is not to accept equivalence claims immediately. The purpose is to preserve researched candidate mappings so reviewers can decide whether a term is equivalent, overlapping, adjacent, broader, narrower, contradictory, or StegVerse-specific.

## Page Status

```text
active
```

## Page Posture

```text
research note
```

## Maturity Posture

```text
source-aware preliminary
```

## Authority Boundary

This page does not accept any external term as equivalent to a StegVerse term.

It records researched candidates for later proposal and decision review.

Accepted equivalence still requires a proposal, decision record, and target-page update.

## Research Method

For each StegVerse term, check whether external terminology appears to be:

```text
equivalent
overlapping
adjacent
broader_than
narrower_than
contradicts
unresolved
```

Use conservative placement unless the external term clearly describes the same underlying concept for the page's purpose.

## Reviewed Source Families

### W3C PROV

Source family:

```text
https://www.w3.org/TR/prov-overview/
https://www.w3.org/TR/prov-primer/
```

Observed relevance:

PROV defines provenance as information about entities, activities, and people involved in producing data or things, supporting quality, reliability, or trustworthiness assessment.

Candidate mapping:

| StegVerse term | Candidate external term | Relationship posture | Notes |
| --- | --- | --- | --- |
| Reconstructability | Provenance | overlapping | Provenance can support reconstruction, but it does not necessarily reconstruct why consequence had standing at commit time. |
| Receipt-Bound Execution | Provenance record | overlapping | A receipt may include provenance-like information, but StegVerse receipt-bound execution also includes authority, evidence, policy, review, and decision posture. |
| Evidence Posture | Provenance evidence | adjacent | Provenance may support evidence evaluation, but evidence posture is the current admissibility-relevant state of evidence. |

Preliminary conclusion:

Do not mark provenance as equivalent to reconstructability or receipt-bound execution without additional review.

### Open Policy Agent

Source family:

```text
https://www.openpolicyagent.org/docs
```

Observed relevance:

OPA describes a general-purpose policy engine that decouples policy decision-making from policy enforcement and evaluates structured input against policies and data.

Candidate mapping:

| StegVerse term | Candidate external term | Relationship posture | Notes |
| --- | --- | --- | --- |
| Policy Reference | Policy-as-code | overlapping | Policy-as-code may define rules, but a policy reference is the specific rule basis cited for a transition decision. |
| Commit-Time Authority | Policy decision | overlapping | A policy decision may contribute to authority evaluation, but commit-time authority also includes standing at the binding moment. |
| Governance Boundary | Policy enforcement boundary | adjacent | Enforcement boundary may describe where policy is applied; governance boundary describes what the system claims to govern, observe, authorize, enforce, or prove. |

Preliminary conclusion:

Do not mark policy-as-code, policy decision, or policy enforcement as equivalent to StegVerse commit-time authority without additional review.

### NIST SP 800-53

Source family:

```text
https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
```

Observed relevance:

NIST SP 800-53 provides a catalog of security and privacy controls and includes control families such as Access Control, Audit and Accountability, Assessment, Authorization and Monitoring, Configuration Management, Incident Response, and Supply Chain Risk Management.

Candidate mapping:

| StegVerse term | Candidate external term | Relationship posture | Notes |
| --- | --- | --- | --- |
| Review Posture | Assessment, Authorization and Monitoring | overlapping | Assessment and authorization may overlap with review state, but review posture is a transition-specific condition at commit time. |
| Reconstructability | Audit and Accountability | overlapping | Audit controls can support reconstruction, but reconstructability asks whether a reviewer can recover why a decision appeared to have standing. |
| Governance Boundary | Control boundary | adjacent | Control boundaries may help define system scope, but governance boundary includes claims and non-claims about authority and proof. |

Preliminary conclusion:

NIST control-family language is useful for comparison and source-aware notes, but it should not be treated as accepted-equivalent terminology without a targeted proposal.

### NIST Cybersecurity Framework

Source family:

```text
https://www.nist.gov/cyberframework
```

Observed relevance:

NIST describes the Cybersecurity Framework as voluntary guidance and a common language for managing cybersecurity risk, with functions used to organize risk-management outcomes.

Candidate mapping:

| StegVerse term | Candidate external term | Relationship posture | Notes |
| --- | --- | --- | --- |
| Terminology Convergence | Common language | overlapping | The wiki also aims to create cross-domain common language, but does so for transition governance terminology and admissibility mappings. |
| Governance Boundary | Risk-management scope | adjacent | Risk-management scope helps define program boundaries; governance boundary defines what a system claims to decide, enforce, observe, or prove. |

Preliminary conclusion:

NIST common-language framing supports the wiki's sector-convergence goal but does not define the StegVerse-specific commit-time admissibility structure.

## Current Recommended Target-Page Actions

Do not add any accepted `Equivalent Terms` from this note yet.

Recommended actions:

1. Leave `Provenance` as overlapping for `Reconstructability` and `Receipt-Bound Execution`.
2. Leave `Policy-as-code`, `Policy decision`, and `Policy enforcement` as overlapping or adjacent for policy and authority pages.
3. Leave `Audit and Accountability` as overlapping for `Reconstructability`.
4. Add source-specific proposal records only when a reviewer is ready to decide an individual mapping.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Related Pages

- [Terminology Convergence](../governance/terminology-convergence.md)
- [Proposal Lifecycle](../governance/proposal-lifecycle.md)
- [Decision Record](../governance/decision-record.md)
- [Reconstructability](../glossary/reconstructability.md)
- [Receipt-Bound Execution](../glossary/receipt-bound-execution.md)
- [Commit-Time Authority](../glossary/commit-time-authority.md)
