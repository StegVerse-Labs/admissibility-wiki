# Federal Minimum Exceedance Security Baseline

## Policy

Federal security requirements are the minimum acceptable floor for StegVerse systems. Applicable federal controls must be satisfied first; StegVerse-specific controls then add stricter evidence, authority, recovery, and continuous-verification requirements.

This document is a control policy and engineering baseline. It is not a claim of FedRAMP authorization, FISMA authorization, FIPS validation, agency approval, or federal certification.

## Federal floor

The declared floor consists of the applicable portions of:

- NIST SP 800-53 Rev. 5 and current published updates;
- NIST SP 800-53B control baselines;
- NIST SP 800-218 Secure Software Development Framework;
- FIPS 140-3 for cryptographic modules where validated cryptography is required;
- FedRAMP Rev. 5 baseline requirements where a cloud service falls within FedRAMP scope.

Applicability must be assessed per system, data category, deployment environment, and authority boundary. A control may not be marked satisfied solely because a document, workflow, schema, or example exists.

## Mandatory exceedance controls

### 1. Authority separation

The system must represent each of the following independently:

```text
visibility
verification
identity
standing
consent
admissibility
commitment
execution permission
release authority
downstream mutation authority
```

No state may be inferred from another. Verification does not imply execution permission. Publication does not imply admissibility. Deployment does not imply release authority.

### 2. Fail-closed evidence handling

Missing, malformed, stale, inconsistent, unverifiable, or inaccessible evidence must produce a fail-closed or blocked state. Absence of evidence must never be converted into success, completion, certification, or authority.

### 3. Run-bound provenance

Security-relevant validation and deployment evidence must bind, where available:

```text
repository
branch or ref
commit SHA
workflow identity
run ID
run attempt
artifact identity
input digest
output digest
timestamp
validator version
```

### 4. Deterministic negative-path testing

Every high-impact security or authority transition must have at least one deterministic denial or fail-closed test. Positive-path testing alone is insufficient.

### 5. Canonical workflow and collision control

A repository must identify one canonical validation/deployment workflow. Duplicate execution lanes must be prohibited or explicitly partitioned. Claims must have owners, collision boundaries, and expiration or release conditions.

### 6. Supply-chain integrity

Dependencies, generated artifacts, build outputs, and deployment receipts must be attributable to their source inputs. Unpinned or unverifiable dependencies must not be treated as equivalent to verified supply-chain provenance.

### 7. Cryptographic strength and agility

Approved cryptography must use validated modules when required by deployment authority. The architecture must preserve algorithm agility, key rotation, revocation, compromise recovery, and post-quantum migration readiness. Post-quantum readiness is not equivalent to post-quantum security validation.

### 8. Recovery and reconstructability

Security controls must be evaluated during degraded operator authority, partial outage, rollback, restoration, and reconstruction. A control that is enforceable only while all actors and services remain coherent is incomplete.

### 9. Continuous observation

One-time evidence is insufficient for long-lived activation. Repository-owned automation must re-observe critical validation, deployment, public-route, dependency, and receipt states at an interval appropriate to the risk.

### 10. Privacy exceedance

Collection authorization alone is insufficient. Systems must enforce data minimization, purpose limitation, retention limits, deletion or irreversible de-identification where appropriate, and explicit disclosure boundaries.

### 11. Security downgrade prevention

A stronger StegVerse control may not be silently replaced by a weaker federal-floor control. Any downgrade requires an explicit governed decision, risk acceptance, scope, duration, compensating controls, and expiry.

### 12. Evidence before claims

The following claims require direct evidence from the applicable authority or validated runtime surface:

```text
FedRAMP authorized
FISMA authorized
FIPS validated
federal compliant
agency approved
production secure
penetration tested
zero trust compliant
post-quantum secure
```

Without that evidence, the state must remain `NOT_CLAIMED`, `UNVERIFIED`, `BLOCKED`, or `FAIL_CLOSED`.

## Minimum machine-readable states

```text
COMPLETE
BLOCKED
RETRY
REVIEW_REQUIRED
FAILED
CLAIMED
SUPERSEDED
MERGED
FAIL_CLOSED
```

## Validation boundary

Static validation proves only that the baseline and profile are internally consistent. Hosted workflow success, deployment hardening, runtime enforcement, cryptographic module validation, penetration resistance, and federal authorization require separate evidence.
