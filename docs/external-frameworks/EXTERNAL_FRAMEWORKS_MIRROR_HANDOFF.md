# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff and continuation source of truth for Goal 5 external-framework intake, evidence capture, implementation selection, binary build and promotion, readiness, execution planning, materialization, runtime authorization, dispatch observation, replay, and publication work in `StegVerse-Labs/admissibility-wiki`.

Preserve unrelated CI repair, conceptual-inheritance, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

## Current goal

```text
Goal: evidence-bound external-framework intake through observed, replayable, non-authorizing interoperability evidence
Phase: Cedar hash-only registry promotion applied; canonical validation passed; bounded OPA capture repair installed and awaiting successor verification
Result: CANONICAL_VALIDATION_PASS_OPA_CAPTURE_REPAIR_PENDING
```

## Current state

```text
registered framework and crosswalk entries: 19
candidate intake records: 42
visible observatory entries: 61
sourced-intake pages: 18
benchmark mappings: 18 of 18
non-authorizing fixtures: 18 of 18
priority capture queue entries: 7 of 7
capture harnesses: 7 of 7
artifact validators: 7 of 7
implementation-selection gates: installed
Cedar pinned build-and-hash automation: installed and observed passing
Cedar build-receipt inspection: completed for run 29205883335
Cedar binary registry-promotion receipts: APPROVED_NOT_APPLIED and APPLIED_HASH_ONLY installed
Cedar compiled binary SHA-256 registry field: applied
runtime execution authorized by promotion: false
dispatch-state fixture coverage: 4 of 4
dispatch-observation hash-chain validation: installed
canonical validation chain: PASS on run 29208976626
runtime jobs emitted by plan automation: 0
OPA observed external outputs: pending successor verification after bounded version-probe repair
independent organization/provider replays: 0 of 18
```

## Validation-critical observed-evidence references

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
```

The queue remains `AWAITING_CAPTURE_NOT_OBSERVED_EVIDENCE` until exact source, version or commit, input, output, timestamp, environment, policy/configuration, authority context, freshness context, hashes, replay instructions, and limitations are attached.

## Governed transition chain

```text
fixture_ready
-> awaiting_implementation_selection
-> implementation_selected_hash_bound
-> selected_binary_build_hashed_unexecuted
-> binary_build_receipt_inspection
-> registry_promotion_review
-> hash_only_registry_promotion_if_approved
-> automation_readiness_review
-> eligible_for_execution_job_materialization
-> governed_job_materialization_receipt
-> materialized_non_executable_descriptor
-> separate_runtime_authorization_review
-> commit_time_predicate_revalidation
-> authorized_not_dispatched_runtime_transition
-> separate_observed_runtime_dispatch_transition
-> dispatch_observation
-> awaiting_capture
-> captured_unverified
-> replay_confirmed_same_environment
-> replay_confirmed_independent_environment_fresh_runner
-> independent_implementation_or_provider_review
-> observed_partial
-> interoperability_candidate
```

No stage advances merely because tooling, a schema, fixture, plan, authorization, promotion receipt, or observation record exists.

## Cedar evidence-bound hash promotion

Observed workflow evidence:

```text
Workflow: Validate chain continuation
Run: 29205883335
Commit: 9e60f52f01f5e981baf4fd5c55a9a5a6e199e25c
Job: build-selected-cedar-binary
Result: PASS
Artifact: cedar-selected-binary-build
Artifact ID: 8263766611
Artifact digest: sha256:cff4fbf627776db206c9f1f66281bf03a2c732709d29fa7682e56b99923b61dc
Pinned Cedar commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
Binary SHA-256: 96e6b0517f145875c12457f3350ad43fdc3be9f0e32c42ce813df0667fa036e1
Build receipt SHA-256: edd03d9e5334009674916586ba27045309f006435b623f38f89da2fa3cf015d1
Promotion candidate SHA-256: 1324a6a9b83b19c30f674c6b93de2e71b46d64ac485419f480a60c1061558468
Build state: BUILT_HASHED_UNEXECUTED
```

Installed governed progression:

```text
7c7a7b4436a9c01a30f71a531b64b5a55da354d4
  -> evidence-bound APPROVED_NOT_APPLIED receipt
8e19046a83b9387089eb11156d5e5589b9073177
  -> only frameworks[cedar-policy].selection.compiled_binary_sha256 changed
3aacddfd9358d7bd8b214c7f771d084f0e9785b2
  -> APPLIED_HASH_ONLY receipt
