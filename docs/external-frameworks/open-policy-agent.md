---
title: Open Policy Agent
---
# Open Policy Agent

## Evidence posture

```text
evidence_class: SOURCE_REVIEWED
observed_evidence_class: PARAMETERIZED_OBSERVATION
page_completeness: COMPLETE_WITH_EXTERNAL_GATES
native_runtime_observation: observed
same_environment_replay: observed
fresh_runner_same_provider_replay: observed
StegVerse_bounded_governance_compatibility: observed_6_of_6
independent_implementation_reproduction: false
comparative_testing_claim_allowed: false
bounded_comparative_result_recorded: true
execution_authority_claim_allowed: false
```

`SOURCE_REVIEWED` remains the page's non-escalating source boundary required by the public remediation contract. The stronger bounded observation is recorded separately and does not convert the page into a general compatibility, certification, standing, or authority claim.

## Published scope

Open Policy Agent is a general-purpose policy engine that evaluates structured input against policy and produces policy decisions.

Canonical source: https://www.openpolicyagent.org/docs/latest/

StegVerse has additionally executed a pinned OPA capture/replay path and a bounded governance-compatibility evaluation. The observed result is limited to the pinned artifacts and six declared case families; it is not a general certification of OPA.

## Native terms

| OPA term | Meaning here | StegVerse relationship |
|---|---|---|
| Input | Structured facts supplied for evaluation. | Evidence input; not standing by itself. |
| Policy | Rego rules and data used to evaluate input. | Policy reference that must remain current and scoped. |
| Decision | OPA evaluation output. | Non-authorizing policy evidence; not execution authority. |
| Bundle | Deployable policy and data package. | Versioned source artifact requiring hash and custody evidence. |

## Relationship to admissibility

```text
OPA asks: What result follows from this input, policy, and data?
StegVerse asks: May this transition bind consequence at commit time under current identity, authority, policy, delegation, evidence, scope, recoverability, and execution context?
```

OPA can contribute a policy-decision artifact to a governed transition path. That decision does not establish that the actor has current authority, delegation remains valid, evidence is fresh, or consequence may bind now.

```text
OPA input + policy -> OPA policy decision
OPA decision -> bounded policy evidence
StegVerse -> current state / authority / delegation / evidence / scope evaluation
StegVerse -> ALLOW / DENY / ESCALATE / FAIL_CLOSED
separate commit/execution boundary -> consequence
```

## Evidence Provenance

Canonical evidence:

```text
workflow run: 29455057960
commit: 618a57fb618cd29c90264eb1cab5f4d6814a55f6
validate-chain-continuation: SUCCESS
capture-opa-evidence: SUCCESS
replay-opa-fresh-runner: SUCCESS
OPA governance compatibility evaluator: OBSERVED
cases: 6/6 expected == observed
bounded state: GOVERNANCE_COMPATIBILITY_OBSERVED
```

The overall workflow concluded failure because a later `build-pages` job failed; the OPA capture, replay, compatibility execution, and canonical validation jobs completed successfully before that unrelated publication-stage failure.

Preserved artifact evidence:

```text
pinned capture/replay artifact:
  id: 8359055203
  sha256: 552b50531de1877abc6c5b1546feaa1e45d9aea5800f530da3039b4bb32a580a
fresh-runner replay artifact:
  id: 8359059090
  sha256: f1d7aaf4a8a1719aba498826cf7b9df4a8f913feb6a6418c8ae23840e268f8ff
```

Detailed test page: `opa-governance-compatibility-test.md`.

## Expected versus observed outcomes

| Condition | Expected | Observed |
|---|---|---|
| OPA allow + all StegVerse commit-time conditions current | `ALLOW` | Match |
| OPA deny | `DENY / POLICY_DENIAL` | Match |
| OPA allow + revoked delegation | `DENY / AUTHORITY_DRIFT` | Match |
| OPA allow + stale evidence | `FAIL_CLOSED / STALE_EVIDENCE` | Match |
| No usable OPA decision | `FAIL_CLOSED / FRAMEWORK_RUNTIME_ERROR` | Match |
| OPA allow + target outside current scope | `DENY / SCOPE_DIVERGENCE` | Match |

## StegVerse analysis and governance-chain position

