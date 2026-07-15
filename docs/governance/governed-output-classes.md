# Governed Output Classes

## Purpose

This page is the public registry of output classes for governed transition results.

A desired output is not valid merely because it can be requested, generated, displayed, or technically executed. It remains a candidate until the applicable commitment boundary establishes current standing and binds the result to evidence and receipts.

## Core output path

```text
admitted input or request
  -> governed evaluation
  -> candidate result
  -> current authority and policy check
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> bounded output disposition
  -> optional authorized consequence
```

## Registered output classes

| Output class | Required boundary | Typical destination | Current posture |
| --- | --- | --- | --- |
| Informational response | Evidence and scope sufficient; no consequence-bearing authority inferred | User or requesting interface | `SUPPORTED_BOUNDED_RESPONSE` |
| Action proposal | Explicitly remains non-authorizing | Commitment-candidate or review path | `SUPPORTED_NON_EXECUTING` |
| Commitment request | Current policy, delegation, evidence and recoverability must be evaluated | Authority decision surface | `SUPPORTED_NON_AUTHORIZING_REQUEST` |
| Authority decision | Decision must identify standing, scope, policy and validity window | Governed transition record | `SCHEMA_OR_FIXTURE_SUPPORTED` |
| Disabled execution handoff | Must state that no side effect occurred | Authorized executor boundary | `DEFAULT_FIXTURE_POSTURE` |
| Denial receipt | Denial reason and governing evidence must be preserved | Originating path and continuity record | `REGISTERED` |
| Fail-closed receipt | Missing or invalid authority, evidence, identity, policy or standing must be named | Originating path and continuity record | `REGISTERED` |
| Quarantine result | Unresolved conflict, provenance, privacy, freshness or custody condition | Review or remediation queue | `REGISTERED` |
| Committed repository change | Destination handoff and repository mutation authority required | Authorized repository and commit history | `EXTERNAL_TO_WIKI_AUTHORITY` |
| External communication | Recipient, content, authority and consequence boundary required | Email, social, API or messaging surface | `EXPLICIT_AUTHORITY_REQUIRED` |
| Memory or KnowledgeVault mutation | Current consent, policy, provenance and custody required | Authorized memory service | `SERVICE_EXTERNAL` |
| STRP handoff | Transition identity, result, hashes, authority and continuity fields required | Next governed entity or system | `CONTRACT_OR_FIXTURE_SUPPORTED` |
| Receipt-chain continuation | Prior chain validity plus current standing required | Continuity or Master-Records path | `REGISTERED_CURRENT_VALIDATION_REQUIRED` |
| State-transition summary | Must remain a bounded explanation rather than proof authority | Public or reviewer-facing surface | `SUPPORTED_PUBLIC_EXPLANATION` |
| Custody record | Authenticated installation and reconstructability evidence required | Master-Records/orchestration | `EXTERNAL_NOT_CREATED_BY_WIKI` |

## Required result distinctions

Every result surface should distinguish, where applicable:

```text
candidate_output
admitted_informational_response
action_proposal
commitment_request
authority_decision
execution_handoff
execution_result
custody_result
reconstruction_result
```

Collapsing these stages into a single “success” state obscures whether anything was authorized, executed, recorded, or independently reconstructable.

## Machine-readable support

Relevant machine-readable artifacts may include:

```text
governed session packet
intake result
commitment request
authority decision
disabled execution handoff
denial or fail-closed receipt
manifest and receipt handoff
STRP record
custody receipt
reconstruction report
```

The artifact must identify its producer and scope. A generated file does not inherit authority merely because it conforms to a schema.

## Boundary

```text
Generated output != admitted output.
Admitted response != action authority.
Commitment request != authority decision.
Authority decision != execution evidence.
Execution evidence != custody.
Receipt handoff != Master-Records installation.
Historical reconstruction != current admissibility.
```

## Current status

```text
GOVERNED_OUTPUT_CLASS_REGISTRY_COMPLETE_WITH_EXTERNAL_GATES
```