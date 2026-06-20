---
title: Proposal Governance Core-Lite Creation Task
---

# Proposal Governance Core-Lite Creation Task

## Task

Create the target repository:

```text
StegVerse-Labs/proposal-governance-core-lite
```

Then copy the seed from:

```text
repo-seeds/proposal-governance-core-lite/
```

## Done Criteria

```text
target_repository_exists: true
seed_files_copied: true
npm_run_validate_passes_in_target_repo: true
ingestion_cge_return_contract_documented: true
master_records_copy_contract_documented: true
public_display_consequence_contract_documented: true
```

## Current Status

```text
target_repository_exists: false
seed_status: installed_and_validatable
runtime_status: not_deployed
```

## Source of Truth

```text
docs/governance/proposal-governance-core-lite-seed.md
static/status/proposal-governance-core-lite-seed-status.json
repo-seeds/proposal-governance-core-lite/status/proposal-governance-core-lite-status.json
```

## Boundary

Do not claim the target repo is active until it exists independently and validates independently.

## Next Action

Create `StegVerse-Labs/proposal-governance-core-lite`, copy the seed, then run:

```text
npm run validate
```
