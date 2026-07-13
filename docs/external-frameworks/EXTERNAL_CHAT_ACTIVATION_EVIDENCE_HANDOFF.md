# External Chat Activation Evidence Handoff

## Current state

```text
Goal: receive and validate exact deployment-correlated External Chat evidence from StegVerse-Labs/Site
Phase: bounded acquisition and synchronization installed; exact multi-run and run-attempt artifact selection hardened
Result: EXACT_SELECTION_INSTALLED_OBSERVED_SITE_ARTIFACT_PENDING
```

## Source artifact

The source repository is `StegVerse-Labs/Site`, workflow `Site Task Runner`, and expected artifact name is exact rather than prefix-only:

```text
external-chat-activation-evidence-<run_id>-<run_attempt>
```

The artifact must contain exactly one:

```text
external-chat-activation-evidence.json
```

The payload must bind the selected workflow run ID, run attempt, commit SHA, repository identity, post-deployment observations, and mutation-disabled posture.

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
receipts/external-chat-activation-artifact-selection-hardening-2026-07-13.json
scripts/check_goal5_external_frameworks_all.py
```

## Acquisition selection and identity binding

The acquisition client now examines completed successful `Site Task Runner` runs on `main` newest-first. It does not stop merely because the newest successful run lacks the expected artifact.

For each candidate run it constructs the exact expected artifact name:

```text
external-chat-activation-evidence-<selected run id>-<selected run attempt>
```

It accepts exactly one non-expired match and verifies:

```text
source repository = StegVerse-Labs/Site
source workflow = Site Task Runner
run conclusion = success
head branch = main
artifact name run_id = selected run_id
artifact name run_attempt = selected run_attempt
payload workflow_run_id = selected run_id
payload workflow_run_attempt = selected run_attempt
payload commit_sha = selected run head_sha
exactly one activation-evidence JSON file exists
```

The following stale behavior is prohibited:

```text
select newest successful run and stop when it lacks an artifact
accept any artifact sharing only the expected prefix
ignore run-attempt drift
choose among duplicate exact artifacts
```

Duplicate exact matches, run-attempt drift, commit drift, repository drift, or malformed content fail closed.

Authentication is preferred through:

```text
STEGVERSE_SITE_ARTIFACT_TOKEN
GITHUB_TOKEN
```

For the public Site repository, the client may attempt public discovery without a token. When artifact download requires authentication, the result is an explicit `SKIPPED` receipt—not a successful import and not false activation evidence.

## Synchronization states

```text
SKIPPED
ACQUIRED_EXACT_ARTIFACT
IMPORTED_EXACT_ARTIFACT
FAIL_CLOSED
```

A no-artifact result now records:

```text
reason: no_successful_run_has_exact_activation_evidence_artifact
successful_runs_inspected: <count>
```

The synchronization orchestrator:

```text
acquires exact artifact
-> stages source JSON
-> invokes the fail-closed importer
-> verifies projected evidence hash
-> verifies provenance run identity
-> verifies provenance commit identity
-> marks acquisition receipt IMPORTED_EXACT_ARTIFACT
```

Goal 5 invokes synchronization before structural validators. A skipped acquisition remains visible through `external_chat_activation_sync.state` and does not create projection or activation claims.

## Current source readiness

The current `StegVerse-Labs/Site` handoff records Site validation result, receipt, and manifest generation, but does not yet declare a successful External Chat activation-evidence artifact. Therefore the expected current synchronization posture remains:

```text
state: SKIPPED
reason: no_successful_run_has_exact_activation_evidence_artifact
projection_written: false
```

This is a bounded observation, not proof that no future or uninspected run contains the artifact.

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

The acquisition and synchronization receipts remain under `reports/` and bind source workflow, run, attempt, artifact, commit, evidence hash, observed result, and mutation-disabled posture.

## Authority boundary

```text
contract installation != observed deployment evidence
artifact discovery != artifact acquisition
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
1. Observe a successful Site Task Runner run that emits the exact run-and-attempt-bound activation artifact.
2. Allow Goal 5 synchronization to inspect successful runs newest-first and either import or explicitly skip.
3. Preserve acquisition receipt, source artifact, projection, provenance, and Goal 5 report together.
4. Require mutation_required_disabled = true before retaining OBSERVED_NON_MUTATING_PUBLIC_PATHS.
5. Confirm source run ID, run attempt, and commit SHA match Site metadata.
6. Do not convert imported observation into certification, compatibility standing, publication authority, or mutation authority.
7. Perform one separately authorized disposable staging mutation only after non-mutating public evidence is observed and preserved.
```

## Sharing posture

The Admissibility Wiki now has a bounded automated path that searches across successful Site runs, requires exact run-attempt artifact identity, imports only content-bound evidence, and fails closed on drift. No observed Site activation artifact has yet been imported, and no deployment, publication, mutation, certification, or standing claim follows from synchronization tooling alone.
