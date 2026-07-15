---
title: OpenLineage
---
# OpenLineage

## Status

```text
Relationship type: external framework crosswalk
Evidence class: SOURCE_REVIEWED
Page completeness: COMPLETE_WITH_EXTERNAL_GATES
Runtime observation: none attached
Independent reproduction: false
Comparative testing claim allowed: false
Execution authority claim allowed: false
Maintenance owner: admissibility-wiki External Frameworks audit
```

## Official Source

- Project source: https://openlineage.io/
- Source posture: official project documentation captured; no producer, transport, event stream, or consumer fixture is attached.

## Framework-Native Scope

OpenLineage is an open standard for collecting metadata about datasets, jobs, and runs across data pipelines. Its event model can describe run state, job identity, dataset inputs and outputs, and extensible facets emitted by participating systems.

## Evidence Provenance

| Evidence class | Current evidence | Status | Missing fields |
|---|---|---|---|
| Official framework source | Project documentation | present | pinned specification or source snapshot hash |
| Implementation source | No producer or consumer selected | missing | release, configuration, commit |
| Observed behavior | No lineage event capture | missing | event payloads, transport, timestamps, consumer output |
| Reproduced behavior | No independent replay | missing | event stream, commands, environment, second result |
| StegVerse analysis | Bounded crosswalk | present | common event fixture |

## Relationship to Admissibility

```text
OpenLineage asks: What datasets, jobs, and runs were connected and reported across the pipeline?
StegVerse Admissibility asks: Is the reconstructed evidence sufficient and does the current actor hold authority to bind this consequence?
```

Lineage events can strengthen reconstruction and freshness review by linking data, jobs, and run events. They do not independently establish truth, legitimacy, current authority, or admissibility.

## Execution Authority Boundary

```text
lineage visibility != governance authority
reported origin != verified truth
run relationship != current delegation
event completeness != permission to bind consequence
```

## Observation Boundary

```text
Pinned producer: none
Pinned consumer: none
Event schema/version: none
Captured event stream: none
Raw consumer output: none
Timestamp and transport configuration: none
Independent replay: none
```

No lineage-capture, reconstruction, or interoperability result is claimed.

## StegVerse Analysis

| Criterion | Current result |
|---|---|
| Identity | Job, run, and dataset identifiers may be represented, but actor identity may remain external. |
| Authority | Emission or consumption of lineage events does not create execution authority. |
| Policy | Event acceptance, retention, trust, and freshness policy must be explicit. |
| Delegation | Lineage relationships do not prove delegated authority. |
| Evidence | Events may strengthen reconstruction if complete, authentic, ordered, and retained. |
| Replayability | Requires pinned schema, event stream, producer/consumer versions, and transport configuration. |
| Reconstructability | Depends on event completeness, ordering, identifiers, custody, and facet interpretation. |
| Commit-time validity | Must be evaluated independently from lineage state. |
| Failure behavior | Missing, duplicate, reordered, stale, or unverifiable events must not be treated as complete truth. |

## Commit-Time Interoperability Contract

```text
transition_id
run_id
job_namespace
job_name
event_type
event_time
input_dataset_ids
output_dataset_ids
facet_digests
producer_identity
schema_version
event_digest
custody_reference
freshness_state
policy_reference
delegation_reference
requested_action
target_system
```

## Failure Classes

| Failure class | Applies | Notes |
|---|---:|---|
| Semantic equivalence divergence | yes | Recorded lineage may be mistaken for causal proof. |
| Stale evidence | yes | Events can lag behind current pipeline state. |
| Replay divergence | yes | Different ordering, schema handling, or facets may alter reconstruction. |
| Recoverability loss | yes | Missing event segments can make the chain incomplete. |
| Source-claim mismatch | yes | Producer-reported events may exceed what was independently verified. |
| Evidence-class confusion | yes | Source review must not be described as observed lineage behavior. |

## Machine-Readable Companions

- Manifest: `docs/external-frameworks/openlineage.json`
- Compatibility report: `docs/external-frameworks/reports/openlineage.compatibility.json`
- Registry: `docs/external-frameworks/index.json`
- Canonical inventory: `static/external-frameworks/canonical-union-inventory.v1.json`

## Validation Completion Criteria

```text
pin one producer, transport, and consumer
publish a bounded lineage event fixture
capture raw emitted and consumed events with timestamps
publish ordering, custody, expected result, and replay commands
complete an independent replay
route reconstructed lineage evidence into a Commitment Candidate
```

## Non-Claims

OpenLineage is not a StegVerse canonical formalism. Lineage visibility and recorded origin are not truth, legitimacy, current authority, transition admissibility, certification, or general compatibility.

## Challenge Path

A challenge must identify the run, job, dataset, event or facet, disputed relationship, supporting evidence, and requested correction. Reported lineage receives only the standing supported by reconstructable custody and provenance.

## Next Safe Build Target

Publish one pinned producer-to-consumer event fixture with raw events, ordering and custody evidence, immutable hashes, replay instructions, and an independent replay.

This page reflects a bounded admissibility packet. Publication does not create standing.