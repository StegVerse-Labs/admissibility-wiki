# External Framework Endpoint Evidence Binding Mirror Handoff

Updated: 2026-09-13

Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Parent COSV: `50000000100000`
Reusable Task ID: `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`
Parent binding-registry handoff: `docs/external-frameworks/EXTERNAL_FRAMEWORK_ROUNDTRIP_BINDING_REGISTRY_MIRROR_HANDOFF.md`
Status: `SOURCE STAGED / EXACT-HEAD VALIDATION PENDING / REAL ENDPOINT OVERLAY REMAINS EMPTY`

## Purpose

Strengthen the canonical external-framework round-trip binding registry so a non-null `runtime_endpoint_ref` cannot be introduced as a bare URL or documentation-derived guess. A bound endpoint must carry explicit provenance sufficient to show where the current endpoint observation came from and when it was observed.

This handoff governs source-level binding qualification only. It creates no network traffic, runtime execution, credential authority, transition authority, user-verification authority, or foreign-framework authority.

## Required bound-endpoint fields

A bound endpoint overlay entry must include:

- `runtime_endpoint_ref`: the exact current endpoint reference supplied for the invocation path;
- `endpoint_evidence_ref`: a repository/external evidence reference that independently establishes the endpoint observation;
- `endpoint_observed_at`: an explicit observation timestamp or bounded observation identifier;
- `endpoint_evidence_class`: a bounded provenance class identifying how the endpoint was established;
- optional `counterpart_provenance` and `operation_class` inputs retained by the existing binding registry.

A bare string endpoint, an endpoint entry missing any required evidence field, or endpoint evidence metadata without an endpoint must fail closed.

## Staged source

`build_external_framework_roundtrip_bindings.py` now:

- rejects bare string endpoint overlays;
- requires all three endpoint evidence fields whenever `runtime_endpoint_ref` is non-null;
- rejects orphan endpoint-evidence metadata when no endpoint is present;
- retains unbound rows with all endpoint evidence fields null;
- emits `EVIDENCE_QUALIFIED_ENDPOINT_BOUND` only for evidence-qualified endpoint rows;
- records explicit semantics that documentation/source URLs may not be inferred as runtime endpoints;
- preserves `NONE_COORDINATION_ONLY` authority effect and `NONE_PLAN_ONLY` transition effect.

`check_external_framework_roundtrip_bindings.py` now includes positive evidence-qualified binding coverage and negative controls for bare endpoint strings, missing evidence metadata, orphan evidence metadata, unknown framework ids, and duplicate registry identities.

The live `data/external-framework-roundtrip-endpoints.json` overlay remains empty. No real framework endpoint has been asserted by this source work.

## Authority boundary

Endpoint evidence makes a binding eligible to be considered by the reusable rollout. It does not prove endpoint authenticity, availability, authorization, admission, successful foreign execution, successful return, or standing. Those remain separate transition/runtime predicates.

Documentation URLs, standards URLs, source references, implementation-selection records, and non-executable runtime descriptors must not be promoted into runtime endpoint bindings.

## Completion boundary

Source completion requires the staged builder/checker behavior to pass the canonical validation chain and merge. Runtime endpoint establishment remains a separate evidence-producing activity, and each real endpoint remains independently fail-closed until that evidence exists.

## Next action

Run exact-head validation. If green, merge this evidence-qualification contract. Then admit real endpoint bindings one at a time only from current observed endpoint evidence and feed them through the reusable registry-wide planner.

## Manual work

None.
