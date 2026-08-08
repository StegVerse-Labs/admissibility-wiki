# External Framework Evaluation Workers Mirror Handoff

## Source of truth

This file is the current worker-coordination handoff for completion of the second-page external-framework evaluations in `StegVerse-Labs/admissibility-wiki`.

Parent repository source of truth remains `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`. External-framework execution and publication boundaries remain governed by `docs/external-frameworks/EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md` and issue #50. This handoff owns only the non-overlapping framework-evaluation completion lanes defined below.

## Governing goal

Complete the second-page evaluation for every actual external framework in `docs/external-frameworks/index.json` so each framework exposes, at the strongest legitimately supported evidence class:

- what the framework claims;
- what its implementation or specification actually demonstrates;
- what StegVerse Governance actually tested;
- expected versus observed results and failure classes;
- pinned sources, versions, hashes, timestamps, raw outputs, and replay commands where available;
- exact placement in the StegVerse governance chain;
- capabilities the framework does not establish;
- evidence class, standing, remaining gates, and exact external blockers.

## Baseline

```text
actual external frameworks: 36
fully completed second-page evaluations at worker activation: 0/36
companion procedure/test surfaces: broadly present
procedure/test surface presence counts as completion: false
manifest/report presence counts as completion: false
simulation-only result counts as completion: false
```

The repository's evaluation standard is `docs/external-frameworks/evaluation-standard.md`.

## Active worker lanes

### Worker A — identity and supply chain

```text
issue: #62
branch: worker/external-frameworks-identity-supplychain
claimed frameworks:
  OAuth 2.0
  OpenID Connect
  W3C Decentralized Identifiers
  W3C Verifiable Credentials
  SPIFFE/SPIRE
  in-toto
  SLSA
  Sigstore
  OpenLineage
```

### Worker B — policy and agent control

```text
issue: #63
primary branch: worker/external-frameworks-policy-agent
repair branch used for OPA closure: worker/external-frameworks-policy-agent-repair
Cedar promotion branch: worker/external-frameworks-cedar-promotion
claimed frameworks:
  Open Policy Agent
  Cedar Policy
  Guardrails AI
  NeMo Guardrails
  Llama Guard
  Model Context Protocol
  Agent2Agent Protocol
  Emergency Stop Convention
  Agent Governance Playbook
```

#### Open Policy Agent — COMPLETE_BOUNDED_OBSERVED

OPA is the first completed second-page evaluation under this worker program.

Canonical implementation/evidence commits:

```text
PR #68 -> merge commit 3831367b1de4bad41c639a215c2a106860b53cfc
PR #69 -> repair merge commit 49ae93ddc8d48476d067a606a04f190b1c2e39f4
canonical validation run: 31272895338
```

Observed bounded evidence preserved on the OPA pages:

```text
historical observed compatibility run: 29455057960
case families: 6
expected == observed: 6/6
native capture: observed
same-environment replay: observed
fresh-runner same-provider replay: observed
independent implementation reproduction: not observed
independent provider reproduction: not observed
execution authority: not granted
certification / endorsement: not established
```

Successor canonical run `31272895338` directly established that the OPA-specific closure survived current validation:

```text
EXTERNAL FRAMEWORK PAGE REMEDIATION: PASS
EXTERNAL FRAMEWORK GOVERNANCE COMPATIBILITY: PASS
compatibility_observed=1
opa_bounded_compatibility=observed_run_29455057960
open-policy-agent_case_families=6
capture-opa-evidence: SUCCESS
replay-opa-fresh-runner: SUCCESS
build-pages: SUCCESS
deploy-pages: SUCCESS
verify-public-pages: SUCCESS
```

The repository-wide canonical run remains fail-closed for unrelated tracks owned outside the OPA sub-claim, including Morrison Runtime promotion and AGCP handoff state. Those failures do not erase the directly observed OPA-specific PASS evidence and must not be reassigned to Worker B.

OPA completion state means the bounded second-page evaluation is complete at the strongest supported evidence class. It does not create a general OPA certification or claim independent reproduction.

#### Cedar Policy — CLAIMED_FOR_IMPLEMENTATION_AND_VALIDATION

