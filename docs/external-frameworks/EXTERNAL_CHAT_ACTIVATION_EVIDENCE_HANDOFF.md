# External Chat Activation Evidence Handoff

## Current state

```text
Goal: receive, validate, and prepare exact deployment-correlated External Chat evidence from StegVerse-Labs/Site for separately authorized status promotion
Phase: exact acquisition, synchronization, and non-mutating observation-candidate generation installed
Result: OBSERVATION_CANDIDATE_LAYER_INSTALLED_SOURCE_ARTIFACT_PENDING
```

## Source artifact

The source repository is `StegVerse-Labs/Site`, workflow `Site Task Runner`, and expected artifact name is exact:

```text
external-chat-activation-evidence-<run_id>-<run_attempt>
```

The artifact must contain exactly one:

```text
external-chat-activation-evidence.json
```

The payload must bind the selected workflow run ID, run attempt, commit SHA, repository identity, post-deployment observations, and mutation-disabled posture.

## Installed surfaces

```text
docs/external-frameworks/schemas/external-chat-activation-evidence.schema.json
docs/external-frameworks/examples/external-chat-activation-evidence.example.json
scripts/check_external_chat_activation_evidence.py
scripts/import_external_chat_activation_evidence.py
scripts/check_external_chat_activation_importer.py
scripts/acquire_external_chat_activation_evidence.py
scripts/sync_external_chat_activation_evidence.py
scripts/check_external_chat_activation_sync.py
scripts/generate_external_chat_activation_observation_candidate.py
scripts/check_external_chat_activation_observation_candidate.py
receipts/external-chat-activation-evidence-contract-2026-07-13.json
receipts/external-chat-activation-evidence-sync-2026-07-13.json
receipts/external-chat-activation-artifact-selection-hardening-2026-07-13.json
receipts/external-chat-activation-observation-candidate-2026-07-13.json
scripts/check_goal5_external_frameworks_all.py
```

## Acquisition identity binding

The acquisition client examines completed successful `Site Task Runner` runs on `main` newest-first. For each candidate run it constructs:

```text
external-chat-activation-evidence-<selected run id>-<selected run attempt>
```

It accepts exactly one non-expired artifact and verifies:

```text
source repository = StegVerse-Labs/Site
source workflow = Site Task Runner
run conclusion = success
head branch = main
artifact run_id = selected run_id
artifact run_attempt = selected run_attempt
payload workflow_run_id = selected run_id
payload workflow_run_attempt = selected run_attempt
payload commit_sha = selected run head_sha
exactly one activation-evidence JSON file exists
```

Duplicate exact matches, run-attempt drift, commit drift, repository drift, malformed content, or hash drift fail closed.

Authentication is preferred through:

```text
STEGVERSE_SITE_ARTIFACT_TOKEN
GITHUB_TOKEN
```

When artifact access is unavailable, synchronization records `SKIPPED`; it does not fabricate an import or activation observation.

## Synchronization states

```text
SKIPPED
ACQUIRED_EXACT_ARTIFACT
IMPORTED_EXACT_ARTIFACT
FAIL_CLOSED
```

The orchestrator:

```text
acquires exact artifact
-> stages source JSON
-> invokes fail-closed importer
-> verifies projected evidence hash
-> verifies provenance run identity
-> verifies provenance commit identity
-> marks acquisition receipt IMPORTED_EXACT_ARTIFACT
```

A validated import writes:

```text
static/status/external-chat-activation-evidence.json
static/status/external-chat-activation-evidence.provenance.json
```

Goal 5 runs synchronization before structural validation and preserves the synchronization state in its machine-readable report.

## Observation candidate layer

The new generator consumes only the validated projection and provenance:

```text
python scripts/generate_external_chat_activation_observation_candidate.py
```

It emits:

```text
reports/external-chat-activation-observation-candidate.json
```

Allowed candidate states are:

```text
PENDING_SOURCE_EVIDENCE
PENDING_OBSERVED_NON_MUTATING_RESULT
OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE
FAIL_CLOSED
```

`OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE` requires:

```text
source repository = StegVerse-Labs/Site
source result = OBSERVED_NON_MUTATING_PUBLIC_PATHS
local validation passed
local authority effect = NONE
post-deployment live verification passed
mutation_required_disabled = true
projection evidence SHA-256 recomputes
provenance evidence hash matches projection
provenance run ID matches projection
provenance commit SHA matches projection
```

The candidate is content-bound by `candidate_sha256` and records:

```text
canonical_status_mutated = false
deployment_authorized = false
repository_mutation_authorized = false
publication_authorized = false
certification_created = false
standing_created = false
```

A valid observed candidate identifies only the next possible transition:

```text
separately_authorized_canonical_status_promotion
```

It does not perform that promotion.

## Current source readiness

No successful Site activation artifact has yet been observed in this workstream. The expected current candidate posture is therefore:

```text
state: PENDING_SOURCE_EVIDENCE
canonical_status_mutated: false
```

This does not prove that no future or uninspected run contains the artifact.

## Authority boundary

```text
contract installation != observed deployment evidence
artifact discovery != artifact acquisition
artifact acquisition != deployment authority
artifact synchronization != repository mutation authority
wiki projection != source authority
observation candidate != canonical status mutation
observation candidate != public activation authority
activation evidence != publication authority
activation evidence != certification
activation evidence != standing
mutation remains separately authorized
```

## Next tasks

```text
1. Observe a successful Site Task Runner run emitting the exact run-and-attempt-bound activation artifact.
2. Allow Goal 5 synchronization to import or explicitly skip with a machine-readable reason.
3. Preserve acquisition receipt, source artifact, projection, provenance, observation candidate, and Goal 5 report together.
4. Require OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE before any status-promotion request.
5. Add a separately authorized canonical status-promotion receipt and application boundary.
6. Keep canonical promotion unable to authorize deployment, publication, repository mutation, certification, or standing.
7. Perform one separately authorized disposable staging mutation only after non-mutating public evidence is observed and preserved.
```

## Sharing posture

The Admissibility Wiki now has a bounded automated path from exact Site artifact discovery through import, provenance validation, and deterministic observation-candidate generation. No observed Site activation artifact has yet been imported, no canonical status has been advanced, and no deployment, publication, mutation, certification, or standing claim follows from the installed candidate layer.
