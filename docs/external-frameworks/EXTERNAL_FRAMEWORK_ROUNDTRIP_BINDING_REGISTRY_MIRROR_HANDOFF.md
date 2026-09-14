# External Framework Round-Trip Binding Registry Mirror Handoff

Updated: 2026-09-13

Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Parent COSV: `50000000100000`
Reusable Task ID: `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`
Canonical reusable handoff: `StegVerse-Labs/.github/docs/EXTERNAL_FRAMEWORK_ROUNDTRIP_ROLLOUT_MIRROR_HANDOFF.md`
Canonical framework registry: `docs/external-frameworks/index.json`
Status: `HANDOFF ESTABLISHED / BINDING REGISTRY SOURCE PENDING`

## Purpose

Provide one canonical admissibility-wiki-owned binding registry that projects every external-framework registry entry into the reusable StegVerse external-framework round-trip model without creating one Goal Task, transport stack, scheduler, credential route, or authority plane per framework.

The binding registry is coordination data only. It does not make a framework runnable, prove endpoint authenticity, admit a transition, authorize a foreign verdict, or execute network traffic.

## Design

The canonical compatibility registry remains `docs/external-frameworks/index.json`. This continuation adds a derived binding surface with one row for every framework identity in that registry. Each row may carry an explicit `runtime_endpoint_ref` only when independently supplied and may otherwise remain unbound.

The binding surface is intended to feed the merged `.github` registry-wide planner `scripts/plan_external_framework_registry_rollout.py`. It must not duplicate the planner's eligibility logic. Admissibility-wiki owns framework identity/source metadata and explicit endpoint-binding inputs; the reusable rollout resolver owns round-trip eligibility classification.

## Required invariants

- every canonical external-framework registry entry resolves to exactly one binding row;
- no binding row exists for an unknown framework id;
- missing endpoint binding is an explicit null/unbound state, not an inferred endpoint;
- endpoint bindings do not confer authority or prove availability/authenticity;
- source-blocked frameworks remain source-blocked regardless of endpoint text;
- no direct framework-specific bypass around Interlock/InTr is introduced;
- no per-framework Goal Task is created when the reusable invocation is sufficient;
- GitHub/source/CI authority effect remains `NONE`.

## Planned source surfaces

- `scripts/build_external_framework_roundtrip_bindings.py`
- `tests/test_external_framework_roundtrip_bindings.py`
- `data/external-framework-roundtrip-bindings.example.json`
- this handoff

## Completion boundary

This continuation is source-complete only when the builder deterministically projects all canonical framework identities, validates optional endpoint overlays, preserves unbound rows fail-closed, emits no execution authority, passes repository validation, and merges.

Runtime transition completion remains outside this artifact. Actual framework execution occurs only through the reusable rollout and its existing Interlock/InTr-governed component composition.

## Next action

Implement the deterministic builder and tests, then validate the exact branch head. Do not create per-framework tasks or transports while doing so.

## Manual work

None.
