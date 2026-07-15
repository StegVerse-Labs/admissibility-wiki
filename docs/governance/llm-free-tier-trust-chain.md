# LLM Free Tier Trust Chain

## Purpose

This page documents the bounded free-tier trust contract that connects the public Site display, the LLM-adapter response contract, and the SDK metadata-ingestion contract.

The contract defines what a future governed free-tier interaction may expose while preserving these boundaries:

```text
quota availability is not admissibility
receipt export is not permanent retention
replay is not commit-time standing
reconstruction is not commit-time standing
upgrade does not change governance requirements
prepared configuration is not live use
```

## Current activation posture

```text
contract_status: PREPARED_NOT_DEPLOYED
site_checkpoint: SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED
live_transport_enabled: false
usage_api_base: null
bounded_live_use_observed: false
same_origin_authenticated_deployment_observed: false
master_records_custody_observed: false
reconstructability_pass_observed: false
```

The values below are configured contract limits and display metadata. They are not evidence that live usage is currently active.

## Cross-repository chain

```text
StegVerse-org/LLM-adapter
  -> defines free_tier_trust metadata and usage-session contract fields
  -> destination implementation installed; current-main validation and deployment evidence remain gates

StegVerse-Labs/Site
  -> displays the bounded free-tier trust envelope on ecosystem-chat.html
  -> validates the display through scripts/check_site_llm_free_tier_trust.py
  -> runs that checker through the canonical Site validation workflow
  -> remains PREPARED_NOT_DEPLOYED with live transport disabled

StegVerse-org/StegVerse-SDK
  -> validates free_tier_trust metadata shape
  -> validates quota, receipt, replay, reconstruction, and authority non-claims
  -> produces contract-validation evidence without granting authority or custody

master-records/orchestration
  -> future authenticated custody destination
  -> must provide custody and reconstructability evidence before RECORDED may be claimed
```

## Configured free-tier envelope

```text
governed inquiries per day: 5
trial governed inquiries total: 25
receipt exports per day: 1
replays per day: 1
reconstruction scope: recent-session limited
private connectors: upgrade path
premium models: upgrade path
static demo only: false as a contract design
live service currently active: false
```

The trust-window values are design hypotheses, not observed user-study results:

```text
3-10 meaningful inquiries: proposed curiosity-level evaluation window
20-50 meaningful inquiries: proposed reliance-level evaluation window
```

No trust conclusion should be presented as measured until the study method, event records, population, results, and reproducibility evidence are public.

## Required non-claims

```text
free_tier_response_is_authority == false
quota_allow_is_admissibility == false
quota_allow_is_execution_authority == false
limit_allow_is_execution_authority == false
receipt_export_is_permanent_retention == false
replay_grants_commit_time_standing == false
reconstruction_grants_commit_time_standing == false
upgrade_changes_admissibility_requirements == false
configured_limits_prove_live_service == false
site_display_proves_provider_call == false
retrieval_receipt_proves_master_records_custody == false
```

## Activation evidence required

The contract may advance from prepared to live only after all of the following are observed:

```text
destination current-main tests
same-origin authenticated deployment
sample response conformance
retrieval receipt validation
no browser secret surface
Site current-main validation
Master-Records custody
reconstructability PASS
```

## Verification ownership

Adapter, Site, and SDK commands remain repository-local evidence sources. This wiki does not direct the user to run them manually. Their canonical workflows own execution, artifact generation, and renewal.

Relevant repository-local checks include:

```text
LLM-adapter: free-tier metadata, quota, limits, capability manifest, usage-session contract
Site: scripts/check_site_llm_free_tier_trust.py and governed ecosystem mirror checks
StegVerse-SDK: free-tier metadata ingestion and tests
```

## Boundary

This page is documentation. It does not call live providers, issue receipts, persist records, export audit packets, replay sessions, reconstruct sessions, grant execution authority, or prove that the configured free tier is deployed.

## Downstream propagation

After current-main validation, authorized deployment, conformance, custody, and reconstruction evidence are verified, propagation status should be reviewed for:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-002/stegguardian-wiki
```

Queued propagation is not completed propagation, and this repository has no cross-repository mutation authority.