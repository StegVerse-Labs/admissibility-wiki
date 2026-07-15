# Ecosystem Capability Status

## Purpose

This page explains how ecosystem capability status must be reported across separate coordinates. A single label such as `implemented` or `validated` is insufficient when documentation, runtime source, deployment, conformance, custody, and execution are owned by different repositories or authorities.

## Machine-readable example

```text
static/status/ecosystem-capability-status.example.json
```

Validator:

```text
scripts/check_ecosystem_capability_status_example.py
```

The example is a schema demonstration only. It is not evidence that every ecosystem capability occupies the state shown in the fixture.

## Governed LLM coordinate status

| Coordinate | Owner | Current evidence posture | Lifecycle interpretation |
|---|---|---|---|
| Public doctrine and topology | `StegVerse-Labs/admissibility-wiki` | Source pages and validators installed; public workflow observation remains evidence-bound. | `IMPLEMENTED`; higher state requires observed canonical evidence. |
| Adapter fixture runtime | `StegVerse-org/LLM-adapter` | Fixture-first source and verification commands documented. | `FIXTURE_VALIDATED` only where pinned outputs are available. |
| SDK contract layer | `StegVerse-org/StegVerse-SDK` | Packet validation, intake routing, manifest binding, and receipt handoff source documented. | `IMPLEMENTED` or repository-evidenced validation state; no execution authority. |
| Site client surfaces | `StegVerse-Labs/Site` | Client and contract preparation complete. | `PREPARED_NOT_DEPLOYED`; not operational. |
| Same-origin gateway | Site plus authorized destination | No authorized deployment evidence recorded here. | `NOT_DEPLOYED`. |
| Live provider path | Provider plus adapter deployment | Credentials and authorized deployed provider conformance not established. | `EXTERNAL_NOT_ESTABLISHED`. |
| Formalism proof | `Data-Continuation/formalism-tests` | Executable fixtures and receipts remain authority-repository owned. | State must be read from that repository; wiki does not promote it. |
| Master-Records custody | `master-records/orchestration` | Authenticated custody and reconstructability evidence required. | `NOT_ESTABLISHED`. |
| External executor | Explicit executor authority | Adapter emits disabled handoff by default. | `DISABLED_OR_EXTERNAL`. |

## Aggregate status rule

The aggregate capability state must be bounded by the weakest required consequence-bearing coordinate.

For the governed LLM public path, the current bounded summary is:

```text
documentation: implemented
fixture path: available in authority repositories
Site client: prepared_not_deployed
live transport: false
same_origin_gateway: not_deployed
provider conformance: not_established
Master-Records custody: not_established
external execution: disabled_or_external
aggregate_operational: false
release_authorized: false
```

A public documentation deployment may be verified while the governed LLM service remains non-operational. Those are different capabilities and must be recorded separately.

## Required status fields

```text
capability_id
coordinate_id
owner_repository
version_or_commit
current_state
evidence_refs
evidence_hashes
observed_at
blocked_by
external_gates
operational
custody_recorded
execution_authorized
non_claims
next_evaluation
```

## Fail-closed rules

```text
missing owner -> UNKNOWN_OWNER_FAIL_CLOSED
missing version -> UNPINNED_FAIL_CLOSED
missing evidence -> EVIDENCE_MISSING_FAIL_CLOSED
source present but workflow unobserved -> IMPLEMENTED_NOT_INTERNALLY_VALIDATED
route reachable but deployment identity unknown -> REACHABLE_UNBOUND_FAIL_CLOSED
conformance absent -> NOT_OPERATIONAL
custody absent when required -> NOT_RECORDED
execution authority absent -> NO_EXECUTION
```

## Boundary

```text
status artifact != authority
example fixture != observed ecosystem state
repository validation != release authorization
wiki deployment != Site deployment
Site deployment != provider conformance
provider conformance != Master-Records custody
custody != execution authority
```

## Current status

```text
ECOSYSTEM_CAPABILITY_STATUS_MODEL_DOCUMENTED
GOVERNED_LLM_AGGREGATE_OPERATIONAL_FALSE
```
