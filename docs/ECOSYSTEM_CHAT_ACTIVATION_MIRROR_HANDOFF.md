# Ecosystem Chat Activation Projection Mirror Handoff

## Source of truth

This file is the goal-specific continuation source for the Ecosystem Chat activation projection in `StegVerse-Labs/admissibility-wiki`.

## Correct repository map

```text
Source: StegVerse-Labs/Site
Destination: StegVerse-Labs/admissibility-wiki
Guardian peer: StegVerse-002/stegguardian-wiki
Removed nonexistent target: StegVerse-Labs/Sit
```

`StegVerse-Labs/Site` is the existing Site repository and is not a separate downstream destination from itself.

## Installed consumer

```text
scripts/check_ecosystem_chat_activation_projection.py
static/status/ecosystem-chat-activation-status.json
scripts/check_admissibility_automation_handoff.py
```

The consumer is invoked through the existing canonical validation chain. It attempts to refresh the hash-bound activation state and propagation packet from Site. If the source is temporarily unavailable, it validates the last checked-in fail-closed projection and creates no user task.

## States

```text
ACTIVATION_EVIDENCE_PENDING
VERIFIED_ACTIVATION_PROJECTED
```

The verified state requires a valid Site state hash, propagation packet hash, packet-to-state binding, explicit destination declaration, `ACTIVATION_COMPLETE`, and `READY_FOR_DOWNSTREAM_INGESTION`.

## Authority boundary

Projection is documentation evidence only. It grants no activation, release, publication, execution, admissibility, standing, or custody authority.

## Remaining work

```text
1. Observe canonical validation containing the consumer.
2. Allow the canonical workflow to refresh the projection automatically.
3. Observe VERIFIED_ACTIVATION_PROJECTED only after Site emits verified activation evidence.
4. Preserve the public projection through the existing Pages build.
```

Manual user action required: false.

## Archive readiness

This handoff and the repository implementation preserve all continuation state for this projection goal.
