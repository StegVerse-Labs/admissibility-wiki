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
branch: worker/external-frameworks-policy-agent
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

OPA is the leading empirical candidate in this lane. Existing native execution and replay evidence must be preserved. Its pending canonical StegVerse governance-compatibility execution/receipt gate must be closed before stronger claims are made.

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
handoff task: #67
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
complete: 0/36
active worker-owned: 33/36
existing issue #50 owned: 3/36
unowned: 0/36
```

Completion percentage is therefore `0%` at worker activation. Worker deployment/claim coverage is `100%` of the 36-framework goal, but claim coverage must never be reported as framework completion.

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
