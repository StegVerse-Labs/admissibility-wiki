---
title: Sigstore Governance Compatibility Procedure
---
# Sigstore Governance Compatibility Procedure

## Current posture

```text
framework: Sigstore
contract_state: CONTRACT_AUTHORED_RUNTIME_PENDING
pinned client: none
signed artifact fixture: none
native verification observed: no
fresh-runner replay observed: no
StegVerse governance compatibility observed: no
```

This procedure tests whether Sigstore signature, certificate-identity, and transparency evidence can enter a StegVerse governed transition without being mistaken for action authority or admissibility.

## Compatibility path

```text
Sigstore verification
  -> artifact-origin, integrity, identity, and log evidence
  -> Commitment Candidate translation
  -> independent StegVerse commit-time evaluation
  -> ALLOW, DENY, ESCALATE, or FAIL_CLOSED
```

## Authored test families

| Family | Native posture | Governed expectation |
|---|---|---|
| Positive alignment | Signature, identity, log, trust, and transition conditions are current. | `ALLOW` |
| Framework denial | Signature verification fails. | `DENY` |
| Authority failure | Artifact verifies but current delegation is revoked. | `DENY` |
| Stale evidence | Trust root or evidence is stale. | `FAIL_CLOSED` |
| Runtime error | Verifier errors or returns undefined evidence. | `FAIL_CLOSED` |
| Semantic divergence | Artifact verifies but requested action is outside scope. | `DENY` |

## Machine-readable procedure

```text
fixture: tests/fixtures/external-frameworks/sigstore-governance-compatibility-cases.v1.json
runner: scripts/run_sigstore_governance_compatibility.py
result receipt: reports/external-frameworks/sigstore/sigstore-stegverse-governance-compatibility-receipt.json
status ledger: static/external-frameworks/governance-compatibility-testing-status.v1.json
```

## Execution sequence required for promotion

1. Pin a Sigstore client, trust-root set, and verification policy.
2. Attach a signed artifact, signature, certificate chain, and transparency proof.
3. Capture raw positive, negative, stale, malformed, and scope-divergence verifier outputs.
4. Record client version, source or binary hash, runtime environment, commands, and timestamps.
5. Execute the StegVerse translation evaluator against captured native outputs.
6. Replay the verification and governed evaluation on a fresh runner.
7. Publish the receipt and update the status ledger only from observed evidence.

## Current limitation

The authored runner uses predeclared Sigstore outcomes. It validates the translation and StegVerse decision contract only; it does not establish native Sigstore behavior or bounded interoperability.

## Non-claims

```text
valid signature != authorized action
certificate identity != current delegation
transparency inclusion != admissibility
artifact integrity != deployment permission
translation-contract pass != native verification
```

Publication creates no standing, certification, release permission, execution authority, or general compatibility claim.
