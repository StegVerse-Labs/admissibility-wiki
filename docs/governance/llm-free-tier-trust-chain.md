# LLM Free Tier Trust Chain

## Purpose

This page documents the bounded free-tier trust chain that connects the public Site display, the LLM adapter response contract, and the SDK metadata ingestion contract.

The purpose is to prove that the free tier is not merely a static demo while also preserving the core StegVerse boundary:

```text
quota availability is not admissibility
receipt export is not permanent retention
replay is not commit-time standing
reconstruction is not commit-time standing
upgrade does not change governance requirements
```

## Cross-repository chain

```text
StegVerse-org/LLM-adapter
  -> emits free_tier_trust metadata
  -> exposes adapter.capabilities.json free-tier fields

StegVerse-Labs/Site
  -> displays bounded free-tier trust envelope on ecosystem-chat.html
  -> guards the display with scripts/check_site_llm_free_tier_trust.py
  -> includes the checker in site-public-mirror-status-guard.yml

StegVerse-org/StegVerse-SDK
  -> validates free_tier_trust metadata shape
  -> validates quota / receipt / replay / reconstruction non-claims
  -> exposes validate_free_tier_metadata
  -> verifies ingestion in sdk-demo-test.yml
```

## Public free-tier envelope

The current public envelope is:

```text
governed inquiries per day: 5
trial governed inquiries total: 25
receipt exports per day: 1
replays per day: 1
reconstruction scope: recent-session limited
private connectors: upgrade path
premium models: upgrade path
static demo only: false
bounded live use: true
```

The expected trust window is:

```text
3-10 meaningful inquiries: curiosity-level trust
20-50 meaningful inquiries: reliance-level evaluation
```

## Required non-claims

The chain is valid only if these remain false:

```text
free_tier_response_is_authority == false
quota_allow_is_admissibility == false
quota_allow_is_execution_authority == false
limit_allow_is_execution_authority == false
receipt_export_is_permanent_retention == false
replay_grants_commit_time_standing == false
reconstruction_grants_commit_time_standing == false
upgrade_changes_admissibility_requirements == false
```

## Verification commands

Adapter:

```bash
python scripts/verify_goal4.py
python scripts/verify_free_tier_quota.py
python scripts/verify_free_tier_limits.py
python scripts/verify_ai_entry_free_tier_metadata.py
python scripts/verify_free_tier_capability_manifest.py
```

Site:

```bash
python scripts/check_site_llm_free_tier_trust.py
python scripts/check_site_governed_ecosystem_mirror.py
```

SDK:

```bash
python scripts/verify_free_tier_metadata_ingestion.py
pytest tests/test_free_tier_metadata.py -v
```

## Boundary

This page is documentation. It does not call live providers, issue receipts, persist records, export audit packets, replay sessions, reconstruct sessions, or grant execution authority.

## Downstream propagation

After Site and SDK validation are green, downstream summaries should be propagated to:

```text
GCAT-BCAT-Engine/Publisher
stegguardian-wiki
```
