---
title: ASRO Governance Compatibility Procedure
---

# ASRO Governance Compatibility Procedure

## Purpose

This procedure tests whether ASRO host, edge, verifier, and governance-state attestation evidence can enter StegVerse review without converting attestation reconciliation into action-level authority.

## Current evidence state

```text
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
source_reviewed: true
repository_reference_present: true
native_runtime_execution_observed: false
fresh_runner_replay_observed: false
stegverse_governance_compatibility_observed: false
simulation_only: true
```

The ASRO crosswalk and public repository reference establish vocabulary and source posture. They do not establish a pinned release, captured host or edge agent output, verifier execution, deterministic replay, or independent reproduction.

## Contract artifacts

```text
fixture: tests/fixtures/external-frameworks/asro-governance-compatibility-cases.v1.json
evaluator: scripts/run_asro_governance_compatibility.py
expected receipt: reports/external-frameworks/asro/asro-stegverse-governance-compatibility-receipt.json
```

## Required case families

| Family | ASRO evidence | Expected StegVerse decision |
|---|---|---|
| Positive alignment | Reconciled attestation and all current commit-time conditions | `ALLOW` |
| Framework negative result | Host/edge governance-state mismatch | `DENY / GOVERNANCE_STATE_MISMATCH` |
| Authority or delegation failure | Reconciled attestation with expired delegation | `DENY / AUTHORITY_DRIFT` |
| Stale or missing evidence | Stale attestation packet | `FAIL_CLOSED / STALE_ATTESTATION_EVIDENCE` |
| Malformed or runtime error | Verifier error | `FAIL_CLOSED / ATTESTATION_VERIFIER_ERROR` |
| Semantic divergence guard | Reconciled summary with inconsistent witness evidence | `DENY / SELECTIVE_ATTESTATION_DIVERGENCE` |

## Translation boundary

```text
host measurement -> operator-side governance-state evidence
edge witnessing -> dependent-party witness evidence
verifier reconciliation -> comparison and discrepancy evidence
governance-state change record -> drift and commit-time validity evidence
selective-attestation detection -> evidence-sufficiency and fail-closed evidence
```

None of those artifacts independently establishes current delegation, target permission, consequence authority, recoverability, transition admissibility, release authority, or execution permission.

## Runtime completion requirements

Bounded runtime compatibility may be promoted only after attaching:

```text
- a pinned ASRO release or commit
- pinned host, edge, and verifier components
- versioned governance-state declarations
- shared positive, mismatch, stale, malformed, and selective-attestation vectors
- raw host, edge, and verifier outputs
- component, configuration, vector, and output hashes
- exact replay commands
- a fresh-runner receipt
- an independently inspected StegVerse translation receipt
```

## Non-claims

Attestation reconciliation is not StegVerse `ALLOW`. Governance-state continuity is not current delegation. Independent witnessing is not action authority. This authored simulation is not native runtime observation, independent reproduction, certification, standing, release authority, or execution authority.
