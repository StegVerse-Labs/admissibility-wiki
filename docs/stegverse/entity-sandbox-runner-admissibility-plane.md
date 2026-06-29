---
title: Entity Sandbox Runner Admissibility Plane
---

# Entity Sandbox Runner Admissibility Plane

## Status

```text
source_repo: StegGhost/entity-sandbox-runner
release_goal: admissibility_plane_activation_candidate
wiki_status: documentation_surface_installed
activation_state: pending_external_evidence
```

## Source authority

The source repository remains authoritative for its runtime files, manifests, transition table, CGE route fingerprints, transition receipts, sandbox repair decisions, and admissibility-plane verification reports.

This wiki page is a terminology and documentation surface only.

## Documented chain

```text
manifest schema validation
→ transition table resolution
→ CGE route fingerprint
→ transition receipt emission
→ sandbox repair route when required
→ repair result re-entry through ingestion
→ startup admissibility verification
→ release integration verification
```

## Core terms

### Manifest schema validation

The manifest schema defines the required shape of a governed artifact before ingestion may route it.

### Transition table resolution

The transition table maps a manifest-bearing artifact to an allowed route, denied route, or fail-closed condition.

### CGE route fingerprint

The CGE route fingerprint binds the manifest, payload, source hash, transition identifier, and transition table hash into a reproducible route decision input.

### Transition receipt

The transition receipt records the routed decision, destination, source hash, manifest hash, transition table hash, and CGE fingerprint hashes.

### Sandbox repair re-entry

Sandbox repair is non-authoritative. A sandbox result must return to ingestion before reconciliation or admissibility evaluation can continue.

## Boundary

This page does not certify the source repository as activated. It does not issue commit-time permission. It does not replace source repository receipts or source repository verification reports.

## Required source evidence before stronger status

```text
StegGhost/entity-sandbox-runner brain_reports/admissibility_plane_verification.json
StegGhost/entity-sandbox-runner brain_reports/release_integration_verification.json
StegGhost/entity-sandbox-runner release/entity_sandbox_runner_admissibility_plane_release_packet.json
StegGhost/entity-sandbox-runner transition_receipts/
```
