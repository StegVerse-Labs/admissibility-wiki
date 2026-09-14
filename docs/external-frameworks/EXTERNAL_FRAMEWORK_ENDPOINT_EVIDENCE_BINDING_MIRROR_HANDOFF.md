# External Framework Endpoint Evidence Binding Mirror Handoff

Updated: 2026-09-14

Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Parent COSV: `50000000100000`
Reusable Task ID: `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`
Parent binding-registry handoff: `docs/external-frameworks/EXTERNAL_FRAMEWORK_ROUNDTRIP_BINDING_REGISTRY_MIRROR_HANDOFF.md`
Status: `SOURCE COMPLETE / EXACT-HEAD VALIDATION GREEN / MERGED / REAL ENDPOINT OVERLAY REMAINS EMPTY`

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

## Merged source

`build_external_framework_roundtrip_bindings.py`:

- rejects bare string endpoint overlays;
- requires all three endpoint evidence fields whenever `runtime_endpoint_ref` is non-null;
- rejects orphan endpoint-evidence metadata when no endpoint is present;
- retains unbound rows with all endpoint evidence fields null;
- emits `EVIDENCE_QUALIFIED_ENDPOINT_BOUND` only for evidence-qualified endpoint rows;
- records explicit semantics that documentation/source URLs may not be inferred as runtime endpoints;
- preserves `NONE_COORDINATION_ONLY` authority effect and `NONE_PLAN_ONLY` transition effect.

`check_external_framework_roundtrip_bindings.py` includes positive evidence-qualified binding coverage and negative controls for bare endpoint strings, missing evidence metadata, orphan evidence metadata, unknown framework ids, and duplicate registry identities.

The live `data/external-framework-roundtrip-endpoints.json` overlay remains empty. No real framework endpoint has been asserted by this source work.

## Validation and merge evidence

```text
PR: StegVerse-Labs/admissibility-wiki#140
exact head: abae06cada9252324d303fb6f46fc8f0414ae80c
Validate chain continuation: 34798422252 SUCCESS (run 4862)
merge: 5d3baaeb3175a06ff046826df9e10a2958fb1fe2
```

This closes only the source-level endpoint-evidence qualification requirement. It does not establish any runtime endpoint, endpoint authenticity, endpoint availability, foreign-framework execution, return transition, or final standing.

## Authority boundary

Endpoint evidence makes a binding eligible to be considered by the reusable rollout. It does not prove endpoint authenticity, availability, authorization, admission, successful foreign execution, successful return, or standing. Those remain separate transition/runtime predicates.

Documentation URLs, standards URLs, source references, implementation-selection records, and non-executable runtime descriptors must not be promoted into runtime endpoint bindings.

## Completion boundary

Source completion is satisfied for this contract by the exact-head validation and merge above. Runtime endpoint establishment remains a separate evidence-producing activity, and each real endpoint remains independently fail-closed until that evidence exists.

## Next action

Keep the live endpoint overlay empty unless a current independently observed runtime endpoint maps to an exact canonical framework identity. Feed only evidence-qualified bindings through the existing registry-wide reusable rollout planner. Frameworks without a qualified endpoint remain explicitly non-runtime-eligible rather than receiving inferred endpoints.

## Manual work

None.
