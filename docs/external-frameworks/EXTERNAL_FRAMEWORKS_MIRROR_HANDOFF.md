# External Frameworks Mirror Handoff

## Source of truth

This file is the current handoff and continuation source of truth for Goal 5 external-framework intake, evidence capture, implementation selection, binary build and promotion, readiness, execution planning, materialization, runtime authorization, dispatch observation, replay, and publication work in `StegVerse-Labs/admissibility-wiki`.

Preserve unrelated CI repair, conceptual-inheritance, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

## Current goal

```text
Goal: evidence-bound external-framework intake through observed, replayable, non-authorizing interoperability evidence
Phase: Cedar hash-only registry promotion applied; dispatch progression installed; canonical revalidation pending
Result: LOCAL_IMPLEMENTATION_INSTALLED_CANONICAL_AND_OPA_VALIDATION_PENDING
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
runtime jobs emitted by plan automation: 0
OPA observed external outputs: pending successful capture
independent organization/provider replays: 0 of 18
```

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

## Latest canonical failure and bounded repair

```text
Workflow: Validate chain continuation
Run: 29206548078
Commit: 3dc11143ee077fcaf5b12a498e620bb508f125ac
Job: validate-chain-continuation
First failing step: Enforce complete validation result
Full-validation artifact: 8263908851
Artifact digest: sha256:9299517ce7dea63198435ce498dd33cb3a6f405a4a6f8b585759404e28d2bcd1
Aggregate result: 32 of 34 Goal 5 checks passed
Failure class: stale pre-promotion compiled-binary-null assertions
```

Bounded repairs:

```text
95df392f5e3de3c5a5fac3fadbd09023289b7b59
  -> implementation-selection gate accepts only evidence-bound Cedar APPLIED_HASH_ONLY state
7b4f3f7d104860c678a0927afd98e7d420eeb831
  -> Cedar selection evidence binds the registry hash to the applied promotion receipt
```

Both validators continue to require `execution_authorized=false`, a valid lowercase SHA-256, the exact Cedar registry field, a ready candidate, delegated review PASS, `APPLIED_HASH_ONLY`, and no external consequence.

## OPA blocker

Run `29205883335` produced no OPA capture or replay records. The preserved artifacts show capture validation failed because expected generated files were absent; the fresh-runner replay then failed closed because validated upstream artifacts were unavailable.

```text
capture artifact: opa-pinned-capture-replay
artifact ID: 8263746209
artifact digest: sha256:52254577fef3e4f9a0fc242388bedcf3fb753166bdcc486c817b43b021ca602b
fresh-runner artifact: opa-fresh-runner-replay
artifact ID: 8263747567
artifact digest: sha256:19c85b972bef2775ff627c48819a088552cce24805dca5b27b2353ab5bc579c7
```

The failure occurs before a validated capture is produced. Do not claim same-environment or fresh-runner replay success until receipts exist and validate.

## Canonical integration

```text
Aggregate: scripts/check_goal5_external_frameworks_all.py
Canonical workflow: .github/workflows/validate-chain-continuation.yml
iOS mirror: iosnoperiod/github/workflows/validate-chain-continuation.yml
Additional active workflow created: no
```

## Next task

```text
1. Verify the canonical Goal 5 aggregate and full validation chain on commit 7b4f3f7d104860c678a0927afd98e7d420eeb831 or a documented successor.
2. Preserve the passing full-validation and Goal 5 receipts.
3. If canonical validation passes, inspect the next OPA capture job logs and artifacts.
4. Apply only a bounded OPA acquisition/capture robustness repair after the first failure is confirmed.
5. Verify same-environment replay before fresh-runner replay.
6. Perform replay outside the same repository/provider before any stronger independence claim.
7. Publish observed-partial reports only after exact evidence exists.
8. Capture public deployment and downstream propagation receipts before updating destination repositories.
```

## Remaining files or modules

```text
StegVerse-Labs/admissibility-wiki
  -> current-main canonical validation receipts
  -> bounded OPA acquisition/capture diagnosis and repair
  -> successful same-environment replay receipt
  -> successful fresh-runner replay receipt
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
replay confirmation != execution authority
```

No deployment, release, tag, merge, external-repository mutation, runtime execution, credential attachment, dispatch, or public activation claim is authorized by this handoff. No release tag is authorized solely from schema, fixture, validation, promotion, or automation installation.

## Archive readiness

This handoff preserves the current Cedar build evidence, hash-only promotion receipts, dispatch progression chain, canonical failure and repairs, OPA blockers, authority boundaries, remaining modules, and ordered continuation task. Earlier conversation context is not required.
