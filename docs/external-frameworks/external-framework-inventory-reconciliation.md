---
title: External Framework Inventory Reconciliation
---

# External Framework Inventory Reconciliation

## Purpose

This page distinguishes the machine-readable registry, framework-specific public pages, and support/audit pages in the External Frameworks section.

A cohort count is not the repository-wide framework count.

## Current counts

```text
machine-readable registry entries: 20
framework-specific pages in the External Frameworks sidebar: 26
support, audit, intake, benchmark, and governance pages in the sidebar: 22
total External Frameworks sidebar pages: 48
distinct framework records across registry and sidebar: 38
```

The 38-record union is the correct current scope for reconciliation. It includes records found only in the registry, records found only in the public sidebar, and records present in both.

## Registry-only framework records

The following registry entries do not currently have a matching framework-specific item in the External Frameworks sidebar:

```text
AAR
MITRE ATLAS
OWASP Top 10 for LLM Applications
Agent Governance Playbook
Emergency Stop Convention
NIST AI RMF
ISO/IEC 42001
EU AI Act
Policy Cards
Runtime Governance for AI Agents
Admissible Existence Seed Cycle
Decision Authority Compatibility
```

Registry presence does not guarantee public navigation coverage.

## Sidebar-only framework pages

The following framework-specific sidebar pages do not currently have a matching entry in `docs/external-frameworks/index.json`:

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
OpenID Connect
OAuth 2.0
W3C Decentralized Identifiers
OpenLineage
W3C PROV
Guardrails AI
Llama Guard
NeMo Guardrails
```

Sidebar visibility does not guarantee registry inclusion, manifest coverage, generated report coverage, or validator coverage.

## Shared records

The following records are currently represented in both the registry and the framework-specific sidebar inventory:

```text
GLM
EVIDE
ASRO
DecisionAssure
MindForge
Morrison Runtime
CARE Runtime
KPT
```

## Reconciliation requirements

A complete framework inventory requires, for every distinct framework record:

```text
stable framework_id
public page path
machine-readable manifest path
source posture
current evidence class
page completeness class
generated report path
sidebar/navigation state
validator coverage
non-claims and authority boundary
```

Missing fields must fail closed rather than causing a record to disappear from the reported total.

## Counting rule

Future progress reports must use explicit labels:

```text
frameworks audited in current cohort
frameworks evidence-classified overall
machine-readable registry entries
framework-specific public pages
distinct framework records across all inventories
support and audit pages
```

The phrase `external frameworks total` must not be used without identifying which inventory is being counted.

## Current audit implication

The prior 13-framework figure described only the policy, identity, provenance, and supply-chain cohort. It did not describe the repository-wide framework inventory.

The repository-wide reconciliation target is currently 38 distinct framework records, not 13 and not merely the 20 registry entries.

## Next actions

```text
1. Add missing registry entries for sidebar-only frameworks.
2. Add missing sidebar coverage or explicit non-public status for registry-only records.
3. Generate one inventory artifact from the union of registry, manifests, reports, and sidebar paths.
4. Validate one-to-one framework_id, page, manifest, report, and navigation coverage.
5. Recalculate audit completion against the reconciled 38-record inventory.
```

## Boundary

```text
cohort count != total framework count
registry count != public page count
sidebar count != machine-readable coverage
page visibility != evidence completeness
registry inclusion != certification or execution authority
```