Cedar is Worker B's active empirical target.

Canonical run `31272895338` produced and uploaded `cedar-selected-binary-build` artifact `9026196254`. Direct artifact inspection established:

```text
implementation: cedar-policy-cli 4.11.0
pinned/resolved commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
build command: cargo build --locked --release -p cedar-policy-cli
build exit code: 0
Cargo.lock SHA-256: 6efd3893a3c32d463748edfbd8361152e26dd17964d61bbe94cc4a390cd887b1
compiled binary SHA-256: 2f85096e819a40b90a11d45e971c9bb1f6cc1024aa20f00bfc593893d7a3b6d3
binary size: 16325032 bytes
state: BUILT_HASHED_UNEXECUTED
binary.executed_after_build: false
runtime_execution_authorized: false
external_consequence_allowed: false
source build receipt SHA-256: 0b9004042129effeb9627fc952dd0fd497095c8e042b43c36f00db0aefb259d8
promotion candidate SHA-256: b500a8d0b42eb48236e5f603c706587fe2c259af81be2408ae33f4492e41cbec
```

The generated promotion candidate was `READY_FOR_REGISTRY_PROMOTION_REVIEW`.

The current hash-only provenance transition is now installed:

```text
PR: #70
merge commit: 388d9f6dbf73cd35b8b89ebc0195b048940c1758
registry: docs/external-frameworks/implementation-selection-gates.v0.1.json
compiled_binary_sha256: 2f85096e819a40b90a11d45e971c9bb1f6cc1024aa20f00bfc593893d7a3b6d3
execution_authorized: false
current promotion receipt: reports/external-frameworks/cedar-build/cedar-binary-registry-promotion-receipt.applied-hash-only.json
Cedar page evidence posture: IMPLEMENTATION_BUILT_HASHED_UNEXECUTED
```

PR #70 also updates the Cedar second page to expose the inspected build evidence and explicitly avoids runtime, compatibility, certification, standing, or execution-authority promotion.

Canonical validation for this transition is machine-owned by workflow run `31276206898`, triggered from merge commit `388d9f6dbf73cd35b8b89ebc0195b048940c1758`. At the latest inspection the run is `pending`; no canonical PASS is claimed yet.

Exact next transition:

```text
workflow run 31276206898 reaches terminal state
-> inspect Cedar registry/promotion/provenance validators
-> if the hash-only transition validates, release the provenance sub-claim
-> invoke the existing governed Cedar authorization capture path only when its execution gate is satisfied
-> preserve request/policy/entities, raw Cedar result, runtime identity, timestamps, replay evidence, and StegVerse compatibility result
```

Cedar is not complete while no Cedar authorization decision or runtime compatibility observation has been preserved.

### Worker C — standards and risk

```text
issue: #64
branch: worker/external-frameworks-standards-risk
claimed frameworks:
  NIST AI RMF
  ISO/IEC 42001
  EU AI Act
  MITRE ATLAS
  OWASP Top 10 for LLM Applications
  OSCAL
  Policy Cards
  Runtime Governance for AI Agents
```

For non-runtime standards, the worker must not manufacture runtime evidence. Complete source/specification comparison, machine-readable crosswalks, StegVerse Governance test execution, chain placement, and explicit non-capabilities at the strongest supported evidence class.

### Worker D — bespoke and interoperability

```text
issue: #65
branch: worker/external-frameworks-bespoke-interop
claimed frameworks:
  GLM
  EVIDE
  DecisionAssure
  CARE Runtime
  KPT
  AAR
  W3C PROV
```

Where source or artifact packages are absent, complete all independently establishable source/implementation/analysis fields, record the exact blocker, and remain fail-closed for runtime/reproduction claims.

## Existing issue #50 ownership — collision boundary

The worker lanes above MUST NOT take ownership of the following active issue #50 repair tracks:

```text
MindForge
Morrison Runtime
ASRO
```

These three frameworks remain part of the 36-framework goal but are counted under issue #50 until that owner releases or transfers them.

## Coordinator

