---
title: Public Reachability Evidence Guide
---

# Public Reachability Evidence Guide

## Purpose

This guide defines the evidence that must be captured before the Admissibility Wiki activation posture can be changed.

It does not perform the network checks and does not claim activation.

## Public Target

```text
https://stegverse-labs.github.io/admissibility-wiki/
```

## Required Evidence Records

Record evidence for each target below before changing activation status.

### Landing Page

```text
check_id: public_site_loads
required_url: https://stegverse-labs.github.io/admissibility-wiki/
required_result: reachable over HTTPS
record: timestamp, HTTP status, and observed page title or page marker
```

### Ontology JSON

```text
check_id: ontology_json_reachable
required_url: https://stegverse-labs.github.io/admissibility-wiki/ontology/admissibility-vocabulary.v0.1.json
required_result: reachable over HTTPS and parses as JSON
record: timestamp, HTTP status, and schema or top-level key observed
```

### Wiki Status JSON

```text
check_id: status_json_reachable
required_url: https://stegverse-labs.github.io/admissibility-wiki/status/admissibility-wiki-status.json
required_result: reachable over HTTPS and parses as JSON
record: timestamp, HTTP status, repository field, and status field
```

### Public Activation Receipt Example

```text
check_id: activation_receipt_reachable
required_url: https://stegverse-labs.github.io/admissibility-wiki/status/public-activation-receipt.example.json
required_result: reachable over HTTPS and parses as JSON
record: timestamp, HTTP status, schema field, and activation_state field
```

### Governance Decision Example

```text
check_id: governance_decision_reachable
required_url: https://stegverse-labs.github.io/admissibility-wiki/governance/decisions/decision.example.007.json
required_result: reachable over HTTPS and parses as JSON
record: timestamp, HTTP status, decision_id field, and decision field
```

## Evidence Storage Rule

Store completed evidence in a new receipt under:

```text
static/status/public-activation-receipt.<YYYYMMDD>.json
```

Do not overwrite the example receipt unless the example schema itself changes.

## Activation Rule

Activation posture may only change after all required evidence records are complete.

## Non-Claims

```text
This guide does not activate the site.
This guide does not prove admissibility.
This guide does not grant publication authority.
This guide does not replace repository validation.
```

## Next Safe Action

After GitHub Pages deployment completes, record a real public activation receipt using the evidence requirements above.
