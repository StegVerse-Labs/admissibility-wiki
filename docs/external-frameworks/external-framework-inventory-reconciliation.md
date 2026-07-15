---
title: External Framework Inventory Reconciliation
---

# External Framework Inventory Reconciliation

## Purpose

This page records the canonical relationship among external-framework records, internal ecosystem records stored in the same section, public sidebar pages, manifests, compatibility reports, and legacy compatibility indexes.

A cohort count is not a repository-wide framework count. A record stored under `external-frameworks` is not necessarily an external framework.

## Canonical inventory posture

```text
canonical registry: docs/external-frameworks/index.json
canonical union inventory: static/external-frameworks/canonical-union-inventory.v1.json
sidebar associations: static/external-frameworks/sidebar-page-associations.v1.json
artifact bindings: static/external-frameworks/sidebar-framework-artifact-bindings.v1.json
navigation dispositions: static/external-frameworks/registry-navigation-dispositions.v1.json
legacy compatibility index: static/external-frameworks/external-framework-registry.v0.1.json
```

The docs registry and canonical union inventory define the complete 38-record scope. The older static registry remains a compatibility index and must not be treated as a second canonical inventory.

## Current counts

```text
canonical records: 38
actual external frameworks or conventions: 36
internal ecosystem records: 2
public sidebar framework pages: 26
explicitly non-public external records: 10
internal records excluded from framework navigation: 2
support, audit, intake, benchmark, and governance pages: 24
total External Frameworks sidebar pages: 50
navigated manifests present: 26 of 26
navigated compatibility reports present: 26 of 26
unclassified records: 0
```

The two internal records are:

```text
Admissible Existence Seed Cycle
Decision Authority Compatibility
```

## Sidebar association enforcement

Every page in the External Frameworks sidebar is represented in:

```text
static/external-frameworks/sidebar-page-associations.v1.json
```

The validator compares sidebar order and association order bidirectionally. A one-sided addition, removal, reordering, path change, page deletion, duplicate ID, or declared registry-state change fails validation.

## Framework artifact binding enforcement

Every framework-specific sidebar page is represented in:

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

Current state:

```text
framework pages: 26
manifest and report present: 26
manifest and report missing_explicit: 0
undeclared artifact states: 0
```

Manifest or report appearance and disappearance are both guarded. A new artifact requires its binding to change to `present`; a removed artifact requires an explicit state change and otherwise fails validation.

## Navigation disposition enforcement

Every canonical registry entry must be exactly one of:

```text
public_sidebar
non_public_explicit
internal_record
```

The 12 records not represented as framework-specific sidebar pages are recorded in:

```text
static/external-frameworks/registry-navigation-dispositions.v1.json
```

Their disposition is:

```text
10 external records -> non_public_explicit
2 internal ecosystem records -> internal_record
```

A canonical registry record may not silently disappear from navigation. It must either remain sidebar-bound or receive an explicit disposition with a reason and page path.

## Canonical union inventory

The normalized union inventory records, for all 38 records:

```text
record_id
record_type
external_framework: true | false
navigation_state
page-path convention or explicit exception
manifest-path convention
compatibility-report-path convention
```

The inventory uses conventions rather than duplicating every full path:

```text
page: docs/external-frameworks/{page_slug}.md
manifest: docs/external-frameworks/{record_id}.json
report: docs/external-frameworks/reports/{record_id}.compatibility.json
```

Only records whose page slug differs from the record ID declare an exception. This reduces path-copy drift.

## Evidence posture

All 38 records have either an external-framework evidence class or an internal-record disposition:

```text
external records classified: 36
internal records dispositioned: 2
unclassified records: 0
```

Manifest and report presence does not upgrade evidence strength. Most framework records remain `SOURCE_REVIEWED`; comparative claims remain prohibited unless raw outputs, timestamps, runtime configuration, pinned source versions or hashes, replay commands, expected outcomes, and independent reproduction are all present.

## Remaining reconciliation work

```text
1. Validate the canonical union inventory directly against the docs registry, sidebar associations, navigation dispositions, manifests, and reports.
2. Migrate or retire the legacy 16-record static compatibility index without creating a second canonical source.
3. Regenerate evaluation-results and generated page-status blocks under report schema 0.7.
4. Remediate short PARTIAL framework pages to the required-section standard.
5. Observe the single canonical workflow and repair only directly observed failures.
6. Recalculate full section-completeness status after generated-page synchronization.
```

## Boundary

```text
cohort count != total framework count
registry count != public page count
sidebar count != machine-readable coverage
inventory record != external framework
page visibility != evidence completeness
manifest/report presence != compatibility
source review != reproducible comparison
registry inclusion != certification or execution authority
```
