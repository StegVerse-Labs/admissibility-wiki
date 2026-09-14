# External Framework Endpoint Evidence Binding Mirror Handoff

Updated: 2026-09-13

Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Parent COSV: `50000000100000`
Reusable Task ID: `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`
Parent binding-registry handoff: `docs/external-frameworks/EXTERNAL_FRAMEWORK_ROUNDTRIP_BINDING_REGISTRY_MIRROR_HANDOFF.md`
Status: `ACTIVE / ENDPOINT EVIDENCE QUALIFICATION SOURCE IN PROGRESS`

## Purpose

Strengthen the canonical external-framework round-trip binding registry so a non-null `runtime_endpoint_ref` cannot be introduced as a bare URL or documentation-derived guess. An endpoint binding must carry explicit provenance sufficient to show where the current endpoint observation came from and when it was observed.

This handoff governs source-level binding qualification only. It creates no network traffic, runtime execution, credential authority, transition authority, user-verification authority, or foreign-framework authority.

## Required bound-endpoint fields

A bound endpoint overlay entry must include:

- `runtime_endpoint_ref`: the exact current endpoint reference supplied for the invocation path;
- `endpoint_evidence_ref`: a repository/external evidence reference that independently establishes the endpoint observation;
- `endpoint_observed_at`: an explicit observation timestamp or bounded observation identifier;
- `endpoint_evidence_class`: a bounded provenance class identifying how the endpoint was established;
- optional `counterpart_provenance` and `operation_class` inputs retained by the existing binding registry.

A bare string endpoint or an endpoint entry missing any required evidence field must fail closed.

## Authority boundary

Endpoint evidence makes a binding eligible to be considered by the reusable rollout. It does not prove endpoint authenticity, availability, authorization, admission, successful foreign execution, successful return, or standing. Those remain separate transition/runtime predicates.

Documentation URLs, standards URLs, source references, implementation-selection records, and non-executable runtime descriptors must not be promoted into runtime endpoint bindings.

## Completion boundary

Source completion requires the binding builder and checker to reject unqualified endpoints, retain all unbound registry entries unchanged, preserve zero authority/plan-only effects, pass the canonical Goal 5 validation chain, and merge.

## Next action

Implement evidence-qualified endpoint binding in the existing builder/checker and validate exact-head behavior. Do not populate any real framework endpoint unless current endpoint evidence is independently available.

## Manual work

None.