```

The promoted hash does not establish compatibility, standing, execution authority, dispatch authority, consequence authority, certification, or admissibility. `execution_authorized` remains false.

## Dispatch observation progression

Installed:

```text
tests/fixtures/external-framework-runtime-dispatch-observation.not-dispatched.json
tests/fixtures/external-framework-runtime-dispatch-observation.dispatch-attempted.json
tests/fixtures/external-framework-runtime-dispatch-observation.dispatched.json
tests/fixtures/external-framework-runtime-dispatch-observation.execution-observed.json
tests/fixtures/external-framework-runtime-dispatch-observation-chain.json
scripts/check_external_framework_runtime_dispatch_observation.py
scripts/check_external_framework_runtime_dispatch_progression.py
```

The progression validator checks canonical order, prior receipt identity and SHA-256, strictly increasing observation time, framework and transition continuity, and fail-closed authority boundaries. Fixture progression is not observed production execution and cannot initiate dispatch, attach credentials, execute a command, or create an external consequence.

## Canonical validation completion

```text
Workflow: Validate chain continuation
Run: 29208976626
Commit: 48e9eead987a77701582807e0a9b1fc6b20980a8
Job: validate-chain-continuation
Result: PASS
Complete validation result enforcement: PASS
Goal 5 aggregate generation and upload: PASS
Cedar selected-binary build: PASS
```

This verifies the documented successor to `397c5d376ad68a1f1cc6da5e812418a097321637` and closes the prior handoff-reference regression. It does not establish OPA capture, replay, compatibility, execution authority, deployment, or release.

## OPA capture failure and bounded repair

The first post-validation OPA capture failure was confirmed in run `29208976626`:

```text
Job: capture-opa-evidence
Failing command: python scripts/run_pinned_opa_ci_capture.py
Pinned runtime: OPA v1.0.0 static Linux AMD64
Failure: Error: unknown flag: --format
Rejected invocation: opa_linux_amd64_static version --format=json
Capture artifact ID: 8264578155
Capture artifact digest: sha256:fc646130fcccb80779bb5a28acf18b5a0b16a6600fcdcb48b1e87adb430534cc
Generated capture files: absent because capture exited during version probing
```

Bounded repair:

```text
Commit: 1ab96f779a4cf457bdd98753a41c1648114461d3
File: scripts/run_pinned_opa_ci_capture.py
Change: use supported `opa version`, preserve raw version output, and fail closed unless output contains pinned version 1.0.0
```

The repair does not change the pinned version, checksum verification, OPA policy/input cases, output comparison, authority boundaries, workflow permissions, execution authority, release state, deployment state, or external repositories.

## Canonical integration

```text
Aggregate: scripts/check_goal5_external_frameworks_all.py
Canonical workflow: .github/workflows/validate-chain-continuation.yml
iOS mirror: iosnoperiod/github/workflows/validate-chain-continuation.yml
Additional active workflow created: no
```

## Next task

```text
1. Verify the canonical successor run for commit 1ab96f779a4cf457bdd98753a41c1648114461d3.
2. Require capture-opa-evidence and generated-artifact validation to pass before advancing.
3. Preserve the OPA capture artifact, exact hashes, environment, inputs, outputs, policy/configuration, and same-environment replay receipt.
4. Verify same-environment replay before accepting fresh-runner replay.
5. Inspect any remaining build-pages activation-artifact failure separately; do not weaken activation or deployment gates.
6. Perform replay outside the same repository/provider before any stronger independence claim.
7. Publish observed-partial reports only after exact evidence exists.
8. Capture public deployment and downstream propagation receipts before updating destination repositories.
```

## Remaining files or modules

```text
StegVerse-Labs/admissibility-wiki
  -> successor verification for bounded OPA version-probe repair
  -> successful OPA capture artifacts and same-environment replay receipt
  -> successful fresh-runner replay receipt
  -> build-pages activation-artifact diagnosis without gate weakening
  -> public deployment verification receipt

Independent organization/provider
  -> independent OPA replay or implementation review

StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-002/stegguardian-wiki
  -> destination-handoff review before any propagation
```

## Authority and release boundary

```text
binary build != runtime execution
binary hash != compatibility proof
promotion approval != mutation applied
registry hash promotion != execution authority
runtime authorization != dispatch
dispatch attempted != dispatched
dispatched != execution observed
execution observed != compatibility
observation receipt != authority
same-environment replay != independent replay
replay confirmation != execution authority
```

No deployment, release, tag, merge, external-repository mutation, runtime execution, credential attachment, dispatch, or public activation claim is authorized by this handoff. No release tag is authorized solely from schema, fixture, validation, promotion, capture, or automation installation.

## Archive readiness

This handoff preserves the current Cedar build evidence, hash-only promotion receipts, dispatch progression chain, canonical validation success, exact OPA capture failure, bounded version-probe repair, authority boundaries, remaining modules, and ordered continuation task. Earlier conversation context is not required.
