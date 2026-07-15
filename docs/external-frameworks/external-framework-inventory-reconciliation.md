---
title: External Framework Inventory Reconciliation
---

# External Framework Inventory Reconciliation

## Purpose

This page distinguishes machine-readable registry entries, framework-specific public pages, internal ecosystem records, and support/audit pages in the External Frameworks section.

A cohort count is not the repository-wide framework count, and a record stored in this section is not necessarily an external framework.

## Current counts

```text
machine-readable docs registry entries: 20
machine-readable static registry entries: 11
framework-specific pages in the External Frameworks sidebar: 26
support, audit, intake, benchmark, and governance pages in the sidebar: 24
total External Frameworks sidebar pages: 50
distinct records across registry and sidebar: 38
actual external-framework or external-convention records: 36
internal ecosystem records stored in the inventory: 2
records explicitly classified or dispositioned: 38
```

The 38-record union remains the reconciliation scope. The correct external-framework count is 36 because two records are internal ecosystem artifacts:

```text
Admissible Existence Seed Cycle
Decision Authority Compatibility
```

## Sidebar association enforcement

Every page in the External Frameworks sidebar is represented in:

```text
static/external-frameworks/sidebar-page-associations.v1.json
```

The association artifact preserves sidebar order and classifies each page as either a framework page or a support page. Framework pages receive a stable framework ID. Support pages receive a stable association ID.

The validator compares the sidebar and association artifact bidirectionally. A one-sided addition, removal, reordering, path change, page deletion, duplicate ID, or registry-state change fails validation.

## Framework artifact binding enforcement

Every framework-specific sidebar page is also represented in:

```text
static/external-frameworks/sidebar-framework-artifact-bindings.v1.json
```

Each binding records:

```text
framework_id
page_path
manifest_path
manifest_state
report_path
report_state
evidence_class_source
page_completeness_source
```

Current artifact coverage:

```text
framework pages: 26
manifest and report present: 8
manifest and report missing_explicit: 18
undeclared manifest/report states: 0
```

The eight currently artifact-bound framework pages are:

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

The remaining 18 sidebar framework pages have explicit `missing_explicit` manifest and report states. If a manifest or report is added without changing its binding state to `present`, validation fails. If a bound manifest or report is removed while still declared `present`, validation also fails.

This makes the relationship bidirectional:

```text
sidebar framework page
        <-> page association
        <-> docs registry
        <-> static registry
        <-> manifest
        <-> compatibility report
        <-> evidence-class source
        <-> page-completeness source
```

## Registry-only records

The following docs-registry entries do not currently have a matching framework-specific item in the External Frameworks sidebar:

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
Admissible Existence Seed Cycle — internal record
Decision Authority Compatibility — internal record
```

Registry presence does not guarantee public navigation coverage.

## Sidebar-only external-framework pages

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

The following records are currently represented in both the docs registry and the framework-specific sidebar inventory:

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

## Evidence-classification closure

All 38 records now have either an explicit external-framework evidence classification or an internal-record disposition.

```text
external records classified: 36
internal records dispositioned: 2
unclassified records: 0
```

The final nine-record closure is recorded in:

```text
docs/external-frameworks/inventory-record-type-and-evidence-closure.md
```

## Reconciliation requirements

A complete inventory requires, for every distinct record:

```text
stable framework_id or record_id
record_type
external_framework: true | false
public page path
machine-readable manifest path
source posture
current evidence class or internal evidence disposition
page completeness class
generated report path
sidebar/navigation state
validator coverage
non-claims and authority boundary
```

Missing fields must fail closed rather than causing a record to disappear from reported totals.

## Counting rule

Future progress reports must use explicit labels:

```text
frameworks audited in current cohort
external frameworks evidence-classified overall
internal ecosystem records dispositioned
machine-readable registry entries
framework-specific public pages
distinct records across all inventories
support and audit pages
```

The phrase `external frameworks total` must not be used without identifying the inventory and excluding internal records.

## Next actions

```text
1. Add missing registry entries for all 18 sidebar-only external frameworks.
2. Add missing manifests and compatibility reports for those 18 framework pages.
3. Add missing sidebar coverage or explicit non-public status for registry-only records.
4. Add record_type and external_framework fields to every registry entry.
5. Generate one inventory artifact from the union of registries, manifests, reports, and sidebar paths.
6. Validate one-to-one record_id, page, manifest, report, and navigation coverage.
7. Recalculate section completion against 36 external records plus 2 internal records.
8. Remediate PARTIAL framework pages to the required-section standard.
```

## Boundary

```text
cohort count != total framework count
registry count != public page count
sidebar count != machine-readable coverage
inventory record != external framework
page visibility != evidence completeness
manifest/report presence != compatibility
registry inclusion != certification or execution authority
```
