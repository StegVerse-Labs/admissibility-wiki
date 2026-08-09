---
title: Policy Cards External Framework Crosswalk
---

# Policy Cards External Framework Crosswalk

## Status

```text
Relationship type: external framework crosswalk
Canonical StegVerse formalism source: Admissible-Existence
External framework role: machine-readable deployment-layer normative policy artifact
Evaluated source: arXiv:2510.24383v1
Source submission: 2025-10-28
Paper date: 2025-10-19
Canonical archived DOI declared by arXiv: 10.5281/zenodo.17391796
Related resource DOI declared by arXiv: 10.5281/zenodo.17464706
Evidence class: SOURCE_REVIEWED_SCHEMA_DESCRIBED
Runtime posture: NATIVE_EXECUTION_NOT_OBSERVED
Standing: none created
Execution authority: none
```

## Framework-Native Scope

Policy Cards are presented as versioned, machine-readable deployment-layer specifications for operational rules, obligations, exceptions, evidence requirements, monitoring, change management, and assurance mappings for a deployed AI system or agent. The paper describes JSON Schema 2020-12 as the structural basis and discusses validation, version control, CI/CD gates, runtime policy gateways, monitoring, and audit pipelines.

The framework-native action effects are `allow`, `deny`, and `require_escalation`. Those effects are policy-artifact outputs. They are not StegVerse standing, delegation, admissibility, commitment, or execution authority.

## Official Framework Sources

```text
primary record: https://arxiv.org/abs/2510.24383
arXiv version: 2510.24383v1
submission timestamp: 2025-10-28T12:59:55Z
paper title: Policy Cards: Machine-Readable Runtime Governance for Autonomous AI Agents
author: Juraj Mavračić
arXiv DOI: 10.48550/arXiv.2510.24383
canonical archived record DOI listed by arXiv: 10.5281/zenodo.17391796
related resource DOI listed by arXiv: 10.5281/zenodo.17464706
```

The evaluated framework source is therefore version-pinned to arXiv `2510.24383v1`.

## Official Implementation Sources

The paper states that a full schema, validator, and domain scenarios are available through a public repository and Zenodo resource. This StegVerse record does **not** promote that statement into an implementation identity because no exact external repository commit, immutable package hash, or frozen validator binary/package has been independently bound here.

Implementation status:

```text
implementation_attached=false
native_execution_observed=false
implementation_identity=UNBOUND
```

A later implementation evidence transition must bind a stable repository/package identity, immutable hashes, commands, environment, raw output, and replay receipt before native validator or runtime behavior can be claimed.

## Evidence Provenance

| Evidence Class | Current Evidence | Status | Missing Fields |
|---|---|---|---|
| Official Framework Source | arXiv `2510.24383v1`, author, submission timestamp, paper date, arXiv DOI, and archive/resource DOI identifiers. | pinned_versioned_public_source | No source-version ambiguity for the evaluated paper revision. |
| Schema Evidence | Paper describes JSON Schema 2020-12, structured deployment policy fields, semantic versioning, action rules, temporal bounds, monitoring, KPI and assurance-mapping structures. | source_described | Exact external repository/commit/hash for the full schema and validator is not bound locally. |
| Official Implementation Evidence | Paper states a full schema/validator and domain scenarios exist in a public repository/Zenodo resource. | external_locator_unbound | Stable repository/commit and immutable package identity required before execution attribution. |
| Observed Native Behavior | No external Policy Cards validator or runtime gateway was executed by this StegVerse transition. | not_observed | Frozen implementation package, command, environment, raw output, and receipt required. |
| StegVerse Analysis | Six deterministic governance case families are installed. | installed_simulation_only | Simulation remains separate from native framework execution. |
| Standing | Publication, schema description, an `allow` effect, or a policy-card artifact does not establish current actor delegation or execution authority. | none_created | Standing and delegation must be independently reconstructed at commit time. |

## Framework-Term Definitions

This section provides inline terminology reconciliation and governed coverage for the framework-native vocabulary.

| Native term | Definition for this wiki | Governed coverage / admissibility relationship |
|---|---|---|
| Policy Card | Versioned machine-readable deployment policy for a specific system/context. | Policy Reference and Evidence Posture input; not a commit decision. |
| `controls.action_rules` | Rules binding subject, action, resource, condition, and effect. | Candidate policy evidence for transition review. |
| `allow` / `deny` / `require_escalation` | Framework-native rule effects. | Must not be conflated with StegVerse standing, admissibility, or execution authority. |
| obligations | Actions that must occur under specified conditions. | May become commitment obligations only when independently applicable and current. |
| exceptions | Explicit bounded deviations with approval/justification/validity. | Requires independent authority and validity reconstruction. |
| monitoring | Loggable events, fields, detectors, thresholds, retention, and review cadence. | Evidence Posture and reconstructability input. |
| `critical_auto_fail` | Critical KPI failure condition described by the source. | Supports fail-closed policy evidence; does not independently bind consequence. |
| assurance mapping | Links policy fields to external assurance frameworks. | Translation evidence; mapping is not certification or equivalence. |

## Relationship to Admissibility

A Policy Card can be a structured Policy Reference for a Commitment Candidate because it can bind deployment context, rule effect, evidence requirements, validity period, monitoring expectations, and change history. StegVerse must still reconstruct whether the card is current and applicable, whether the actor has standing and delegation, whether evidence is fresh, whether the proposed action semantically matches the governed resource/action, whether an exception remains valid, and whether the target can bind consequence under current authority.

`policy_card.effect == allow` therefore does **not** imply `StegVerse admissibility == ALLOW`.

