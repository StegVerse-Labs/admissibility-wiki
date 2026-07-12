# Cedar Binary Build Automation Handoff

## Current transition

Cedar has advanced from canonical implementation selection to an automated build-and-hash stage.

```text
canonical source selection
-> pinned source checkout
-> locked release build
-> binary SHA-256 receipt
-> artifact upload
-> inspection required
```

The stage does not run `cedar authorize`, does not evaluate a policy, and does not request runtime execution.

## Selected implementation

```text
framework_id: cedar-policy
implementation: cedar-policy-cli
version: 4.11.0
canonical_repository: cedar-policy/cedar
pinned_commit: 0807ec154afd7ffa14a658c9955d25bfe12770ca
rust_toolchain: 1.89.0
build_command: cargo build --locked --release -p cedar-policy-cli
binary: target/release/cedar
```

## Installed automation

```text
scripts/build_selected_cedar_binary.py
scripts/check_cedar_selected_binary_build_harness.py
.github/workflows/validate-chain-continuation.yml
  -> build-selected-cedar-binary
iosnoperiod/github/workflows/validate-chain-continuation.yml
  -> byte-identical mirror
scripts/check_goal5_external_frameworks_all.py
  -> Cedar build-harness validator integrated
```

The existing canonical workflow was extended; no additional workflow was created.

## Generated artifact

A successful build job writes:

```text
reports/external-frameworks/cedar-build/cedar-binary-build-receipt.json
```

and uploads:

```text
cedar-selected-binary-build
```

The receipt records the pinned and resolved commit, Cargo.lock SHA-256, build command, build exit code, binary SHA-256, binary size, GitHub runner context, stdout/stderr, and explicit non-authority boundaries.

## Required output posture

```text
overall_status: BUILT_HASHED_UNEXECUTED
binary.executed_after_build: false
authority_boundary.binary_build_is_execution_authority: false
authority_boundary.binary_hash_is_compatibility_proof: false
authority_boundary.binary_was_used_for_authorization_decision: false
authority_boundary.runtime_execution_authorized: false
authority_boundary.external_consequence_allowed: false
```

A failed clone, checkout, lockfile check, build, or binary lookup produces `BUILD_FAILED` with explicit failures.

## Evidence boundary

```text
source selection != compiled binary
compiled binary != executed evaluator
binary hash != compatibility proof
build success != policy decision
build artifact != runtime authority
artifact upload != inspected evidence
```

## Current evidence state

```text
build automation installed: yes
workflow mirror synchronized: yes
aggregate structural validator installed: yes
completed build receipt inspected: no
compiled binary SHA-256 promoted into selection registry: no
Cedar authorization output captured: no
runtime execution authorized: no
```

No successful build is claimed until the workflow job and uploaded receipt are inspected.

## Next action

Inspect the first `cedar-selected-binary-build` artifact when its run becomes accessible. Verify the resolved commit, Cargo.lock hash, build exit code, binary SHA-256, binary size, runner context, and non-execution flags. Only after inspection may the compiled binary hash be attached to the Cedar selection evidence. Authority and consequence-boundary review remain separate and are still required before any authorization capture.
