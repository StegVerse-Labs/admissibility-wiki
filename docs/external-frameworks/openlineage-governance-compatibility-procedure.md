---
title: OpenLineage Governance Compatibility Procedure
---
# OpenLineage Governance Compatibility Procedure

## Current state

```text
framework_id: openlineage
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_execution_observed: false
stegverse_governance_compatibility_observed: false
case_count: 6
```

This procedure tests whether OpenLineage run, job, dataset, event, facet, custody, and freshness records can enter StegVerse as reconstruction evidence without being mistaken for verified truth, causal proof, current delegation, or consequence-binding authority.

## Test contract

```text
fixture: tests/fixtures/external-frameworks/openlineage-governance-compatibility-cases.v1.json
evaluator: scripts/run_openlineage_governance_compatibility.py
result receipt: reports/external-frameworks/openlineage/openlineage-stegverse-governance-compatibility-receipt.json
```

## Required case families

| Family | OpenLineage-side condition | Expected StegVerse result |
|---|---|---|
| Positive alignment | Authentic, ordered, fresh, reconstructable lineage with current delegation and scope | `ALLOW` |
| Framework negative result | Rejected or invalid lineage evidence | `DENY` |
| Authority or delegation failure | Valid lineage but revoked or absent action authority | `DENY` |
| Stale or missing evidence | Event stream no longer represents current pipeline state | `FAIL_CLOSED` |
| Malformed or runtime error | Producer, transport, parser, consumer, or schema failure | `FAIL_CLOSED` |
| Semantic divergence guard | Complete lineage is outside the requested action or target scope | `DENY` |

## Translation boundary

```text
OpenLineage events
    -> lineage and reconstruction evidence
    -> not independently verified truth
    -> not causal proof
    -> not current delegation
    -> not governance authority
    -> StegVerse independently evaluates policy, identity,
       delegation, freshness, action scope, recoverability,
       execution context, and consequence authority
```

## Runtime evidence still required

Promotion requires a pinned producer, transport, schema, event stream, consumer, raw emitted and consumed records, ordering and custody evidence, timestamps, same-environment replay, fresh-runner replay, and independent reproduction. Until those artifacts exist, the evaluator validates only the declared translation and decision contract.

## Replay command

```bash
python scripts/run_openlineage_governance_compatibility.py
```

## Non-claims

A passing fixture does not prove a real OpenLineage integration, certify a producer or consumer, establish event truth, grant standing, create execution authority, or support a general compatibility claim.
