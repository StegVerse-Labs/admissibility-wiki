# Governed Input Classes

## Purpose

This page is the public registry of input classes that may enter StegVerse as governed transition candidates.

Registration means the ecosystem recognizes the class and can define an intake boundary for it. Registration does not mean every instance is supported, admissible, trusted, deployed, or authorized to produce consequence.

## Shared intake path

```text
input or request
  -> entry surface
  -> governed ingestion
  -> identity and origin binding
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output candidate
```

## Registered input classes

| Input class | Example entry coordinates | Canonical evidence or authority source | Current posture |
| --- | --- | --- | --- |
| External framework artifacts | External Frameworks intake, compatibility reports, supplied traces | Official framework sources, pinned artifacts, generated compatibility reports | `REGISTERED_EVIDENCE_VARIES` |
| LLM or agent outputs | Ecosystem Chat, LLM-adapter, agent/runtime producers | Adapter session packets, provider or fixture references, policy and authority records | `FIXTURE_PROVEN_LIVE_EXTERNAL_GATES` |
| Human requests | Ecosystem Chat, proposal intake, direct governed request surfaces | Request envelope, identity/session context, explicit scope and desired consequence | `REGISTERED_ENTRY_SURFACES_VARY` |
| Repository tasks and build artifacts | GitHub issues, task packets, patches, workflow artifacts, manifests | Repository handoff, commit, workflow receipt, destination authority | `ACTIVE_REPOSITORY_GOVERNANCE` |
| SDK or API requests | StegVerse-SDK, adapter clients, same-origin gateway contract | SDK schema, intake result, manifest, receipt handoff | `IMPLEMENTED_PENDING_LIVE_ROUTE_EVIDENCE` |
| Math Solver inputs | Site Math Solver source, mapping, generation, and result surfaces | Source records, mapping records, generated instruction packet, artifact return | `PUBLIC_CONCEPT_AND_FIXTURE_PATH` |
| Demo and applicability tester packets | Governance Demo Suite, dynamic demo, applicability tester | Test manifest, tester packet, expected boundary, generated result | `BROWSER_OR_FIXTURE_ONLY` |
| Runtime observations | Core-node runtime demo, monitoring and observation artifacts | Timestamped trace, version, configuration, runtime receipt | `REGISTERED_EVIDENCE_REQUIRED` |
| Memory or KnowledgeVault candidates | Reconstructive-search and continuity intake | Source pointers, hashes, timestamps, policy, delegation and custody posture | `DOCTRINE_PRESENT_SERVICE_EXTERNAL` |
| Receipt-chain continuations | Prior receipts, STRP records, continuation packets | Prior record identity, chain validation, current policy and standing | `REGISTERED_CURRENT_STANDING_REQUIRED` |
| External retrieval evidence | Continuity or reconstructive search responses | Source pointers, retrieval time, freshness, supersession and conflict state | `SERVICE_EXTERNAL_FIXTURE_EXPLAINED` |

## Required instance fields

Where applicable, an input instance should identify:

```text
input_class
origin
producer or actor
entry_surface
requested action or desired output
scope
timestamp and validity window
source or payload hash
policy reference
delegation or authority reference
evidence references
privacy and custody posture
expected consequence boundary
```

Missing required fields must produce quarantine, rejection, or `FAIL_CLOSED`; they must not be silently inferred into authority.

## Machine-readable support

Machine-readable support may exist in the source repository rather than this wiki. Examples include:

```text
adapter session packets
SDK intake and manifest schemas
framework compatibility reports
math-solver instruction and artifact templates
tester-output packets
workflow receipts
STRP or continuation records
```

The wiki is the public registry and explanation layer. It does not become the canonical source merely by linking to an artifact.

## Boundary

```text
Registered class != supported instance.
Supported instance != admissible transition.
Source availability != truth.
Fixture success != live service activation.
Prior receipt != current standing.
Input acceptance != execution authority.
```

Each instance must pass the applicable governed ingestion, evidence, policy, authority, recoverability, and commitment requirements before it can become consequence-bearing state.

## Current status

```text
GOVERNED_INPUT_CLASS_REGISTRY_COMPLETE_WITH_EXTERNAL_GATES
```