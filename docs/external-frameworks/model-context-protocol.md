---
title: Model Context Protocol
---
# Model Context Protocol

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

MCP defines a client-server protocol for exposing context, resources, prompts, and tools to AI applications, including capability negotiation and authorization guidance.

Canonical source: https://modelcontextprotocol.io/specification/2025-06-18

Source snapshot posture: the dated protocol specification is recorded, but no pinned implementation, server package, tool registry, transport trace, authorization policy, raw call result, or independent replay receipt is attached.

## Native terms

| MCP term | Meaning here | StegVerse relationship |
|---|---|---|
| Client | Application connecting to an MCP server. | Requesting participant; not automatically an authorized actor. |
| Server | Provider of resources, prompts, or tools. | Capability source whose identity and authority must be reconstructed. |
| Tool | Callable operation advertised by a server. | Proposed capability; advertisement is not permission to execute. |
| Resource | Contextual data exposed through the protocol. | Evidence input requiring source, freshness, and custody checks. |
| Capability negotiation | Declaration of supported protocol features. | Preparation evidence; not current delegation. |

## Relationship to admissibility

```text
MCP asks: What context and capabilities can this client and server exchange?
StegVerse asks: May this specific capability invocation bind consequence now?
```

```text
tool discovered != tool authorized for this transition
capability advertised != current delegation
call prepared != commit admissible
successful response != governed consequence
```

MCP can carry capability descriptions and invocation artifacts into a governed transition path. Identity, delegation, policy, target scope, validity window, and consequence authority remain separately reconstructable.

## Observation boundary

No public StegVerse MCP execution observation is claimed.

```text
shared test vector: missing
raw protocol trace: missing
timestamp: missing
client and server configuration: missing
implementation version or hash: missing
replay commands: missing
declared expected outcome: missing
independent reproduction: missing
```

The compatibility report must remain `SOURCE_REVIEWED` until those fields are public and inspectable.

## StegVerse analysis

| Criterion | Current result |
|---|---|
| Identity | Protocol endpoints can be identified, but endpoint identity does not prove actor standing. |
| Authority | Tool availability does not establish permission for the requested action. |
| Policy | Authorization guidance may constrain access, but policy identity and current applicability must be pinned. |
| Delegation | Delegation must bind actor, tool, target, scope, and validity window outside capability discovery. |
| Evidence | Requests, responses, schemas, and errors can become evidence when retained with hashes and timestamps. |
| Replayability | Requires pinned client/server implementations, transport, schemas, configuration, and fixtures. |
| Reconstructability | Partial until tool registry, authorization inputs, call trace, and result custody are retained. |
| Failure behavior | Missing authorization, unknown tool, schema mismatch, or server error must fail closed. |
| Interoperability | MCP call artifacts can enter a Commitment Candidate as non-authorizing capability evidence. |

## Commit-time interoperability contract

```text
transition_id
actor
mcp_client_identity
mcp_server_identity
requested_tool
requested_action
target_system
tool_schema_reference
tool_registry_hash
client_version
server_version
transport_profile
authorization_reference
delegation_reference
policy_reference
request_payload_hash
response_or_error_reference
execution_context
validity_window
source_timestamp
```

## Failure classes

| Failure class | Applies | Current boundary |
|---|---:|---|
| Capability-authority collapse | Yes | Advertised capability must not become implicit permission. |
| Authority drift | Yes | Delegation may change after discovery or before invocation. |
| Stale resource evidence | Yes | Resources and tool metadata can become stale. |
| Delegation leakage | Yes | A tool may be available more broadly than the actor's current scope. |
| Replay divergence | Yes | Client, server, schema, transport, or configuration changes can alter behavior. |
| Fail-open transport error | Yes | Timeout or protocol error must not authorize fallback execution. |
| Source-claim mismatch | Yes | Advertised schema or description may not match deployed behavior. |

## Machine-readable companions

```text
manifest: docs/external-frameworks/model-context-protocol.json
compatibility report: docs/external-frameworks/reports/model-context-protocol.compatibility.json
canonical registry: docs/external-frameworks/index.json
canonical union: static/external-frameworks/canonical-union-inventory.v1.json
```

## Maintenance and challenge path

Maintenance owner: `StegVerse-Labs/admissibility-wiki`, External Frameworks audit surface.

A challenge must identify `model-context-protocol`, the disputed capability, schema, authorization claim, or source field, and the public artifact supporting correction. No challenge may increase evidence strength without a pinned implementation and replayable trace.

## Validation completion criteria

```text
pinned MCP client and server implementations
pinned tool registry and schemas
shared request vectors
predeclared expected boundaries
raw request, response, and error traces
authorization and delegation inputs
timestamps and runtime configuration
replay commands
independent rerun receipt
non-claim language preserved
```

## Benchmark relevance

`preparation_boundary`, `commitment_boundary`, `authority_boundary`, `interoperability_path`

## Non-claims

Protocol interoperability does not establish transition admissibility, current standing, execution authority, certification, or general compatibility. A successful tool call does not prove that consequence was admissible.

## Next safe build target

Attach one pinned MCP client/server fixture with a hashed tool registry, explicit authorization and delegation inputs, raw call trace, expected StegVerse boundary, replay command, and independent rerun receipt.

This page reflects a bounded admissibility packet. Publication does not create standing. The reflected claim inherits only the standing reconstructable from the referenced evidence, authority, and admissibility conditions.
