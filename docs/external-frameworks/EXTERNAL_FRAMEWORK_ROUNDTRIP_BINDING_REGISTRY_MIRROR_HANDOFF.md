# External Framework Round-Trip Binding Registry Mirror Handoff

Updated: 2026-09-13

Parent Goal Task ID: `MIR-CONNECTION-ROUNDTRIP-TECHNICAL-GUIDE-001`
Parent COSV: `50000000100000`
Reusable Task ID: `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`
Canonical reusable handoff: `StegVerse-Labs/.github/docs/EXTERNAL_FRAMEWORK_ROUNDTRIP_ROLLOUT_MIRROR_HANDOFF.md`
Canonical framework registry: `docs/external-frameworks/index.json`
Status: `BINDING REGISTRY SOURCE STAGED / GOAL 5 AGGREGATE CHECK WIRED / EXACT-HEAD VALIDATION PENDING`

## Purpose

Provide one canonical admissibility-wiki-owned binding registry that projects every external-framework registry entry into the reusable StegVerse external-framework round-trip model without creating one Goal Task, transport stack, scheduler, credential route, or authority plane per framework.

The binding registry is coordination data only. It does not make a framework runnable, prove endpoint authenticity, admit a transition, authorize a foreign verdict, or execute network traffic.

## Design

The canonical compatibility registry remains `docs/external-frameworks/index.json`. The staged binding builder projects one row for every framework identity in that registry. Each row may carry an explicit `runtime_endpoint_ref` only when independently supplied and otherwise remains `UNBOUND_NO_RUNTIME_ENDPOINT_REF`.

The binding surface feeds the merged `.github` registry-wide planner `scripts/plan_external_framework_registry_rollout.py`. It deliberately does not duplicate that planner's source/manifest/runtime eligibility logic. Admissibility-wiki owns framework identity/source metadata and explicit endpoint-binding inputs; the reusable rollout resolver owns round-trip eligibility classification.

The existing admissibility-wiki implementation readiness/execution-plan machinery remains intact. Those plans cover implementation-selection/job-materialization readiness for their bounded candidate set. This binding registry is broader and orthogonal: it covers every canonical external-framework identity and only records explicit reusable-round-trip endpoint binding state. It does not replace or promote the existing execution plans.

## Required invariants

- every canonical external-framework registry entry resolves to exactly one binding row;
- no binding row exists for an unknown framework id;
- missing endpoint binding is an explicit null/unbound state, not an inferred endpoint;
- endpoint bindings do not confer authority or prove availability/authenticity;
- source-blocked frameworks remain source-blocked regardless of endpoint text;
- no direct framework-specific bypass around Interlock/InTr is introduced;
- no per-framework Goal Task is created when the reusable invocation is sufficient;
- GitHub/source/CI authority effect remains `NONE`.

## Staged source surfaces

- `scripts/build_external_framework_roundtrip_bindings.py`
- `scripts/check_external_framework_roundtrip_bindings.py`
- `data/external-framework-roundtrip-endpoints.json`
- `scripts/check_goal5_external_frameworks_all.py` integration
- this handoff

The endpoint overlay is intentionally empty at source establishment. Empty means no framework endpoint has been asserted merely from documentation or source URLs. The builder still projects all canonical framework identities into explicit unbound rows, giving one managed connection slot per framework without inventing endpoint authority.

The checker validates the live canonical registry projection plus negative controls for unknown overlay framework ids and duplicate registry identities. It also verifies exact identity/order coverage, bound/unbound count reconciliation, plan-only transition effect, and zero authority effect.

## Completion boundary

This continuation is source-complete only when the builder deterministically projects all canonical framework identities, validates optional endpoint overlays, preserves unbound rows fail-closed, emits no execution authority, passes repository validation including the Goal 5 aggregate path, and merges.

Runtime transition completion remains outside this artifact. Actual framework execution occurs only through the reusable rollout and its existing Interlock/InTr-governed component composition.

## Next action

Run exact-head repository validation. If green, merge this binding-registry source. After merge, populate endpoint bindings only from separately established current endpoint evidence and feed the resulting binding surface to `RT-EXTERNAL-FRAMEWORK-ROUNDTRIP-ROLLOUT-001`; do not create per-framework tasks or transports.

## Manual work

None.
