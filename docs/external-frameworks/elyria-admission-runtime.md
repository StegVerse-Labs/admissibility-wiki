---
title: Elyria Admission Runtime
---
# Elyria Admission Runtime

## Evidence posture

```text
evidence_class: SOURCE_REVIEWED
source_version: v0.8.2-public
runtime_endpoint_binding: UNBOUND_NO_RUNTIME_ENDPOINT_REF
authentic_two_way_stegverse_roundtrip: not observed
execution_authority_claim_allowed: false
```

## Published scope

Elyria Admission Runtime is a public buyer-review consequence-admission runtime from Samantha Revita / Elyria Systems. The verified public release describes deterministic movement assessment, structured evidence gates, signed receipts, replay verification, exposure graphing, no-bind/proof surfaces, and proof export.

Canonical public source: https://github.com/Kamanaka5502/elyria-admission-runtime/releases/tag/v0.8.2-public

The public repository documents `POST /movements/assess` as the movement-assessment API path. Its reviewer quickstart and container paths are local execution instructions and are **not** treated as callable public runtime endpoints.

## Relationship to StegVerse

```text
StegVerse manifested operation
  -> governed SDK processing
  -> Interlock/InTr egress
  -> evidence-qualified Elyria runtime endpoint binding
  -> Elyria movement assessment
  -> foreign verdict + receipt
  -> Master Records custody/readback
  -> SDK return
```

Elyria's verdict is preserved as a foreign-framework observation. It does not become StegVerse admission, execution authority, standing, or custody authority.

## Runtime round-trip binding

Canonical framework identity:

```text
framework_id: elyria-admission-runtime
operation_class: RUNTIME_ROUNDTRIP
adapter_operation: movement_assessment
runtime_endpoint_ref: null
binding_state: UNBOUND_NO_RUNTIME_ENDPOINT_REF
```

The canonical endpoint overlay is `data/external-framework-roundtrip-endpoints.json`. A future endpoint binding must include:

```text
runtime_endpoint_ref
endpoint_evidence_ref
endpoint_observed_at
endpoint_evidence_class
```

Source, release, documentation, localhost, and container URLs cannot substitute for independently observed runtime endpoint evidence.

## Current boundary

```text
EVIDENCE_QUALIFIED_ELYRIA_RUNTIME_ENDPOINT_NOT_AVAILABLE
```

No current independently observed callable Elyria runtime endpoint has been established. Therefore no authentic two-way StegVerse/Elyria round trip or Master Records custody of such a round trip is claimed.

## Non-claims

Elyria inclusion is not certification, endorsement, equivalence, production certification, StegVerse admission, execution authority, or proof of live endpoint availability.
