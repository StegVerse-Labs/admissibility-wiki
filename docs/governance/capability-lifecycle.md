# Capability Lifecycle

## Purpose

This page defines the shared lifecycle states used to distinguish a documented surface from an implemented, validated, released, verified, or operational capability.

A capability is not operational merely because a page, script, workflow, or artifact exists. It must occupy a specific lifecycle state and carry evidence appropriate to that state.

## Lifecycle states

| State | Meaning | Required evidence |
| --- | --- | --- |
| Proposed | A capability has been described but not implemented. | Proposal, scope, boundary, and intended evidence path. |
| Implemented | Files or artifacts exist for the capability. | Source files, generated artifacts, or implementation records. |
| Internally Validated | Repository automation has validated the implementation. | Passing validators, workflow evidence, and local receipts. |
| Release Authorized | A release decision has been explicitly recorded. | Release authorization record and standing boundary. |
| Publicly Verified | Public URLs or published artifacts have been verified after release authorization. | Public verification evidence recorded after authorization. |
| Operational | The capability is allowed to participate in governed ecosystem transitions. | Release evidence, public verification, receipt binding, and current standing. |
| Deprecated | The capability is no longer valid for new transitions. | Deprecation record and replacement or shutdown boundary. |

## Status interpretation

```text
Implemented does not imply released.
Released does not imply publicly verified.
Publicly verified does not imply operational standing.
Operational standing can be revoked or deprecated.
```

## Capability status fields

A machine-readable lifecycle artifact should expose:

```text
capability_id
current_state
implemented
internally_validated
release_authorized
publicly_verified
operational
deprecated
blocked_by
evidence
boundary
```

## Boundary

This lifecycle is a classification model, not an authority source. It does not grant release, public standing, operational standing, or execution authority by itself.

## Current status

```text
CAPABILITY_LIFECYCLE_REGISTRY_PRESENT
```
