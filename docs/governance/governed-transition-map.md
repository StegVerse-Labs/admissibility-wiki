# Governed Transition Map

## Purpose

This page ties governed input classes to governed output classes through the shared StegVerse transition path.

The map is not a permission table. It shows the stages and evidence boundaries that prevent candidate inputs, generated outputs, authority decisions, execution events, and custody records from being collapsed into one undifferentiated result.

## Shared transition path

```text
input-class instance
  -> entry surface
  -> origin and identity binding
  -> governed ingestion
  -> CGE fingerprinting
  -> evidence, freshness and provenance evaluation
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> candidate result
  -> commitment request when consequence is proposed
  -> ALLOW / DENY / FAIL-CLOSED
  -> disabled or authorized execution handoff
  -> execution result, if separately authorized
  -> receipt_chain / STRP record
  -> custody and reconstruction, if separately installed
```

## Coordinate map

| Stage | Principal coordinates | Evidence posture | Authority boundary |
| --- | --- | --- | --- |
| Entry | Ecosystem Chat, Math Solver, Demo Suite, Applicability, SDK/API, repository task intake | Public, browser-local, fixture, or request packet | Entry does not grant standing. |
| Runtime production | LLM-adapter, core-node-runtime-demo, micro-node-runtime, external framework artifact | Source implementation or supplied artifact | Producer output is a candidate. |
| Contract intake | StegVerse-SDK, manifests, packet schemas, routing results | Validation and fixture evidence | Schema validity is not admissibility. |
| Formal evaluation | CGE, GCAT, BCAT, Transition Table, formalism-tests | Doctrine, executable fixture, expected outcome, proof receipt | Wiki explanation does not inherit proof authority. |
| Commitment | Commitment Candidate, policy and delegation references, authority decision | Current standing and validity window required | Historical approval is not current authority. |
| Execution | Disabled handoff by default; explicitly authorized executor externally | Separate executor evidence required | Decision is not execution. |
| Continuity | Receipts, STRP, replay and reconstruction reports | Chain and evidence references | Receipt existence is not custody. |
| Custody | Master-Records/orchestration | Authenticated installation and reconstructability evidence | Receipt handoff is not recorded custody. |
| Public explanation | admissibility-wiki and Site | Public doctrine, status and bounded display | Visibility is not proof or authority. |

## Input-to-output possibilities

| Input class | Possible bounded outputs |
| --- | --- |
| External framework artifacts | Source-reviewed record, parameterized observation, compatibility report, denial, fail-closed result, STRP handoff, bounded analysis |
| LLM or agent outputs | Informational response, action proposal, commitment request, denial, fail-closed result, disabled execution handoff, receipt continuation |
| Human requests | Informational response, proposal, commitment request, denial, fail-closed result, authorized external action when separately approved |
| Repository tasks | Patch proposal, commitment request, committed change under destination authority, denial, fail-closed result, workflow receipt |
| SDK or API requests | Intake result, quarantine, rejection, manifest binding, receipt handoff, commitment request |
| Math Solver inputs | Source record, mapping, instruction packet, artifact return, admissibility result, denial or fail-closed result |
| Demo and tester packets | Browser-local classification, fixture report, expected-versus-observed comparison; no live authority |
| Runtime observations | Health or transition record, escalation, quarantine, denial, fail-closed result, continuity record |
| Memory or KnowledgeVault candidates | Retrieval result, conflict or supersession state, quarantine, commitment request for mutation |
| Receipt-chain continuations | Chain validation result, reconstruction report, continuation candidate, denial or fail-closed result |

## Decision and consequence matrix

| Decision posture | May return information? | May create action proposal? | May execute consequence? | May claim custody? |
| --- | --- | --- | --- | --- |
| `ALLOW_INFORMATIONAL` | Yes, within scope | Only as non-authorizing candidate | No | No |
| `ALLOW_COMMITMENT` | Yes | Yes | Only through separately authorized executor | No |
| `DENY` | Bounded explanation and denial receipt | No authorized proposal crossing | No | No |
| `FAIL_CLOSED` | Bounded missing-condition explanation | No | No | No |
| `QUARANTINE` | Limited review information | Remediation candidate only | No | No |
| `EXECUTED` | Yes | N/A | Only when executor evidence exists | No, unless separately installed |
| `RECORDED` | Yes | N/A | Does not imply execution | Only with authenticated custody and reconstructability evidence |

## Completeness requirements for a concrete transition

A reviewer should be able to identify:

```text
transition identity
origin and entry coordinate
requested action or desired result
input and source hashes
policy and delegation references
evidence and freshness posture
expected boundary
candidate output
authority decision and validity window
execution handoff and execution result, if any
receipt and STRP references
custody and reconstruction posture
```

Missing stages must remain explicitly absent or fail closed; they must not be inferred from later artifacts.

## Boundary

```text
Possible output != authorized output.
ALLOW != executed.
Executed != recorded.
Recorded != currently admissible.
Replayable != reconstructable.
Reconstructable history != reusable authority.
Public map != permission table.
```

## Current status

```text
GOVERNED_TRANSITION_MAP_COMPLETE_WITH_EXTERNAL_GATES
```