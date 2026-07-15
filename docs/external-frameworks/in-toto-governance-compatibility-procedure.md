---
title: in-toto Governance Compatibility Procedure
---
# in-toto Governance Compatibility Procedure

## Current state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_execution_observed: false
stegverse_governance_compatibility_observed: false
case_count: 6
```

This procedure tests whether an in-toto verification result can enter StegVerse as bounded provenance evidence without being mistaken for deployment permission, current delegation, admissibility, certification, or general compatibility.

## Contract artifacts

```text
fixture: tests/fixtures/external-frameworks/in-toto-governance-compatibility-cases.v1.json
runner: scripts/run_in_toto_governance_compatibility.py
receipt: reports/external-frameworks/in-toto/in-toto-stegverse-governance-compatibility-receipt.json
```

## Required case families

1. Valid layout and links with all StegVerse commit-time conditions current.
2. Native verification denial.
3. Historical provenance remains valid while current delegation is revoked.
4. Stale layout, links, keys, or evidence.
5. Malformed input or verifier/runtime error.
6. Verified provenance for an artifact whose requested deployment action is outside current scope.

## Translation boundary

```text
in-toto verification
    -> provenance and process evidence
    -> not deployment authority
    -> StegVerse independently evaluates current delegation,
       policy, target scope, freshness, recoverability,
       execution context, and consequence authority
```

## Evidence still required

A compatibility result cannot be promoted until the repository has a pinned in-toto implementation, immutable implementation identity, a signed layout and link bundle, verification keys, raw verifier output, timestamps, replay commands, same-environment replay, fresh-runner replay, and the published bounded receipt.

## Non-claims

The authored translation fixture is not an observed in-toto execution. A passing simulated contract does not certify in-toto, prove artifact safety, authorize deployment, establish current delegation, create standing, or establish general compatibility.
