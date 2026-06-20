# Proposal Governance Core-Lite

Repository target: `StegVerse-Labs/proposal-governance-core-lite`

## Purpose

This repo is the second post-sandbox core-lite/ingestion engine for Admissibility Wiki proposal governance.

It receives post-sandbox proposal bundles after they return through ingestion/CGE, preserves every ingestion pass to master-records, selects the admissible consequence path through a decision record, and routes eligible consequences to the public wiki display path.

## Core Route

```text
proposal page or shared SDK entry point
↓
ingestion/CGE -> master-records
↓
sandbox candidate-path testing
↓
ingestion/CGE -> master-records
↓
proposal-governance-core-lite
├─ master-records
└─ public display consequence path
```

## Governance Classes

```text
E = Editorial
G = Governance
F = Formalism
```

## Hard Boundaries

```text
Receipt does not accept a proposal.
Queue placement does not create decision authority.
Sandbox output does not create public display standing.
LLM recommendation does not create decision authority.
Only a decision record can select ALLOW, ALLOW_AS_OVERLAP, DENY, DEFER, ESCALATE, REFUSE, or SUPERSEDE.
Every ingestion/CGE pass emits to master-records.
```

## Installed Seed Structure

```text
schemas/proposal-governance-decision.v1.json
schemas/proposal-governance-routing.v1.json
fixtures/post-sandbox-bundle.example.json
fixtures/decision-record.allow-overlap.example.json
scripts/validate-core-lite.mjs
status/proposal-governance-core-lite-status.json
package.json
```

## Not Yet Active

```text
repo_created: pending
runtime_deployed: pending
ingestion_cge_connection: pending
master_records_connection: pending
public_display_connection: pending
```

This seed is ready to copy into `StegVerse-Labs/proposal-governance-core-lite` after the repository is created.