| Criterion | Observed / bounded result |
|---|---|
| Identity | OPA evaluates supplied attributes; it does not independently establish actor identity. |
| Authority | OPA `allow` does not establish present consequence-binding authority. |
| Policy | Direct overlap: OPA supplies policy-decision evidence from pinned policy/input. |
| Delegation | Must be reconstructed separately; revoked delegation produced StegVerse `DENY` even when OPA allowed. |
| Evidence | OPA output is usable as evidence when input, policy, runtime identity, output, and hashes are retained. |
| Replayability | Observed on same environment and fresh runner using the same OPA implementation/provider. |
| Reconstructability | Bounded test artifacts and receipts preserve enough state to reconstruct the declared comparison. |
| Failure behavior | Missing/undefined OPA result remains fail-closed in the StegVerse compatibility evaluator. |
| Interoperability | OPA occupies the policy-evaluation evidence layer before StegVerse commit-time admissibility. |
| Execution authority | Not supplied by OPA and not granted by the compatibility receipt. |

## Commit-time interoperability contract

Minimum OPA-specific fields:

```text
transition_id
actor
requested_action
target_system
opa_input
opa_decision
opa_query
policy_bundle_reference
policy_bundle_hash
opa_version
data_reference
decision_log_reference
policy_reference
delegation_reference
evidence_references
execution_context
validity_window
source_timestamp
```

## Failure Classes

| Failure class | Observed or tested boundary |
|---|---|
| Policy denial | OPA `allow: false` enters as policy evidence and produced `DENY / POLICY_DENIAL`. |
| Authority drift | OPA `allow: true` did not override revoked delegation; StegVerse produced `DENY / AUTHORITY_DRIFT`. |
| Stale evidence | OPA `allow: true` did not override stale evidence; StegVerse produced `FAIL_CLOSED / STALE_EVIDENCE`. |
| Framework runtime error | Missing usable OPA decision produced `FAIL_CLOSED / FRAMEWORK_RUNTIME_ERROR`. |
| Scope divergence | OPA `allow: true` did not override target mismatch; StegVerse produced `DENY / SCOPE_DIVERGENCE`. |
| Replay divergence | Same-environment and fresh-runner decisions matched for the pinned test, but independent implementation/provider reproduction remains unobserved. |

## Replay path

```text
python scripts/run_pinned_opa_ci_capture.py
python scripts/run_independent_opa_ci_replay.py
python scripts/run_opa_governance_compatibility.py
```

The fresh-runner replay is stronger than a single local observation but is explicitly not independent-implementation or independent-provider reproduction.

## Machine-readable companions

```text
manifest: docs/external-frameworks/open-policy-agent.json
compatibility report: docs/external-frameworks/reports/open-policy-agent.compatibility.json
bounded compatibility status: static/external-frameworks/governance-compatibility-testing-status.v1.json
compatibility receipt (workflow artifact): reports/external-frameworks/opa-independent/opa-stegverse-governance-compatibility-receipt.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Remaining external gates

```text
independent organization reproduction: not observed
independent provider reproduction: not observed
independent OPA implementation reproduction: not observed
production StegVerse integration: not established
certification / endorsement: not established
execution authority: not granted
```

Those gates limit stronger claims; they do not erase the bounded 6/6 observed compatibility result.

## Validation Completion Criteria

The local second-page evidence package is complete at the bounded observation level only when all of the following remain inspectable together:

```text
pinned OPA runtime identity
pinned policy and input artifacts
raw capture/replay evidence
same-environment replay receipt
fresh-runner same-provider replay receipt
six predeclared compatibility cases
6/6 expected-versus-observed match
workflow and commit identity
artifact digests
explicit non-equivalence and non-authority boundaries
```

Independent organization/provider/implementation reproduction is a separate higher evidence class and is not claimed here.

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface. A challenge should identify `open-policy-agent`, the disputed field or observed result, and the source or artifact supporting correction. Evidence strength may not be increased without corresponding inspectable evidence.

## Non-claims

OPA inclusion is not certification, equivalence, admissibility proof, standing, production integration, or execution authority. A policy allow result does not independently authorize consequence binding. The bounded StegVerse result applies only to the pinned policy/input/replay artifacts and six declared compatibility cases.

This page reflects bounded evidence-governance work. Publication does not create standing.

## Next Safe Build Target

Preserve the bounded OPA result while seeking a genuinely independent provider, organization, or alternate implementation reproduction. Until such evidence exists, keep `comparative_testing_claim_allowed: false` for general claims and preserve the 6/6 result only as a parameterized StegVerse observation.
