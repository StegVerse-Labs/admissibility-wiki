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

## Bidirectional sidebar association contract

Every page in the `External Frameworks` sidebar is now represented in:

```text
static/external-frameworks/sidebar-page-associations.v1.json
```

Each association identifies:

```text
sidebar route
page path
page type: support | framework
stable framework_id or support association_id
docs-registry presence state
static-registry presence state
```

The existing validator invoked by `npm run validate:external-frameworks` now compares the sidebar and association artifact in both directions and in order.

It fails when:

```text
- a sidebar page is added without an association;
- an associated page is removed from the sidebar;
- sidebar order and association order diverge;
- an associated page file is missing;
- a framework_id is duplicated;
- registry presence differs from the declared state;
- a missing registry binding is not explicitly declared;
- stored page counts are stale.
```

Current known registry gaps are represented as `missing_explicit`. That state permits the existing migration gap to remain visible while preventing silent drift. When a missing registry entry is added, its association must change to `present` in the same change or validation fails.

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

Sidebar visibility does not guarantee registry inclusion, manifest coverage, generated report coverage, or validator coverage. The association artifact now makes each gap explicit and validation-bound.

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

The seven remaining external records classify as `SOURCE_REVIEWED`:

```text
Agent Governance Playbook
KILLSWITCH.md / Emergency Stop Convention
Model Context Protocol
Agent2Agent Protocol
Guardrails AI
Llama Guard
NeMo Guardrails
```

The two internal records are not external frameworks:

```text
Admissible Existence Seed Cycle
  -> INTERNAL_ECOSYSTEM_STATUS_MIRROR

Decision Authority Compatibility
  -> INTERNAL_ECOSYSTEM_COMPATIBILITY_CROSSWALK
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

## Current audit implication

The prior 13-framework figure described only one audited family. It did not describe the repository-wide inventory.

The corrected present counts are:

```text
36 actual external-framework or external-convention records
2 internal ecosystem records
38 total distinct inventory records
50 total External Frameworks sidebar pages including support pages
```

## Next actions

```text
1. Add missing registry entries for all 18 sidebar-only external frameworks.
2. Add missing sidebar coverage or explicit non-public status for registry-only records.
3. Add record_type and external_framework fields to every registry entry.
4. Generate one inventory artifact from the union of registry, manifests, reports, and sidebar paths.
5. Extend validation from registry presence to one-to-one manifest and report coverage.
6. Recalculate section completion against 36 external records plus 2 internal records.
7. Remediate PARTIAL framework pages to the required-section standard.
```

## Boundary

```text
cohort count != total framework count
registry count != public page count
sidebar count != machine-readable coverage
inventory record != external framework
page visibility != evidence completeness
registry inclusion != certification or execution authority
association parity != compatibility or standing
```