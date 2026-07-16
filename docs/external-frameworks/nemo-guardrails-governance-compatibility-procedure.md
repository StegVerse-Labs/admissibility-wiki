---
title: NeMo Guardrails Governance Compatibility Procedure
---
# NeMo Guardrails Governance Compatibility Procedure

## Status

```text
framework_id: nemo-guardrails
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_runtime_execution_observed: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
simulation_only: true
```

This procedure defines the bounded translation test between NeMo Guardrails rail outcomes and StegVerse commit-time governance. It does not claim that NeMo Guardrails has been executed, integrated, independently reproduced, certified, or granted execution authority.

## Native evidence boundary

NeMo Guardrails can produce rail pass, rail block, intervention, configuration, retrieval, model-call, tool-call, and runtime-error evidence. Those outputs remain evidence. They do not silently become StegVerse `ALLOW`, `DENY`, standing, delegation, target permission, or consequence authority.

```text
rail pass != StegVerse ALLOW
rail block != universal policy denial
configured rail != legitimate current policy
successful tool flow != current consequence authority
runtime trace != transition admissibility
```

## Shared contract

Fixture:

`tests/fixtures/external-frameworks/nemo-guardrails-governance-compatibility-cases.v1.json`

Evaluator:

`scripts/run_nemo_guardrails_governance_compatibility.py`

Expected receipt:

`reports/external-frameworks/nemo-guardrails/nemo-guardrails-stegverse-governance-compatibility-receipt.json`

The evaluator is deterministic and simulation-only until pinned native artifacts are attached.

## Required six case families

| Family | Native condition | Expected StegVerse result | Boundary tested |
|---|---|---|---|
| Positive alignment | Rail passes and every commit-time condition remains current | `ALLOW` | Native evidence plus independent authority conditions |
| Framework negative | Rail blocks the interaction | `DENY` | Negative rail evidence is preserved |
| Authority failure | Rail passes but delegation is no longer current | `DENY / AUTHORITY_DRIFT` | Rail pass cannot restore authority |
| Stale evidence | Rail passes but rail/model/retrieval/tool evidence is stale | `FAIL_CLOSED / STALE_EVIDENCE` | Freshness remains independent |
| Runtime error | Rail execution is malformed, missing, or errors | `FAIL_CLOSED / RAIL_RUNTIME_ERROR` | Runtime uncertainty cannot authorize |
| Semantic divergence | Rail passes but the target is outside current scope | `DENY / SCOPE_DIVERGENCE` | Rail pass is not commit-time permission |

## Native runtime packet required for promotion

Promotion beyond authored simulation requires one pinned packet containing:

```text
NeMo Guardrails package version and hash
rail and Colang configuration with hashes
model, prompt, retrieval corpus, and tool identities
shared interaction vectors
raw rail and intervention event traces
runtime parameters and timestamps
predeclared expected StegVerse mappings
same-environment replay receipt
fresh-runner replay receipt
independent implementation or provider evidence, when claimed
```

## Failure posture

Missing configuration, unknown flow, malformed event, runtime exception, stale evidence, scope divergence, authority drift, and unrecoverable intervention state remain fail-closed or denied according to the authored fixture. No missing native output may be inferred as a pass.

## Non-claims

A successful six-case simulation validates only the authored translation logic. It does not establish native execution, production integration, general compatibility, safety completeness, certification, standing, deployment authority, or permission for a specific transition to bind consequence.
