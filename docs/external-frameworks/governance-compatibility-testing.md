---
title: Governance Compatibility Testing
---

# External Framework Governance Compatibility Testing

## Purpose

Compatibility testing determines where an external framework and StegVerse governance can align, exchange artifacts, and operate together without silently changing either system's meaning or authority boundaries.

It is not satisfied merely because the external framework executes successfully.

## Compatibility question

For each framework, the test asks:

> Can the framework's native output be translated into a StegVerse governed transition path, with the correct evidence role, while StegVerse independently reconstructs every commit-time condition the framework does not establish?

## Required test layers

```text
1. native framework execution
2. pinned implementation and artifact capture
3. semantic translation
4. StegVerse commit-time evaluation
5. positive and failure-boundary cases
6. same-environment replay
7. fresh-runner replay
8. machine-readable result publication
```

## Required case families

Every completed framework test must cover, or explicitly justify non-applicability for:

```text
positive alignment
framework denial or negative result
authority or delegation failure
stale or missing evidence
malformed, undefined, or runtime error
semantic divergence guard
```

## Compatibility model

```text
framework-native artifact
        ↓
versioned translation mapping
        ↓
StegVerse evidence / identity / policy / provenance input
        ↓
commit-time authority, delegation, freshness, scope,
recoverability, context, and consequence evaluation
        ↓
ALLOW / DENY / ESCALATE / FAIL_CLOSED
```

The external framework may supply one or more inputs to the StegVerse decision. It does not inherit authority over the complete decision.

## Examples

| Framework capability | Permitted StegVerse role | What remains separately governed |
|---|---|---|
| OPA or Cedar policy result | Policy-decision evidence | Identity, current delegation, evidence freshness, scope, recoverability, consequence standing |
| SPIFFE identity | Actor and credential evidence | Action-level delegation and commit-time authority |
| Verifiable Credential | Signed claim evidence | Claim truth, current status, delegation, and consequence authority |
| in-toto, SLSA, Sigstore | Provenance and integrity evidence | Deployment authority and environmental admissibility |
| OpenLineage or W3C PROV | Reconstruction and lineage evidence | Legitimacy, permission, and standing |
| MCP or A2A | Tool, capability, task, or coordination description | Delegation validity and action-level execution authority |
| Guardrail frameworks | Validation or safety evidence | Complete policy, authority, evidence, and commit-time governance |

## Evidence states

```text
NOT_STARTED
CONTRACT_AUTHORED
NATIVE_EXECUTION_OBSERVED
TRANSLATION_VALIDATED
GOVERNANCE_COMPATIBILITY_OBSERVED
FRESH_RUNNER_REPRODUCED
INDEPENDENT_IMPLEMENTATION_REPRODUCED
SOURCE_BLOCKED_FAIL_CLOSED
```

Documentation completeness and compatibility-test completion are separate states.

## Current program status

```text
canonical framework records: 38
framework-specific compatibility contracts authored: 1
bounded governance compatibility results observed: 0
fresh-runner governance compatibility reproductions: 0
independent-implementation reproductions: 0
```

The first authored contract is Open Policy Agent:

- [Open Policy Agent](./open-policy-agent.md)
- [OPA Governance Compatibility Test](./opa-governance-compatibility-test.md)

Machine-readable program status:

```text
static/external-frameworks/governance-compatibility-testing-status.v1.json
```

## Completion rule

A framework page may state bounded compatibility only when its procedure, fixtures, native artifacts, translation mapping, StegVerse results, failure results, hashes, replay commands, runtime identity, timestamps, and limitations are public and validator-enforced.

A bounded compatibility result remains specific to the tested versions, artifacts, mappings, cases, and conditions.

## Non-claims

```text
framework execution != governance compatibility
framework allow != StegVerse ALLOW
framework identity != action authority
framework validation != admissibility
framework provenance != legitimacy
translation != equivalence
compatibility != certification
compatibility receipt != execution authority
```

Compatibility testing establishes bounded interoperability evidence. It does not certify a framework, create general compatibility, grant standing, or authorize execution.
