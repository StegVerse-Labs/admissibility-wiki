---
title: Guardrails AI Governance Compatibility Procedure
---
# Guardrails AI Governance Compatibility Procedure

## Status

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_runtime_observed: false
governance_compatibility_observed: false
independent_reproduction: false
execution_authority_created: false
```

This procedure defines how a Guardrails AI validator result may enter StegVerse as bounded content-safety evidence without becoming execution authority.

## Required evidence packet

A runtime-backed test requires all of the following:

```text
pinned Guardrails AI package and commit or release
pinned validator identifiers and versions
pinned model, prompt, thresholds, and guard configuration
shared input and output vectors
raw validator results
correction or reask trace
runtime configuration and timestamps
immutable hashes
fresh-runner replay
```

Until that packet exists, the evaluator remains a contract simulation only.

## Six governed case families

| Family | Native posture | Expected StegVerse result | Boundary tested |
|---|---|---|---|
| positive alignment | validator PASS | ALLOW | Pass is usable only when every independent commit-time condition also holds. |
| framework denial or negative result | validator BLOCK | DENY | A configured block enters as negative safety evidence. |
| authority or delegation failure | PASS with stale delegation | DENY | Validator success does not restore authority. |
| stale or missing evidence | PASS from stale evidence | FAIL_CLOSED | Old validators, thresholds, models, or traces cannot support a current transition. |
| malformed, undefined, or runtime error | ERROR | FAIL_CLOSED | Exceptions, missing validators, and timeouts cannot authorize fallback execution. |
| semantic divergence guard | PASS outside target scope | DENY | Content validation cannot be generalized into target or consequence authority. |

Machine-readable fixture:

```text
tests/fixtures/external-frameworks/guardrails-ai-governance-compatibility-cases.v1.json
```

Deterministic contract evaluator:

```text
python scripts/run_guardrails_ai_governance_compatibility.py
```

Expected receipt path:

```text
reports/external-frameworks/guardrails-ai/guardrails-ai-stegverse-governance-compatibility-receipt.json
```

## Translation boundary

```text
validator pass != StegVerse ALLOW
validator block != certification
correction or reask != authorized transition
content safety evidence != actor authority
contract simulation != native runtime observation
```

Guardrails AI results may contribute evidence about configured content checks. StegVerse still evaluates identity, delegation, policy currency, evidence freshness, target scope, recoverability, execution context, and consequence authority independently.

## Promotion rule

The ledger may advance from `CONTRACT_AUTHORED_RUNTIME_PENDING` only after a pinned native execution produces inspectable raw traces, all six case families are replayed, and the resulting receipt is directly observed. A matching simulation alone cannot promote compatibility status.

## Non-claims

This procedure does not certify Guardrails AI, validate every validator, establish general compatibility, create standing, or authorize execution. Publication does not create authority.
