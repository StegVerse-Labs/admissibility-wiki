---
title: SLSA Governance Compatibility Procedure
---
# SLSA Governance Compatibility Procedure

## Current posture

```text
framework: SLSA v1.2
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
native provenance producer selected: no
native verifier selected: no
native verification observed: no
fresh-runner replay observed: no
StegVerse governance compatibility observed: no
```

This procedure tests whether a SLSA provenance-verification result can enter a StegVerse governed transition as bounded supply-chain evidence without being mistaken for deployment authority, runtime permission, or complete admissibility.

## Compatibility path

```text
SLSA provenance verification
  -> artifact, builder, source, and build evidence
  -> translation into a Commitment Candidate
  -> independent StegVerse commit-time evaluation
  -> ALLOW, DENY, ESCALATE, or FAIL_CLOSED
```

A passing SLSA verification result is necessary evidence only for the declared provenance claim. StegVerse still evaluates current delegation, policy, evidence freshness, target-action scope, recoverability, execution context, and consequence authority.

## Authored test families

| Family | Native posture | Governed expectation |
|---|---|---|
| Positive alignment | Provenance verifies and every commit-time condition is current. | `ALLOW` |
| Framework denial | Provenance verification fails. | `DENY` |
| Authority failure | Provenance verifies but deployer delegation is revoked. | `DENY` |
| Stale or missing evidence | Provenance is incomplete or stale. | `FAIL_CLOSED` |
| Runtime error | Verifier returns an error or undefined result. | `FAIL_CLOSED` |
| Semantic divergence | Provenance verifies but the requested deployment is outside scope. | `DENY` |

## Machine-readable procedure

```text
fixture: tests/fixtures/external-frameworks/slsa-governance-compatibility-cases.v1.json
runner: scripts/run_slsa_governance_compatibility.py
result receipt: reports/external-frameworks/slsa/slsa-stegverse-governance-compatibility-receipt.json
status ledger: static/external-frameworks/governance-compatibility-testing-status.v1.json
```

## Execution sequence required for promotion

1. Select and pin one SLSA-compatible provenance producer and verifier.
2. Record implementation versions, source commits, package or binary hashes, and runtime environment.
3. Generate or attach a provenance bundle and bind it to an immutable artifact digest.
4. Capture raw verifier output for positive, negative, stale, malformed, and scope-divergence cases.
5. Run the StegVerse translation evaluator against those captured native outputs.
6. Replay the native verification and governed evaluation on a fresh runner.
7. Publish the complete receipt and update the status ledger only from observed evidence.

## Current limitation

The authored runner currently validates the declared translation and StegVerse decision contract using predeclared SLSA verification outcomes. It does not execute a SLSA producer or verifier and therefore cannot establish native behavior or bounded compatibility.

## Non-claims

```text
SLSA verification != deployment authority
trusted builder != authorized deployer
provenance completeness != runtime safety
translation-contract pass != native framework execution
compatibility receipt != certification or execution authority
```

Publication of this procedure creates no standing, deployment permission, release authority, certification, or general compatibility claim.
