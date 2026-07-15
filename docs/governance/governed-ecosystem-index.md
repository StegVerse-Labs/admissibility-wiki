# Governed Ecosystem Index

## Purpose

This page is the public navigation and status index for governed ecosystem transition framing.

It identifies the principal entry, governance, proof, runtime, custody, deployment, and downstream coordinates. Inclusion in this index does not mean a coordinate is deployed, authoritative, or permitted to execute.

## Public doctrine and registry pages

| Surface | Purpose | Current posture |
| --- | --- | --- |
| [Governed Ecosystem Transitions](./governed-ecosystem-transitions.md) | Defines the shared transition path. | `PUBLIC_DOCTRINE` |
| [Governed Input Classes](./governed-input-classes.md) | Registers candidate input classes and entry coordinates. | `PUBLIC_REGISTRY` |
| [Governed Output Classes](./governed-output-classes.md) | Registers bounded result classes and commitment conditions. | `PUBLIC_REGISTRY` |
| [Governed Transition Map](./governed-transition-map.md) | Maps candidate inputs to possible governed results. | `PUBLIC_MAP` |
| [Governed LLM Activation Map](./governed-llm-activation-map.md) | Shows the complete governed-LLM topology. | `PUBLIC_MAP_WITH_EXTERNAL_GATES` |
| [Capability Lifecycle](./capability-lifecycle.md) | Separates proposed, built, validated, deployed, and activated capability states. | `PUBLIC_DOCTRINE` |
| [Ecosystem Capability Status](./ecosystem-capability-status.md) | Records current bounded capability posture. | `STATUS_SURFACE` |
| [Wiki Section Completeness Audit](./wiki-section-completeness-audit.md) | Tracks section-level completeness and remediation. | `ACTIVE_AUDIT` |

## Entry and user-facing coordinates

```text
StegVerse-Labs/Site
  -> ecosystem-chat.html
  -> ecosystem-usage.html
  -> ecosystem-comparison.html
  -> governed-transitions.html
  -> demo.html
  -> applicability.html
  -> math-solver/
```

These are public entry or demonstration surfaces. Site display does not create proof authority, execution authority, custody, or live-provider activation.

## Runtime and contract coordinates

```text
StegVerse-org/LLM-adapter
  -> provider/output/continuity/action/authority boundary
  -> fixture-first governed session artifacts
  -> disabled execution handoff by default

StegVerse-org/StegVerse-SDK
  -> packet validation
  -> intake routing
  -> manifest binding
  -> receipt handoff

StegVerse-org/core-node-runtime-demo
  -> runtime producer and governed route demonstration

StegVerse-002/micro-node-runtime
  -> portable transition-request contract demonstration
```

## Formalism and proof coordinates

```text
Data-Continuation/formalism-tests
  -> executable fixtures
  -> expected outcomes
  -> proof receipts
  -> Transition Table authority

RTG / STCM surfaces
  -> candidate or research formalism posture unless receipt-backed proof is present
```

The wiki explains and crosswalks these sources. It does not inherit their proof authority.

## Custody and reconstruction coordinates

```text
master-records/orchestration
  -> authenticated custody
  -> retained master records and pointers
  -> reconstructability evidence
```

Receipt emission or manifest binding is not Master-Records installation. `RECORDED` requires authenticated custody evidence and reconstructability proof.

## Deployment and external coordinates

```text
GitHub Pages public route
same-origin authorized gateway or proxy
live provider credentials
continuity search service
external executor
package or release publication
```

These coordinates remain `EXTERNAL`, `PREPARED_NOT_DEPLOYED`, `VALIDATION_PENDING`, or `BLOCKED` until current evidence proves otherwise.

## Downstream documentation destinations

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-002/stegguardian-wiki
StegVerse-Labs/repo-standards
```

Downstream awareness is not completed propagation. Each destination handoff must authorize mutation before updates are applied.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `PUBLIC_DOCTRINE` | Public explanation exists; no implementation claim implied. |
| `PUBLIC_REGISTRY` | Public classification exists; instances remain individually governed. |
| `FIXTURE_ONLY` | Reproducible static or local proof exists without live external consequence. |
| `IMPLEMENTED_PENDING_VALIDATION` | Source implementation exists; current-main evidence is not yet confirmed. |
| `PREPARED_NOT_DEPLOYED` | Deployment contract or client is prepared but no authorized live route is proven. |
| `VALIDATION_PENDING` | Required automated evidence has not yet been observed. |
| `EXTERNAL` | Completion depends on another repository, service, credential, or authority domain. |
| `BLOCKED` | Activation prerequisites are known not to be complete. |
| `VERIFIED` | Required evidence has been observed and bound to the claimed scope. |

## Boundary

```text
Index presence != implementation.
Implementation != validation.
Validation != deployment.
Deployment != admissibility.
Receipt emission != custody.
Public visibility != proof authority.
Handoff awareness != destination mutation authority.
```

## Current status

```text
GOVERNED_ECOSYSTEM_INDEX_COMPLETE_WITH_EXTERNAL_GATES
```