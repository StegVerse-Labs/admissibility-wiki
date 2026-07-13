# External Chat Activation Evidence Handoff

## Current state

```text
Goal: receive and validate exact deployment-correlated External Chat evidence from StegVerse-Labs/Site
Phase: bounded cross-repository acquisition and Goal 5 synchronization installed
Result: AUTOMATED_SYNC_INSTALLED_OBSERVED_SITE_ARTIFACT_PENDING
```

## Source artifact

The source repository is `StegVerse-Labs/Site`, workflow `Site Task Runner`, and expected artifact prefix is:

```text
external-chat-activation-evidence-<run_id>-<run_attempt>
```

The artifact must contain exactly one:

```text
external-chat-activation-evidence.json
```

The record correlates local Site validation, exact commit and workflow identity, Pages deployment URL, post-deployment page and gateway observations, and mutation-disabled posture.

## Installed contracts and synchronization surfaces

```text
docs/external-frameworks/schemas/external-chat-activation-evidence.schema.json
docs/external-frameworks/examples/external-chat-activation-evidence.example.json
scripts/check_external_chat_activation_evidence.py
scripts/import_external_chat_activation_evidence.py
scripts/check_external_chat_activation_importer.py
scripts/acquire_external_chat_activation_evidence.py
scripts/sync_external_chat_activation_evidence.py
scripts/check_external_chat_activation_sync.py
receipts/external-chat-activation-evidence-contract-2026-07-13.json
receipts/external-chat-activation-evidence-sync-2026-07-13.json
scripts/check_goal5_external_frameworks_all.py
```

## Acquisition selection and identity binding

The acquisition client selects only a completed successful `Site Task Runner` run on `main`, then locates a non-expired artifact whose name binds the exact run ID and run attempt.

It verifies:

```text
source repository = StegVerse-Labs/Site
source workflow = Site Task Runner
run conclusion = success
head branch = main
artifact name run_id = selected run_id
payload workflow_run_id = selected run_id
payload commit_sha = selected run head_sha
exactly one activation-evidence JSON file exists
```

Authentication is preferred through:

```text
STEGVERSE_SITE_ARTIFACT_TOKEN
GITHUB_TOKEN
```

For the public Site repository, the client may attempt public discovery without a token. When artifact download requires authentication, the outcome is an explicit `SKIPPED` receipt—not a successful import and not a workflow failure.

## Synchronization states

```text
SKIPPED
ACQUIRED_EXACT_ARTIFACT
IMPORTED_EXACT_ARTIFACT
FAIL_CLOSED
```

The synchronization orchestrator:

```text
acquires exact artifact
-> stages source JSON
-> invokes existing fail-closed importer
-> verifies projected evidence hash
-> verifies provenance run identity
-> verifies provenance commit identity
-> marks acquisition receipt IMPORTED_EXACT_ARTIFACT
```

Goal 5 invokes this synchronization before structural validators. A skipped acquisition remains visible in the Goal 5 report through `external_chat_activation_sync.state` and does not create false activation evidence.

## Accepted result classes

```text
OBSERVED_NON_MUTATING_PUBLIC_PATHS
LOCAL_VALIDATION_NOT_CONFIRMED
LIVE_EVIDENCE_NOT_AVAILABLE
LIVE_EVIDENCE_NOT_CONFIRMED
```

`OBSERVED_NON_MUTATING_PUBLIC_PATHS` is accepted only when local validation passed, the post-deployment receipt passed, and mutation was observed disabled.

## Projection behavior

A validated import atomically writes:

```text
static/status/external-chat-activation-evidence.json
static/status/external-chat-activation-evidence.provenance.json
```

The acquisition and synchronization receipts remain under `reports/` and bind the source workflow, run, artifact, commit, evidence hash, observed result, and mutation-disabled posture.

## Authority boundary

```text
contract installation != observed deployment evidence
artifact acquisition != deployment authority
artifact synchronization != repository mutation authority
activation evidence != publication authority
activation evidence != certification
activation evidence != standing
wiki projection != source authority
mutation remains separately authorized
```

## Next tasks

```text
1. Observe a successful Site Task Runner artifact containing OBSERVED_NON_MUTATING_PUBLIC_PATHS.
2. Allow Goal 5 synchronization to acquire or explicitly skip that artifact with a machine-readable reason.
3. Preserve the acquisition receipt, source artifact, projection, provenance, and Goal 5 report together.
4. Require mutation_required_disabled = true before retaining the observed projection.
5. Confirm the source run ID and commit SHA match the Site artifact metadata.
6. Do not convert the imported observation into certification, compatibility standing, publication authority, or mutation authority.
7. Perform one separately authorized disposable staging mutation only after non-mutating public evidence is observed and preserved.
```

## Sharing posture

The Admissibility Wiki now has a bounded automated path that discovers, identity-checks, imports, and validates the exact Site activation-evidence artifact through Goal 5. No observed Site artifact has yet been imported by this installation, and no deployment, publication, mutation, certification, or standing claim follows from synchronization tooling alone.
