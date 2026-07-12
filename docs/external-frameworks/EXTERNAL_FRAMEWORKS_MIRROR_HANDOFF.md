# External Frameworks Mirror Handoff

## Source of truth

This file is the current continuation source of truth for Goal 5 external-framework intake, evidence capture, implementation selection, binary build and promotion, readiness, execution planning, runtime authorization, dispatch observation, replay, and publication work in `StegVerse-Labs/admissibility-wiki`.

Preserve unrelated CI repair, conceptual-inheritance, lifecycle-formalism, inference-window, and documentation-mesh work owned by other workstreams.

## Current goal

```text
Goal: evidence-bound external-framework intake through observed, replayable, non-authorizing interoperability evidence
Phase: same-environment OPA capture and replay observed passing; bounded fresh-runner version-probe repair installed
Result: SAME_ENVIRONMENT_REPLAY_PASS_FRESH_RUNNER_REPAIR_PENDING
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
Cedar pinned build-and-hash automation: observed passing
Cedar hash-only registry promotion: APPLIED_HASH_ONLY
runtime execution authorized by promotion: false
dispatch-state fixture coverage: 4 of 4
dispatch-observation hash-chain validation: installed
canonical validation chain: PASS on run 29209776393
OPA capture and same-environment replay: PASS on run 29209776393
fresh-runner replay: bounded repair installed; successor verification pending
build-pages activation-artifact validation: FAIL; diagnosis pending
runtime jobs emitted by plan automation: 0
independent organization/provider replays: 0 of 18
```

## Validation-critical references

```text
docs/external-frameworks/observed-evidence-capture-protocol.md
docs/external-frameworks/observed-evidence-capture-queue.v0.1.json
scripts/check_observed_evidence_capture_queue.py
scripts/check_goal5_external_frameworks_all.py
.github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

The observed-evidence queue must not advance beyond the exact evidence supported by artifacts. Same-environment replay is not independent replay, compatibility, standing, execution authority, or consequence authority.

## Cedar evidence boundary

Observed Cedar build evidence remains:

```text
Run: 29205883335
Artifact: cedar-selected-binary-build
Artifact ID: 8263766611
Artifact digest: sha256:cff4fbf627776db206c9f1f66281bf03a2c732709d29fa7682e56b99923b61dc
Pinned Cedar commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
Binary SHA-256: 96e6b0517f145875c12457f3350ad43fdc3be9f0e32c42ce813df0667fa036e1
Build state: BUILT_HASHED_UNEXECUTED
Registry promotion state: APPLIED_HASH_ONLY
execution_authorized: false
```

The promoted hash does not establish compatibility, certification, standing, admissibility, dispatch authority, execution authority, or external consequence authority.

## OPA same-environment completion

The successor run containing both capture-path probe repairs and the regression guard completed the required upstream stage:

```text
Workflow: Validate chain continuation
Run: 29209776393
Commit: 6f05d2d28fa7d1120fece631c980598cab6a3ff8
Branch: main
Job: validate-chain-continuation
Result: PASS
Job: capture-opa-evidence
Result: PASS
Run pinned OPA capture and same-environment replay: PASS
Validate generated OPA capture and replay artifacts: PASS
Artifact: opa-pinned-capture-replay
Artifact ID: 8264830147
Artifact digest: sha256:627dd10e68fb5a5f37759236f3a836e1f61ac02d14f26238de0b5bdf8f1b5446
```

This closes the outer and nested capture-path `version --format=json` regressions. It establishes only captured, validated, same-environment replay evidence.

## Fresh-runner failure and bounded repair

Run `29209776393` then reached the separately authorized fresh-runner stage and failed:

```text
Job: replay-opa-fresh-runner
Result: FAIL
Upstream OPA artifact download: PASS
Replay OPA on a fresh runner: FAIL
Artifact: opa-fresh-runner-replay
Artifact ID: 8264831760
Artifact digest: sha256:25e833afac7b4fdeba06638bf667c184f4348ef444da7b706f0a36cc037dd789
Confirmed compatibility defect: scripts/run_independent_opa_ci_replay.py retained `opa version --format=json`
```

Bounded repair:

```text
Commit: 186c751ac253c585315ca6ba03889f26765a8f02
File: scripts/run_independent_opa_ci_replay.py
Change: use supported `opa version`, require pinned version 1.0.0, preserve raw version evidence, and retain checksum, upstream-validation, comparison, and authority gates
```

The repair does not change the OPA version pin, binary URL, checksum verification, policy, inputs, query, comparison semantics, workflow permissions, execution authority, deployment state, release state, or any external repository.

## Pages blocker

Run `29209776393` also failed at:

```text
Job: build-pages
Step: Validate governance and activation artifacts
Result: FAIL
Build site: skipped
Deploy pages: skipped
Verify public pages: skipped
```

Treat this as a separate activation-artifact diagnosis. Do not weaken activation, deployment, public-verification, or release gates.

## Next task

```text
1. Verify the canonical successor run containing commit 186c751ac253c585315ca6ba03889f26765a8f02.
2. Require replay-opa-fresh-runner to pass before recording fresh-runner replay completion.
3. Preserve the fresh-runner artifact, exact hashes, environment, comparison results, and limitations.
4. Inspect the build-pages failure logs and identify the first failing governance or activation validator.
5. Apply only a bounded repository-local repair that preserves activation and deployment gates.
6. Require a passing Pages build before any deployment or public-verification claim.
7. Perform replay outside the same repository/provider before any stronger independence claim.
8. Review destination handoffs before any propagation to Site, Publisher, or StegGuardian.
```

## Remaining modules

```text
StegVerse-Labs/admissibility-wiki
  -> fresh-runner OPA successor verification
  -> fresh-runner replay receipt preservation
  -> build-pages activation-artifact diagnosis
  -> passing Pages build receipt
  -> public deployment verification receipt

Independent organization/provider
  -> independent OPA replay or independent implementation review

StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-002/stegguardian-wiki
  -> destination-handoff review before propagation
```

## Authority and release boundary

```text
binary build != runtime execution
binary hash != compatibility proof
promotion approval != execution authority
capture != standing
same-environment replay != independent replay
fresh runner != independent organization or provider
replay confirmation != execution authority
observation receipt != authority
Pages build != deployment authority
```

No deployment, release, tag, merge, external-repository mutation, runtime execution, credential attachment, dispatch, or public activation claim is authorized by this handoff. No release tag is authorized solely from schema, fixture, validation, promotion, capture, replay, repair, or automation installation.

## Archive readiness

This handoff preserves current Cedar evidence, canonical validation success, same-environment OPA capture and replay success, the first observed fresh-runner failure, bounded repair commit, Pages blocker, authority boundaries, remaining modules, and ordered continuation task. Earlier conversation context is not required.