## Observed Behavior

No Policy Cards native validator or runtime gateway behavior has been observed by StegVerse in this evidence transition.

```text
native_execution_observed=false
observed_native_decisions=0
```

The absence of native observation is preserved as an evidence boundary rather than interpreted as failure or success.

## Reproduced Behavior

No native implementation reproduction has been performed because the implementation package identity is not yet frozen.

```text
same_environment_replay=NOT_PERFORMED
fresh_runner_replay=NOT_PERFORMED
independent_provider_reproduction=NOT_PERFORMED
```

StegVerse deterministic simulations are separately reproducible repository fixtures but are not native Policy Cards runtime replay.

## StegVerse Analysis

Installed deterministic case families:

F1: positive alignment — ALLOW only when policy evidence, authority, freshness, scope, and other commitment conditions are independently satisfied.

F2: framework denial — DENY when the Policy Card rule denies the proposed action.

S1: authority/delegation failure — DENY when a card permits an action but current actor authority is absent.

S2: stale or missing evidence — FAIL_CLOSED when card/evidence validity cannot be established.

H1: malformed or undefined input — FAIL_CLOSED when the policy artifact cannot be interpreted.

Additional semantic/authority divergence family — DENY when a policy artifact is used to claim authority it does not confer or when action semantics diverge.

These are StegVerse-authored deterministic simulations. `implementation_attached=false` and `native_execution_observed=false` remain required boundaries in the fixture.

## Interoperability Assessment

Current interoperability is a bounded source-level crosswalk, not native validator/runtime interoperability.

`runtime_policy_artifact_crosswalk`:

```text
policy_card_id
policy_card_version
policy_card_hash
source_or_schema_identity
deployment_scope
jurisdiction
valid_from
valid_to
subject
action
resource
condition
framework_effect
obligations
exception_reference
evidence_required
monitoring_reference
critical_auto_fail_state
assurance_mapping_refs
policy_owner_reference
delegation_reference
commitment_candidate_hash
```

A consumer must reject or defer when identity, validity, scope, semantics, authority, or required evidence cannot be reconstructed.

Governance-chain placement:

```text
Policy Card artifact
  -> Policy Reference / Evidence Posture
  -> standing + delegation reconstruction
  -> freshness + applicability + semantic equivalence checks
  -> commit-time admissibility
  -> execution authority / consequence binding
```

Policy Cards occupy the policy-artifact/evidence layer. They do not independently supply the later authority layers.

## Failure Classes

```text
POLICY_CARD_DENY
POLICY_CARD_UNRESOLVED
POLICY_CARD_STALE
POLICY_CARD_SCOPE_DIVERGENCE
POLICY_CARD_AUTHORITY_OVERCLAIM
POLICY_CARD_IMPLEMENTATION_IDENTITY_UNBOUND
POLICY_CARD_NATIVE_EXECUTION_NOT_OBSERVED
```

## Machine-Readable Companions

```text
manifest: docs/external-frameworks/policy-cards.json
benchmark mapping: docs/external-frameworks/benchmark-mappings/policy-cards.mapping.json
benchmark fixture: docs/external-frameworks/fixtures/policy-cards-benchmark-fixture.v0.1.json
governance fixture: tests/fixtures/external-frameworks/policy-cards-governance-compatibility-cases.v1.json
compatibility report: docs/external-frameworks/reports/policy-cards.compatibility.json
canonical workflow: .github/workflows/validate-chain-continuation.yml
```

## Claims Versus Demonstrated Abilities

| Question | Current evidence |
|---|---|
| Is a versioned primary source pinned? | Yes: arXiv `2510.24383v1`. |
| Does the source define a machine-readable deployment policy artifact? | Yes. |
| Does the source describe JSON Schema 2020-12 and validation/linting behavior? | Yes. |
| Has StegVerse executed the external full validator? | No. |
| Has StegVerse observed a native Policy Cards runtime gateway? | No. |
| Are six governance case families installed? | Yes, as deterministic StegVerse simulations. |
| Does a Policy Card `allow` establish actor standing? | No. |
| Does Policy Cards establish StegVerse execution authority? | No. |
| Is certification or endorsement claimed? | No. |

## Validation Completion Criteria

For the bounded source-level evaluation, canonical validation must observe the manifest, terminology, report, page metadata/mapping/status, evidence provenance, benchmark mapping/fixture, and six-family governance compatibility without a Policy-Cards-specific failure. Native implementation execution remains explicitly unclaimed unless a frozen repository/package identity and observed command/output receipt are later installed.

## Non-Claims

```text
Policy Cards are not a StegVerse canonical formalism.
A Policy Card is policy evidence, not actor identity or delegation.
A framework-native allow effect is not StegVerse commit-time admissibility.
Machine readability does not create standing.
StegVerse deterministic fixtures are not native Policy Cards runtime observations.
The paper's statement that a public repository exists is not treated here as a verified repository/commit identity.
No certification, endorsement, compliance determination, or execution authority is created by this page.
Publication does not create standing.
```

## Next Safe Build Target

If a stable public repository/Zenodo implementation package can be independently resolved, freeze the exact schema/validator identity, package hashes, commands, environment, inputs, raw outputs, and replay receipt, then evaluate whether native implementation evidence legitimately raises the evidence class. Until then, the bounded source-level crosswalk must fail closed against native-runtime claims.

## Challenge Path

A challenge should identify the disputed source version, schema field, rule effect, deployment scope, evidence requirement, implementation identity, StegVerse mapping, or authority boundary and provide inspectable evidence for correction.

## Mandatory Footer

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from referenced evidence, authority, and admissibility conditions.
