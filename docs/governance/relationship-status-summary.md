---
title: Relationship Status Summary
---

# Relationship Status Summary

## Purpose

This page summarizes the current relationship-proposal state so future sessions do not recreate accepted or deferred terminology work.

## Accepted Overlap Records

```text
proposal.example.005 / decision.example.005
target_page: docs/glossary/reconstructability.md
external_term: Provenance
source_family: W3C PROV
disposition: ALLOW_AS_OVERLAP
equivalent_status: not accepted

proposal.example.006 / decision.example.006
target_page: docs/glossary/policy-reference.md
external_term: policy-as-code
source_family: Open Policy Agent documentation
disposition: ALLOW_AS_OVERLAP
equivalent_status: not accepted

proposal.example.007 / decision.example.007
target_page: docs/glossary/governance-boundary.md
external_term: AI risk-management governance language
source_family: NIST AI Risk Management Framework
disposition: ALLOW_AS_OVERLAP
equivalent_status: not accepted

proposal.example.008 / decision.example.008
target_page: docs/glossary/commit-time-authority.md
external_term: policy decision
source_family: Open Policy Agent documentation
disposition: ALLOW_AS_OVERLAP
equivalent_status: not accepted

proposal.example.009 / decision.example.009
target_page: docs/glossary/reconstructability.md
external_term: Audit and Accountability
source_family: NIST SP 800-53 Rev. 5
disposition: ALLOW_AS_OVERLAP
equivalent_status: not accepted
```

## Duplicate Avoidance Rule

Do not create new proposal records for the same source-family and target-page relationships listed above.

## Equivalent-Term Boundary

No listed relationship above accepts an equivalent term.

Future equivalence claims require:

```text
source evidence
claim comparison
mismatch analysis
overclaiming-risk analysis
decision record
replay record
reconstruction note
explicit equivalent-status acceptance
```

## Next Safe Build Target

Add another source-backed relationship proposal only if it covers a materially new source family and does not duplicate proposals 005, 006, 007, 008, or 009.

Public activation status should be updated only after the GitHub.io project page, HTTPS, ontology reachability, status reachability, activation-checklist reachability, and governance-record reachability are verified.
