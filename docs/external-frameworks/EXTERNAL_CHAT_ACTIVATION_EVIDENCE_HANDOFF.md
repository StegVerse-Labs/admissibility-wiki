# External Chat Activation Evidence Handoff

## Current state

```text
Goal: receive, validate, and prepare exact deployment-correlated External Chat evidence from StegVerse-Labs/Site for separately authorized canonical status promotion
Phase: exact acquisition, synchronization, observation candidate, promotion receipt, and dry-run application boundary installed
Result: STATUS_PROMOTION_BOUNDARY_INSTALLED_SOURCE_ARTIFACT_PENDING
```

## Source and candidate path

```text
StegVerse-Labs/Site Site Task Runner
-> external-chat-activation-evidence-<run_id>-<run_attempt>
-> exact artifact acquisition
-> fail-closed import
-> projection and provenance
-> reports/external-chat-activation-observation-candidate.json
-> separately authorized promotion receipt
-> canonical status application
```

The candidate must be `OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE` and bind source repository, commit SHA, workflow run ID, run attempt, evidence SHA-256, and `mutation_required_disabled = true`.

## Installed surfaces

```text
scripts/acquire_external_chat_activation_evidence.py
scripts/sync_external_chat_activation_evidence.py
scripts/import_external_chat_activation_evidence.py
scripts/generate_external_chat_activation_observation_candidate.py
scripts/check_external_chat_activation_observation_candidate.py
static/schemas/external-chat-activation-status-promotion-receipt.schema.json
tests/fixtures/external-chat-activation-status-promotion-receipt.blocked.json
scripts/check_external_chat_activation_status_promotion_receipt.py
static/status/external-chat-activation-observation.json
scripts/apply_external_chat_activation_observation_status.py
scripts/check_external_chat_activation_status_application.py
receipts/external-chat-activation-status-promotion-boundary-2026-07-13.json
scripts/check_goal5_external_frameworks_all.py
```

## Promotion receipt boundary

Only this decision can authorize the one canonical status mutation:

```text
ALLOW_CANONICAL_STATUS_PROMOTION_ONLY
```

It requires:

```text
candidate state = OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE
candidate SHA-256 recomputes
source repository = StegVerse-Labs/Site
source commit SHA matches candidate
source workflow run ID matches candidate
source workflow run attempt matches candidate
source evidence SHA-256 matches candidate
mutation_required_disabled = true
target path = static/status/external-chat-activation-observation.json
```

All other decisions require `canonical_status_mutation_allowed = false`.

## Application behavior

The application engine is dry-run by default:

```text
python scripts/apply_external_chat_activation_observation_status.py \
  --promotion-receipt <receipt-path>
```

A real status write additionally requires:

```text
--apply
```

Application states are:

```text
VALIDATED_DRY_RUN
APPLIED_OBSERVED_NON_MUTATING_PUBLIC_PATHS
ALREADY_OBSERVED_NON_MUTATING_PUBLIC_PATHS
BLOCKED
```

The engine is idempotent and fails closed on candidate hash drift, source evidence drift, run-attempt drift, target-path drift, or missing mutation-disabled posture.

## Canonical status boundary

The only mutable target is:

```text
static/status/external-chat-activation-observation.json
```

A successful application records `OBSERVED_NON_MUTATING_PUBLIC_PATHS` while preserving:

```text
deployment_authorized = false
repository_mutation_authorized = false
publication_authorized = false
certification_created = false
standing_created = false
```

Canonical observation status records an observed state. It does not authorize deployment, publication, repository mutation, certification, compatibility standing, or consequence.

## Current readiness

No successful Site activation artifact has yet been observed or imported in this workstream. Therefore:

```text
observed_site_artifact_imported = false
observed_candidate_promoted = false
canonical_status_mutated_by_installation = false
```

## Authority boundary

```text
artifact acquisition != deployment authority
artifact synchronization != repository mutation authority
observation candidate != canonical status mutation
promotion receipt != deployment authority
canonical observation status != publication authority
canonical observation status != certification
canonical observation status != standing
mutation remains separately authorized
```

## Next tasks

```text
1. Observe a successful Site Task Runner activation artifact.
2. Import and validate its exact run, attempt, commit, and evidence hashes.
3. Generate OBSERVED_NON_MUTATING_PUBLIC_PATHS_CANDIDATE.
4. Issue a separately authorized promotion receipt bound to that candidate.
5. Dry-run the application and inspect the result.
6. Apply only the canonical observation status in a separately governed commit.
7. Preserve candidate, promotion receipt, application receipt, canonical status, provenance, and Goal 5 report together.
8. Perform one separately authorized disposable staging mutation only after the observed non-mutating status is preserved.
```

## Sharing posture

The Admissibility Wiki now has the complete bounded path from exact Site evidence through a separately authorized, idempotent, canonical-status-only application boundary. No observed Site artifact has yet been promoted, and no deployment, publication, repository mutation, certification, or standing claim follows from installing this boundary.
