---
title: W3C PROV governance compatibility procedure
---
# W3C PROV governance compatibility procedure

## Current state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_execution_observed: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
```

This procedure tests whether W3C PROV entity, activity, agent, derivation, attribution, delegation, source, and custody records can enter a StegVerse commitment path as bounded provenance evidence without inheriting truth, legitimacy, current authority, or consequence-binding permission.

## Evidence boundary

```text
provenance representation != proof of truth
represented delegation != current delegation
attribution != action authority
derivation != legitimacy
reconstructable chain != admissible chain
```

The current fixture contains declared PROV validation outputs. No pinned producer, serializer, store, validator, or query engine has been executed.

## Six required case families

| Family | Native posture | Expected StegVerse result |
|---|---|---|
| Positive alignment | Valid represented provenance with current independent governance conditions | `ALLOW` |
| Framework denial or negative result | PROV validation failure | `DENY` |
| Authority or delegation failure | Valid historical relation but current delegation revoked | `DENY` |
| Stale or missing evidence | Valid document with stale source evidence | `FAIL_CLOSED` |
| Malformed, undefined, or runtime error | Producer or validator error | `FAIL_CLOSED` |
| Semantic divergence guard | Valid represented relation applied outside requested action scope | `DENY` |

## Artifacts

```text
fixture: tests/fixtures/external-frameworks/w3c-prov-governance-compatibility-cases.v1.json
runner: scripts/run_w3c_prov_governance_compatibility.py
receipt: reports/external-frameworks/w3c-prov/w3c-prov-stegverse-governance-compatibility-receipt.json
status: static/external-frameworks/governance-compatibility-testing-status.v1.json
```

## Promotion gate

Promotion beyond `CONTRACT_AUTHORED_RUNTIME_PENDING` requires:

```text
pinned PROV implementation and serialization profile
source-to-PROV mapping and immutable source hashes
raw generated PROV document
raw validation or query transcript
custody and timestamp evidence
same-environment replay
fresh-runner replay
expected and observed StegVerse results matching
public machine-readable receipt
```

## Non-claims

This authored procedure does not certify W3C PROV, verify the truth of represented relations, create standing, grant execution authority, or establish general compatibility. It validates only the declared translation and StegVerse governance decision contract until native and replay evidence is attached.
