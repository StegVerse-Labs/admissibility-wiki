# Cedar Binary Promotion Automation Handoff

## Scope

This handoff covers the bounded transition from a generated Cedar binary build receipt to a non-mutating registry-promotion candidate. It supplements `EXTERNAL_FRAMEWORKS_MIRROR_HANDOFF.md` and does not supersede concurrent observed-dispatch, CI-repair, deployment-verification, or external-evidence work.

## Installed chain

```text
canonical Cedar source selection
-> pinned locked build
-> BUILT_HASHED_UNEXECUTED receipt
-> fail-closed receipt inspection
-> binary registry-promotion candidate
-> separate governed registry mutation review
```

Installed files:

```text
scripts/build_selected_cedar_binary.py
scripts/inspect_cedar_binary_build_receipt.py
scripts/check_cedar_selected_binary_build_harness.py
scripts/check_cedar_binary_promotion_automation.py
scripts/check_goal5_external_frameworks_all.py
.github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

## Automated inspection

After a successful locked build, `build_selected_cedar_binary.py` invokes `inspect_cedar_binary_build_receipt.py`. The inspector requires:

```text
artifact_type: external_framework_selected_binary_build_receipt
framework_id: cedar-policy
implementation_identifier: cedar-policy-cli
selection_version: 4.11.0
pinned_commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
resolved_commit: same pinned commit
build_command: cargo build --locked --release -p cedar-policy-cli
build_exit_code: 0
overall_status: BUILT_HASHED_UNEXECUTED
failures: []
valid Cargo.lock SHA-256
valid binary SHA-256
positive binary size
binary.executed_after_build: false
all non-authority boundaries: false
```

A valid receipt produces:

```text
reports/external-frameworks/cedar-build/cedar-binary-registry-promotion-candidate.json
candidate_state: READY_FOR_REGISTRY_PROMOTION_REVIEW
receipt_validated: true
registry_mutation_performed: false
runtime_execution_requested: false
runtime_execution_authorized: false
authorization_decision_observed: false
external_consequence_allowed: false
```

An invalid or incomplete receipt produces:

```text
candidate_state: BLOCKED_BUILD_RECEIPT_INVALID
receipt_validated: false
registry_mutation_performed: false
runtime_execution_requested: false
runtime_execution_authorized: false
```

## Promotion boundary

The candidate carries the inspected binary SHA-256, binary size, Cargo.lock SHA-256, resolved commit, version, and source receipt SHA-256. It does not mutate `implementation-selection-gates.v0.1.json`.

A separate governed commit must inspect the workflow artifact and explicitly apply the binary hash to the Cedar selection registry. That later commit must preserve:

```text
execution_authorized: false
runtime execution not requested
no policy decision observed
no external consequence permitted
```

Binary-hash promotion closes one reproducibility field. It does not establish compatibility, certification, standing, authority, delegation, freshness, scope, or consequence admissibility.

## Workflow artifact

The existing workflow artifact remains:

```text
cedar-selected-binary-build
path: reports/external-frameworks/cedar-build
```

It now contains both the build receipt and, when inspection succeeds, the registry-promotion candidate. No additional workflow was introduced.

## Current evidence posture

```text
source selection: installed and hash-bound
pinned build automation: installed
build receipt inspection automation: installed
registry-promotion candidate automation: installed
successful workflow build inspected: no
binary hash promoted into registry: no
Cedar authorization decision executed: no
runtime execution authorized: no
```

No successful build, binary hash, or promotion is claimed until the actual workflow artifact is available and inspected.

## Next action

Inspect the first `cedar-selected-binary-build` artifact. If the build receipt and promotion candidate validate, record the run, job, artifact, source receipt, Cargo.lock, and binary hashes, then apply the binary hash to the Cedar selection registry in a separate governed commit while keeping execution authorization false.
