# Riverbraid

## Intake status

```text
SOURCE_BLOCKED_FAIL_CLOSED
```

Riverbraid is recorded as an external-framework comparison target based on a public announcement attributed to Michael Tilk. The announcement describes a stationary, fail-closed governance layer that verifies configurations, dependencies, and outputs before execution, uses a Bitcoin-anchored root, restricts governance changes through threshold signatures, and operates as an environment-agnostic proxy.

The announcement and shortened links are intake evidence only. They are not sufficient to establish architecture, compatibility, interoperability, regulatory compliance, execution authority, or commit-time admissibility.

## Execution-boundary question

The primary evaluation question is not whether Riverbraid can prove component or configuration integrity. It is whether the governed system can still deny a transition in the live state immediately before irreversibility.

A complete comparison must re-resolve together:

1. state admissibility;
2. current authority validity rather than inherited authority;
3. denial reachability before commitment.

If denial is no longer reachable, a verification result may certify a foregone transition rather than enforce governance.

## Framework-Term Definitions

| Framework Term | Framework Meaning | Reconciliation Class | Admissibility Relationship |
|---|---|---|---|
| stationary fail-closed governance | A claimed governance layer that rejects execution when verification conditions are not met. | adjacent | May provide upstream integrity and refusal evidence, but does not establish current standing or commit-time execution authority. |
| cryptographic verification before execution | A claimed check of configuration, dependencies, and outputs before an action proceeds. | adjacent | Verification evidence may enter a Commitment Candidate; admissibility still requires current authority, state, policy, evidence, and denial reachability. |
| threshold-signature-controlled change | A claimed multi-party control over governance mutation. | unresolved | Delegation derivation, scope, expiry, revocation, and commit-time validity remain unevidenced. |
| independent auditability | A claimed ability for external parties to inspect anchored evidence. | adjacent | Auditability may support reconstruction but does not itself prove non-execution after denial or authorize a transition. |

The reconciliation class is provisional because no canonical technical source or independently reviewable implementation artifact has been supplied.

## Evidence required

- canonical technical documentation and versioned source artifacts;
- the exact pre-execution and commit-time enforcement point;
- proof that denial remains reachable in the evaluated state;
- authority derivation, delegation, threshold, expiry, and revocation semantics;
- drift handling for policy, identity, dependency, evidence, model, and execution context;
- fail-closed behavior when anchoring, network, proxy, or verification dependencies are unavailable;
- reconstructable evidence that an action did not occur after denial;
- receipt, trace, canonicalization, replay, and retention contracts;
- evidence supporting any EU AI Act or SOC 2 alignment claim;
- application-specific recovery and authority behavior behind the environment-agnostic proxy claim.

## Current permitted result

```text
SOURCE_REQUIRED / SOURCE_BLOCKED_FAIL_CLOSED
```

This result does not assert incompatibility. It records that the available announcement is insufficient for a compatibility or admissibility determination.

## Governance boundary

This page does not certify, endorse, validate, authorize, or establish interoperability with Riverbraid. It does not establish regulatory compliance, execution authority, commit-time standing, or proof that pre-execution integrity verification preserves denial reachability.

## Continuation record

The intake task, source links, required evidence, permitted scope, and completion event are recorded in GitHub issue #16.