```text
issue: #66
role: 36-framework completion coordination and anti-scaffold accounting
handoff task: #67 (complete)
```

## Completion definition per framework

A framework is complete only when a reviewer can inspect the second page and determine:

1. which claims come from the framework itself;
2. which capabilities are demonstrated by an implementation/specification;
3. which tests StegVerse actually executed;
4. what inputs and expected outcomes were used;
5. what actually happened;
6. which failure classes were observed;
7. how to reconstruct or replay the result where technically possible;
8. which governance-chain layer receives the framework's artifacts or outputs;
9. which authority, standing, admissibility, commitment, execution, custody, or continuity responsibilities remain outside that framework;
10. what evidence remains missing and whether the missing evidence is local or external.

Authored procedures, fixtures, schemas, generated reports, manifests, or simulations are supporting machinery only. They do not satisfy the completion definition without corresponding observed evidence or an explicit evidence-blocked terminal posture after all locally executable work has been completed.

## Evidence-blocked terminal posture

A framework may reach `LOCAL_WORK_COMPLETE_EXTERNAL_EVIDENCE_BLOCKED` only when:

- all official sources available to StegVerse are pinned and analyzed;
- all locally executable compatibility/crosswalk tests have run and their outputs are preserved;
- governance-chain placement and non-capabilities are explicit;
- the missing external evidence is named precisely;
- no simulated or authored artifact is promoted as observed runtime evidence;
- the page identifies the exact transition that could advance the evidence class if the external dependency arrives.

This posture is not equivalent to reproduced, interoperability-tested, certified, endorsed, or execution-authorized.

## Worker process

Each worker must:

1. read this file, `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`, and `docs/external-frameworks/EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md` before mutation;
2. modify only its claimed framework set unless ownership is explicitly transferred;
3. prefer existing evaluator/capture/report machinery over duplicate implementations;
4. run the strongest available validation before requesting merge;
5. update its issue with exact evidence, remaining blockers, and framework-by-framework completion state;
6. update this handoff or issue #66 when a framework crosses a completion boundary;
7. never count page existence, file count, or generated infrastructure as completion;
8. preserve fail-closed semantics on missing evidence.

## Current accounting

```text
complete: 1/36
completed framework: Open Policy Agent
active incomplete framework records: 35/36
worker-lane incomplete records: 32/36
existing issue #50 incomplete records: 3/36
unowned: 0/36
```

Completion percentage is `2.78%` (`1/36`). Worker/issue ownership coverage remains `100%` of the 36-framework goal, but ownership coverage must never be reported as framework completion.

## Active claims and release conditions

```text
OPA sub-claim: COMPLETE; implementation/validation claim released after run 31272895338 proved OPA-specific remediation and compatibility PASS
Cedar sub-claim: CLAIMED_FOR_IMPLEMENTATION_AND_VALIDATION by Worker B / issue #63
Cedar hash-only provenance transition: MERGED; canonical validation pending run 31276206898
Cedar release condition: runtime capture/compatibility work either observed and preserved or explicitly reaches LOCAL_WORK_COMPLETE_EXTERNAL_EVIDENCE_BLOCKED after all local execution paths are exhausted
Workers A/C/D: unchanged active claims under issues #62/#64/#65
MindForge/Morrison/ASRO: unchanged issue #50 ownership
```

## Session consolidation

The originating session requirements are durably transferred here and to issues #63/#66:

```text
conversation or acknowledgment != validation
page existence != completed evaluation
generated procedure != observed test
framework completion requires claims vs actual abilities + StegVerse test evidence + governance-chain placement
```

The session may be archived only after its live Worker B execution role is released or durably transferred to another active canonical claimant with all current Cedar evidence and next actions preserved.

## Release and archive guard

```text
framework completion != repository release
worker-lane completion != 36-framework completion
36-framework completion != repository-wide validation PASS
source review != runtime observation
simulation != execution
fresh-runner same-provider replay != independent implementation reproduction
publication != standing
compatibility evidence != certification
```

Do not mark the 36-framework evaluation goal archive-ready while any worker issue #62-#65 or existing issue #50 framework track remains incomplete or evidence-blocked without a durable terminal record.
