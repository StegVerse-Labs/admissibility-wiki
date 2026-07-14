# Quantum-Resilient Execution Security

## Overview

StegVerse treats post-quantum cryptography as a core security layer, not as a complete security architecture by itself.

Post-quantum algorithms can protect key establishment, signatures, identity material, policies, delegations, capabilities, releases, and receipts against known classes of quantum attack. StegVerse adds a separate execution-security layer that determines whether a specific state transition remains admissible at the moment consequence attaches.

The governing distinction is:

```text
communication trust != execution trust
```

A secure channel can authenticate a participant and protect data in transit. It does not independently establish that the participant remains delegated, the evidence remains fresh, the target remains in scope, the current state still permits the action, or the consequence remains recoverable.

## Architecture

```text
AI, human, or service proposal
             |
             v
canonical policy resolution
             |
             v
current delegation resolution
             |
             v
state and evidence validation
             |
             v
commit-time admissibility
     ALLOW / DENY / FAIL_CLOSED
             |
             v
state-bound capability
             |
             v
execution-boundary verification
             |
             v
transition + reconstructable receipt
```

## Security composition

StegVerse complete security is modeled as:

```text
post-quantum cryptography
+ cryptographic agility
+ state-bound execution authority
+ commit-time admissibility
+ separation of reasoning and execution
+ receipt-bound evidence
+ replay resistance
+ recoverability
+ fail-closed execution boundaries
```

## Post-quantum primitives

Current standardized primitives relevant to this architecture include:

- **ML-KEM** — NIST FIPS 203 key encapsulation, derived from CRYSTALS-Kyber.
- **ML-DSA** — NIST FIPS 204 digital signatures, derived from CRYSTALS-Dilithium.
- **SLH-DSA** — NIST FIPS 205 stateless hash-based signatures, derived from SPHINCS+.

A StegVerse implementation should use versioned cryptographic-suite identifiers and support hybrid migration, deprecation, key rotation, downgrade prevention, cross-implementation testing, and long-term evidence preservation.

## State-bound execution authority

Authority is not assumed to persist because a session was authenticated or a prior approval existed.

A transition-specific capability should bind:

```text
transition_id
actor
action
target
scope
policy_ref + policy_digest
delegation_ref + delegation_digest
evidence_refs + evidence_digests
state_digest
validity_window
recoverability_profile
nonce / replay state
cryptographic_suite
```

The execution boundary re-checks the binding immediately before execution. A material mismatch produces `DENY` or `FAIL_CLOSED`.

## Why this adds security beyond post-quantum TLS

Post-quantum TLS can protect data between endpoints and reduce harvest-now-decrypt-later risk when correctly deployed.

It cannot by itself prevent:

- execution after delegation revocation;
- use of stale evidence;
- replay of a previously valid action;
- target or scope substitution;
- policy drift;
- unsafe AI output;
- compromised endpoint behavior;
- actions that exceed recoverability constraints.

StegVerse addresses those risks at the state-transition boundary.

## Receipt reconstruction

A transition receipt should support independent reconstruction of:

1. the proposed action;
2. the actor and target;
3. canonical policy and delegation;
4. current state and evidence;
5. the admissibility decision;
6. capability issuance and consumption;
7. execution-boundary result;
8. resulting consequence and recovery status.

A receipt is evidence. It does not become execution authority, certification, or proof of legitimacy merely because it exists.

## Fail-closed conditions

The transition should fail closed when:

- policy or delegation cannot be resolved;
- required evidence is unavailable or stale;
- current state cannot be established;
- cryptographic-suite policy rejects the artifact;
- replay or consumption state is unknown;
- the execution boundary cannot establish its own integrity;
- consequence exceeds the authorized recoverability profile.

## Security properties under explicit assumptions

When correctly implemented, the architecture is intended to provide:

- rejection of stale capabilities;
- transition-specific scope enforcement;
- replay resistance;
- separation of verification from execution authority;
- cryptographic migration without redefining admissibility semantics;
- reconstructable decision evidence;
- a reachable refusal point before consequence.

These properties depend on trustworthy canonical inputs, secure cryptographic implementations, correct state observation, durable replay state, protected keys, and an uncompromised execution boundary.

## Non-claims

This page does not establish:

- universal quantum-proof security;
- NIST certification of StegVerse;
- production deployment of ML-KEM, ML-DSA, or SLH-DSA across every endpoint;
- formal verification of the complete architecture;
- immunity to endpoint compromise, side channels, malicious policy, or future cryptanalysis;
- execution authority derived from publication, independent review, or receipts.

## Publication package

- [Complete security research paper](../research/stegverse-complete-security-paper.md)
- [LinkedIn carousel source](../social/stegverse-quantum-security-carousel.md)
- Simulation source: `simulations/quantum_execution_security_model.py`
- Goal-specific handoff: `docs/STEGVERSE_QUANTUM_SECURITY_MIRROR_HANDOFF.md`

## Verification status

```text
PUBLICATION_SOURCE_IMPLEMENTED_PENDING_REPO_VALIDATION_AND_PUBLIC_ROUTE_INTEGRATION
```

The page is a bounded research and governance surface. Public reachability, workflow validation, cryptographic implementation, audit, and deployment evidence must be established separately.