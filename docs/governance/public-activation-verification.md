---
title: Public Activation Verification
---

# Public Activation Verification

## Purpose

This checklist defines what must be verified before the Admissibility Wiki activation posture can be changed from repository-ready to publicly activated.

It does not claim public activation by itself.

## Activation Target

```text
admissibility.stegverse.org
```

## Required Verification Checks

### 1. Public Site Loads

```text
status: pending
required_result: HTTPS page load succeeds for the activation target.
evidence_required: timestamped URL check or deployment log.
```

### 2. DNS Resolves

```text
status: pending
required_result: activation target resolves to the configured GitHub Pages destination.
evidence_required: DNS lookup result.
```

### 3. HTTPS Is Valid

```text
status: pending
required_result: browser or TLS check confirms a valid HTTPS certificate for the activation target.
evidence_required: certificate or browser verification output.
```

### 4. Ontology JSON Is Reachable

```text
status: pending
required_result: static/ontology/admissibility-vocabulary.v0.1.json is reachable from the public site.
evidence_required: public URL and HTTP status.
```

### 5. Status JSON Is Reachable

```text
status: pending
required_result: static/status/admissibility-wiki-status.json is reachable from the public site.
evidence_required: public URL and HTTP status.
```

### 6. Governance Records Are Reachable

```text
status: pending
required_result: proposal, decision, replay, and evidence records for examples 005 through 008 are reachable from the public site or clearly linked as repository artifacts.
evidence_required: URL list and HTTP status results.
```

### 7. Public Page Navigation Works

```text
status: pending
required_result: glossary, governance, proof-path, and landing-page navigation all load without broken internal links.
evidence_required: build output or link-check output.
```

## Non-Claims

```text
This checklist does not activate the site.
This checklist does not prove admissibility.
This checklist does not grant publication authority.
This checklist does not replace deployment logs.
This checklist does not replace DNS or HTTPS verification.
```

## Activation Update Rule

Only update activation posture after all required checks are complete and evidence is recorded.

## Next Safe Action

Run deployment and reachability checks, then record evidence in a separate activation receipt.
