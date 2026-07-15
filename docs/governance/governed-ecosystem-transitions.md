# Governed Ecosystem Transitions

## Purpose

This page frames StegVerse as a governed transition ecosystem for inputs, proposed actions, desired outputs, consequence-bearing execution, and receipt-bound continuity.

External frameworks are one input class. LLM outputs, human requests, repository tasks, SDK packets, Math Solver artifacts, runtime observations, memory candidates, and prior receipts are additional classes that enter the same high-level governance grammar.

## Core claim

```text
StegVerse governs how candidate information and proposed actions may become bounded transitions.
It does not treat generation, display, validation, approval, execution, or recording as interchangeable states.
```

## Complete transition path

```text
input or request
  -> entry surface
  -> origin, identity and scope binding
  -> governed ingestion
  -> CGE fingerprinting
  -> source, provenance and freshness evaluation
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> candidate output or action proposal
  -> commitment request when consequence is proposed
  -> ALLOW / DENY / FAIL-CLOSED / QUARANTINE
  -> disabled or separately authorized execution handoff
  -> execution result, if any
  -> receipt_chain / STRP record
  -> authenticated custody and reconstruction, if separately installed
```

## Ecosystem coordinates

| Coordinate group | Examples | Current relationship to this page |
| --- | --- | --- |
| Public entry | Ecosystem Chat, Math Solver, Governance Demo Suite, Applicability, proposal intake | Public, browser-local, fixture, or prepared entry surfaces |
| Runtime production | LLM-adapter, core-node-runtime-demo, micro-node-runtime, external artifacts | Produces candidate packets or observations; not authority by itself |
| Contract intake | StegVerse-SDK, manifests, intake and receipt schemas | Validates and routes artifacts without granting authority |
| Formal evaluation | CGE, GCAT, BCAT, Transition Table, formalism-tests | Determines or proves bounded standing where executable evidence exists |
| Commitment and execution | Commitment request, authority decision, executor handoff | Requires current standing and separately authorized consequence binding |
| Continuity and custody | Receipts, STRP, replay, reconstruction, Master-Records | Preserves transition history; custody remains a separate authenticated event |
| Public explanation | admissibility-wiki and Site | Explains status and topology without inheriting implementation or proof authority |

## Governed input classes

The registry includes:

```text
external framework artifacts
LLM or agent outputs
human requests and corrections
repository tasks and workflow artifacts
SDK or API requests
Math Solver source and mapping artifacts
demo or applicability tester packets
runtime observations
memory or KnowledgeVault candidates
external retrieval evidence
receipt-chain continuations
```

See [Governed Input Classes](./governed-input-classes.md) for entry coordinates, evidence ownership, and current posture.

## Governed output classes

Possible bounded outputs include:

```text
informational response
action proposal
commitment request
authority decision
disabled execution handoff
denial or fail-closed receipt
quarantine result
committed repository change under destination authority
external communication under explicit authority
memory mutation under current consent and policy
STRP handoff
receipt-chain continuation
state-transition summary
authenticated custody record
```

See [Governed Output Classes](./governed-output-classes.md) for the required boundary at each stage.

## Decision does not collapse consequence

| State | What it means | What remains unproven |
| --- | --- | --- |
| Candidate generated | A system produced a possible result | Admissibility, authority, execution and custody |
| Validated | Structure or contract passed a validator | Current standing and authority |
| `ALLOW_INFORMATIONAL` | A bounded response may be returned | Authority to perform an action |
| `ALLOW_COMMITMENT` | A proposed consequence may cross to an authorized executor | That execution occurred |
| `DENY` | The transition is not allowed under the evaluated standing | Historical deletion or impossibility of later reconsideration |
| `FAIL_CLOSED` | Required conditions are absent or invalid | Framework invalidity or permanent denial |
| Executed | A separately authorized consequence occurred | Master-Records custody or current future authority |
| Recorded | Authenticated custody and reconstruction conditions passed | Current admissibility for reuse |

## Relationship to external frameworks

```text
external framework artifact
  -> native claim and source preservation
  -> governed ingestion
  -> evidence classification
  -> applicable shared test or crosswalk
  -> commitment candidate when consequence is proposed
  -> bounded decision and receipt
```

A framework mention, source review, author comment, or compatibility report is not automatically comparative testing. Reproducible comparison requires common vectors, pinned versions, declared expectations, raw outputs, scoring, replay instructions, hashes, and independent reproduction.

## Relationship to governed LLMs and reconstructive search

A governed LLM participates as a reasoning and retrieval coordinate. Reconstructive search should establish what evidence state existed at an earlier time, what changed, and what remains historically reconstructable without treating the earlier result as current authority.

```text
historically reconstructable != currently admissible
receipt-backed != true
replayable != reconstructable
reconstructable != authenticated custody
```

## Relationship to repository work

A repository task becomes consequence-bearing only after destination authority is established.

```text
task or patch proposal
  -> repository handoff check
  -> evidence and scope review
  -> destination mutation authority
  -> commit or fail-closed result
  -> workflow receipt
```

A source repository cannot infer mutation authority over Site, Publisher, StegGuardian, Master-Records, or another destination merely because a propagation need is documented.

## Relationship to STRP and continuity

STRP is a transition-record handoff layer. A useful record should preserve:

```text
transition identity
origin and request
input and evidence hashes
policy and delegation references
decision and validity window
execution posture and result
receipt chain
custody and reconstruction posture
```

STRP transfer does not itself prove installation, acceptance, or current standing at the destination.

## Current implementation posture

```text
public doctrine and registry pages: PRESENT
fixture-first adapter and SDK paths: IMPLEMENTED IN SOURCE REPOSITORIES
Math Solver and demo surfaces: PUBLIC CONCEPT / FIXTURE / BROWSER POSTURES
Site live same-origin usage path: PREPARED_NOT_DEPLOYED
live continuity-search service: EXTERNAL
Master-Records custody: EXTERNAL
external executor authority: EXTERNAL
canonical workflow and Pages evidence: REPOSITORY-OWNED OBSERVATION GATES
```

## Boundary

```text
Input registration != admissibility.
Generation != validation.
Validation != standing.
Standing decision != execution.
Execution != custody.
Custody != current reuse authority.
Receipt != truth.
Public framing != proof authority.
Queued propagation != completed downstream mutation.
```

## Current status

```text
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_COMPLETE_WITH_EXTERNAL_GATES
```