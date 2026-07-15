---
title: SPIFFE/SPIRE Governance Compatibility Procedure
---

# SPIFFE/SPIRE Governance Compatibility Procedure

## Current posture

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native_execution_observed: false
governance_compatibility_observed: false
```

This procedure tests where verified workload identity can enter StegVerse governance and where identity must remain separate from delegation, standing, admissibility, and execution authority.

## Compatibility hypothesis

```text
SPIFFE ID + current SVID + valid attestation + current trust bundle
  -> workload identity evidence
  -> actor field in a governed transition
  -> not action-level authority
```

StegVerse separately evaluates current delegation, policy, evidence freshness, scope, recoverability, and execution context.

## Six required cases

| Family | Native identity result | Expected StegVerse result |
|---|---|---|
| Positive alignment | Verified | `ALLOW` only when every independent commit-time condition is satisfied |
| Framework denial | Unverified | `DENY` |
| Authority failure | Verified, delegation revoked | `DENY` |
| Stale evidence | Expired SVID or stale bundle | `FAIL_CLOSED` |
| Framework error | Attestation or verification error | `FAIL_CLOSED` |
| Semantic divergence | Verified identity, target outside scope | `DENY` |

## Executable contract

```text
fixture: tests/fixtures/external-frameworks/spiffe-spire-governance-compatibility-cases.v1.json
runner: scripts/run_spiffe_spire_governance_compatibility.py
receipt: reports/external-frameworks/spiffe-spire/spiffe-spire-stegverse-governance-compatibility-receipt.json
```

The current runner evaluates predeclared identity results. It validates only the StegVerse translation contract.

## Runtime evidence still required

Promotion beyond contract-authored status requires:

- a pinned SPIRE release and plugin set;
- trust-domain and registration configuration;
- attestation inputs and raw outputs;
- issued SVID and trust-bundle hashes;
- expiry and rotation timestamps;
- verification commands and results;
- same-environment replay;
- fresh-runner replay;
- publication of the resulting bounded receipt.

## Non-claims

Identity is not authority. Attestation is not admissibility. A successful contract evaluation is not observed SPIRE behavior, certification, production integration, general compatibility, or permission to execute.
