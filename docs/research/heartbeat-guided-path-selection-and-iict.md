# Heartbeat-Guided Path Selection and IICT

Status: Ongoing research  
Claim type: Conceptual / proposed implementation model  
Creator: Rigel Randolph  
Originating ecosystem: StegVerse

## Overview

Heartbeat-guided path selection is an ongoing StegVerse research direction connecting system heartbeat, ephemeral validity rotation, derived-state refresh, tetrahedron governance enforcement, factor-bound action recording, and Irreversibility-Inference Convergence Theory (IICT).

The working idea is that a governed AI ecosystem should not behave like a static repository that only acts when an external user pushes a commit or triggers validation. Instead, it should behave as a dynamic system that continuously maintains standing alongside human counterparts.

## Static Validation Failure

A static repository validates whatever state happens to be present at the time an external action occurs. This can produce stale-state failures:

```text
source state changes
-> derived hash remains frozen
-> expected corpus consumes stale value
-> downstream validation fails
```

This failure pattern is representative of a broader micro-node and repo-node issue. Any derived value, receipt, verifier output, or token can become stale if the system only reacts after external input instead of continuously maintaining state.

## System Heartbeat

The system heartbeat is the timing substrate of the ecosystem. It is not merely a liveness signal. It is the cadence by which the system coordinates ephemeral authority, token rotation, receipt freshness, derived-state refresh, and micro-node continuity.

The heartbeat may operate at a high frequency, potentially in the MHz range, to support refresh and successor preparation before expiration events occur.

## Ephemeral Validity Rotation

Short-lived tokens should not be revalidated at every consumption boundary. Rechecking every boundary would defeat the purpose of ephemeral tokens.

Instead, tokens are accepted during their declared validity window while the system heartbeat coordinates refresh and successor preparation before expiry.

A validity-window object may include:

```text
valid_from
expires_at
refresh_after
refresh_deadline
successor_required
successor_token_ref
rotation_receipt
```

Transition states include:

```text
TOKEN_VALID -> CONSUME
TOKEN_NEAR_EXPIRY -> REFRESH_IN_PARALLEL + CONTINUE
TOKEN_REFRESHED -> ROTATE + RECORD
TOKEN_EXPIRED_WITH_SUCCESSOR_READY -> CONSUME_SUCCESSOR
TOKEN_EXPIRED_WITHOUT_SUCCESSOR -> FAIL_CLOSED
TOKEN_REVOKED_OR_CONFLICTED -> FAIL_CLOSED
TOKEN_STATUS_UNKNOWN -> QUARANTINE_OR_RECHECK
```

## Derived-State Refresh

Derived-state artifacts behave differently from ephemeral tokens.

Ephemeral tokens are validity-window objects. They remain acceptable until expiry unless revoked or conflicted.

Derived hashes and receipts are source-dependent bindings. They must be recomputed when source state changes.

The ecosystem should therefore distinguish:

```text
EPHEMERAL_VALIDITY_ROTATION
DERIVED_STATE_REFRESH
```

Derived-state refresh should occur before downstream consumption:

```text
source state changes
-> recompute derived value
-> record updated hash or receipt
-> recheck derived chain
-> allow downstream consumption only after derived state is current
```

## ΔHeartbeat as a Contributing Signal

`ΔHeartbeat` is the observed deviation from nominal heartbeat cadence:

```text
ΔHeartbeat = observed heartbeat interval - nominal heartbeat interval
```

`ΔHeartbeat` should not be used alone to make hard standing determinations. It is a contributing stress and coherency signal. Hard routing decisions require a broader system-state vector.

Relevant factors include:

```text
ΔHeartbeat
token refresh success rate
successor-token readiness
receipt latency
micro-node queue depth
verification delay
hash-refresh delay
rollback frequency
fail-closed frequency
resource saturation
network transport delay
state reconstruction latency
```

A possible interpretation model is:

```text
ΔHeartbeat alone -> STRESS_OBSERVED
ΔHeartbeat + corroborating degradation signals -> DEGRADED
ΔHeartbeat + missed validity or refresh boundary -> AUTHORITY_AT_RISK
ΔHeartbeat + failed refresh, rollback, or reconstruction -> FAIL_CLOSED
```

## Tetrahedron Governance Enforcement

The tetrahedron governance enforcement model provides the structural admissibility frame. One possible formulation uses:

```text
authority
policy
evidence
context
```

Another formulation may use:

```text
identity
delegation
state
execution boundary
```

Heartbeat and `ΔHeartbeat` are not replacements for these anchors. They are dynamic coherency signals used alongside them.

## Path Selection

The system may have several possible paths toward an admissible state. Some paths may be faster but less recoverable. Some may be slower but preserve authority. Some may increase proof depth, defer execution, reroute through an alternate node, shed load, or roll back.

Heartbeat-guided path selection asks:

```text
Which path keeps the system converging toward an admissible solution with the least loss of coherence, authority, recoverability, and continuity?
```

Example routing:

```text
low ΔHeartbeat + stable receipts
-> continue normal route

moderate ΔHeartbeat + token refresh pressure
-> pre-rotate tokens and continue

high ΔHeartbeat + queue growth
-> shed noncritical work and preserve core authority

high ΔHeartbeat + receipt latency
-> route through alternate node

high ΔHeartbeat + weak evidence currency
-> increase proof depth or pause execution

high ΔHeartbeat + missed refresh boundary
-> rollback, reconstruct, or fail closed
```

## Factor-Bound Transition Receipts

A governed transition should record not only that a transition occurred, but why a path was selected.

A transition receipt should preserve:

```text
prior state
proposed transition
available paths
selected path
authority condition
policy condition
evidence condition
context condition
heartbeat condition
ΔHeartbeat
token validity condition
successor-token readiness
receipt latency
queue depth
resource pressure
refresh status
rollback availability
recoverability profile
reason for path selection
reason rejected paths were not selected
final transition result
```

This allows later reconstruction of why the system considered the selected path admissible at the time of action.

## Relationship to IICT

Irreversibility-Inference Convergence Theory studies how a system minimizes the distance between its point of inference and the point of irreversibility.

Heartbeat-guided path selection provides an operational mechanism for that convergence:

```text
Inference window
-> system observes possible paths
-> heartbeat measures timing and coherency pressure
-> governance tetrahedron constrains admissible options
-> transition table selects path
-> micro-node acts or defers
-> receipt records contributing factors
-> system approaches or avoids irreversibility
```

Stale hashes, expiring tokens, delayed receipts, and heartbeat degradation all represent cases where the system may approach irreversibility with outdated inference.

The dynamic solution is:

```text
refresh inference before irreversibility,
or choose a path that delays, reroutes, rolls back, quarantines, or fails closed.
```

## Research Status

This page documents ongoing research. It does not claim that all described behavior is fully implemented.

The immediate implementation direction is to model this behavior in Standing-Proof-Engine, then scale the same transition logic to micro-node, repo-node, org-node, and master-records paths.

Open questions include:

1. How should heartbeat cadence be represented in receipts?
2. How should `ΔHeartbeat` be normalized across heterogeneous nodes?
3. What factors are required before `ΔHeartbeat` contributes to a hard route?
4. Which routing paths should exist at micro-node, repo-node, org-node, and master-record levels?
5. When should refresh occur automatically, and when should a stale condition only produce `REFRESH_REQUIRED`?
6. How should rejected paths be recorded without creating excessive receipt volume?
7. How should the transition table encode asymptotic path selection toward admissible solutions?
