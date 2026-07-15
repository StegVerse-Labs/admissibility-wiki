---
title: Agent2Agent Protocol
---
# Agent2Agent Protocol

## Evidence posture

```text
evidence_class: SOURCE_REVIEWED
page_completeness: COMPLETE_WITH_EXTERNAL_GATES
runtime_observation: none attached
independent_reproduction: false
comparative_testing_claim_allowed: false
execution_authority_claim_allowed: false
```

## Published scope

A2A defines agent interoperability concepts for discovery through Agent Cards, messages, tasks, artifacts, completion, failure, and authenticated interactions.

Canonical source: https://a2a-protocol.org/latest/specification/

Source snapshot posture: the protocol specification is recorded, but no pinned agent implementation, Agent Card, task trace, authentication exchange, artifact custody record, or independent replay receipt is attached.

## Native terms

| A2A term | Meaning here | StegVerse relationship |
|---|---|---|
| Agent Card | Description of an agent and its skills or endpoint. | Discovery evidence; not proof of current authority. |
| Task | Stateful unit of work exchanged between agents. | Proposed transition or work packet requiring separate admissibility. |
| Message | Communication within a task. | Evidence input; not an authorization grant. |
| Artifact | Output associated with task progress or completion. | Result evidence requiring provenance and custody. |
| Task state | Submitted, working, completed, failed, or similar status. | Workflow state; not consequence-binding standing. |

## Relationship to admissibility

```text
A2A asks: How can agents discover one another and exchange tasks and artifacts?
StegVerse asks: Did the acting agent have current authority for this specific consequence?
```

```text
agent discovered != trusted for every action
task accepted != consequence authorized
task completed != transition admissible
artifact returned != governed result accepted
```

Agent discovery and task exchange can enter the StegVerse path as proposed interaction evidence. Delegation, current standing, target scope, recoverability, and consequence authority remain separately evaluated.

## Observation boundary

No public StegVerse A2A runtime observation is claimed.

```text
shared task vector: missing
raw messages and task events: missing
timestamp: missing
agent configuration: missing
implementation version or hash: missing
replay commands: missing
declared expected outcome: missing
independent reproduction: missing
```

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | Agent Cards and authenticated channels may identify endpoints; identity does not prove standing. |
| Authority | Task acceptance or completion does not establish authority to bind consequence. |
| Policy | Policy remains external unless explicitly referenced and pinned in the task envelope. |
| Delegation | Delegation must bind agent, skill, target, scope, and validity window. |
| Evidence | Messages, task transitions, artifacts, and errors can become evidence when retained. |
| Replayability | Requires pinned agents, cards, task inputs, authentication state, and transport behavior. |
| Reconstructability | Partial until all task state transitions and artifact custody are retained. |
| Failure behavior | Unknown agent, invalid task state, missing delegation, or artifact mismatch must fail closed. |
| Interoperability | A2A task records can become Commitment Candidate evidence, not inherited authority. |

## Commit-time interoperability contract

```text
transition_id
requesting_actor
requesting_agent_id
responding_agent_id
agent_card_reference
agent_card_hash
requested_skill
requested_action
target_system
task_id
task_input_hash
authentication_reference
delegation_reference
policy_reference
task_state_history
artifact_references
artifact_hashes
execution_context
validity_window
source_timestamp
```

## Failure classes

| Failure class | Applies | Current boundary |
|---|---:|---|
| Agent identity ambiguity | Yes | Agent Card identity may not equal current controller or operator. |
| Authority drift | Yes | Delegation can expire while a task remains active. |
| Delegation leakage | Yes | A declared skill may exceed the task's authorized scope. |
| Task-state confusion | Yes | Completion state may be mistaken for admissibility. |
| Artifact substitution | Yes | Returned artifacts require hashes and custody evidence. |
| Replay divergence | Yes | Agent implementations and external services can alter outcomes. |
| Fail-open interaction error | Yes | Failed or indeterminate tasks must not authorize consequence. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/agent2agent-protocol.json
compatibility report: docs/external-frameworks/reports/agent2agent-protocol.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `agent2agent-protocol`, the disputed Agent Card, task state, delegation, artifact, or source field, and public evidence supporting correction. Evidence strength cannot increase without a pinned and replayable task exchange.

## Validation completion criteria

```text
pinned agent implementations and Agent Cards
shared task vectors
predeclared expected boundaries
raw messages and task-state events
artifact hashes and custody records
authentication, policy, and delegation inputs
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`preparation_boundary`, `commitment_boundary`, `authority_boundary`, `interoperability_path`

## Non-claims

Protocol completion does not create StegVerse standing, certification, equivalence, execution authority, or general compatibility. A completed task is not proof that the resulting consequence was admissible.

## Next safe build target

Attach one pinned two-agent task fixture with Agent Cards, delegation, raw state transitions, artifact hashes, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from the referenced evidence, authority, and admissibility conditions.
