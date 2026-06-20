---
title: Proposal Governance Core-Lite Seed
---

# Proposal Governance Core-Lite Seed

## Purpose

This page documents the drop-in seed for the target repository:

```text
StegVerse-Labs/proposal-governance-core-lite
```

The target repository does not exist yet.

The seed is currently stored in this repository at:

```text
repo-seeds/proposal-governance-core-lite/
```

## Why This Exists

The Admissibility Wiki proposal lifecycle now requires a second StegVerse-Labs core-lite/ingestion engine after sandbox return.

That second core-lite selects the admissible consequence path from the post-sandbox proposal bundle and sends:

```text
copy -> master-records
consequence -> public display path
```

Every ingestion/CGE pass still emits to master-records.

## Seed Contents

```text
README.md
package.json
schemas/proposal-governance-routing.v1.json
schemas/proposal-governance-decision.v1.json
fixtures/post-sandbox-bundle.example.json
fixtures/decision-record.allow-overlap.example.json
scripts/validate-core-lite.mjs
status/proposal-governance-core-lite-status.json
```

## Validation

From this repository, validate the seed with:

```text
node scripts/check-proposal-governance-core-lite-seed.mjs
```

After copying the seed into the new target repository, validate inside the target repo with:

```text
npm run validate
```

## Target Repo Creation Path

```text
1. Create StegVerse-Labs/proposal-governance-core-lite.
2. Copy repo-seeds/proposal-governance-core-lite/* into the new repo.
3. Run npm run validate.
4. Connect post-sandbox ingestion/CGE return path.
5. Connect master-records copy output.
6. Connect public-display consequence output.
```

## Boundaries

```text
seed_only: true
repo_created: false
runtime_deployed: false
ingestion_cge_connection: pending
master_records_connection: pending
public_display_connection: pending
```

Do not claim the target repo is active until the new repository exists and validates independently.

## Related Pages

- [Proposal Governance Classes](./proposal-governance-classes.md)
- [Proposal Intake API Deployment](./proposal-intake-api-deployment.md)
- [Intake API Final Activation Handoff](./intake-api-final-activation-handoff.md)
