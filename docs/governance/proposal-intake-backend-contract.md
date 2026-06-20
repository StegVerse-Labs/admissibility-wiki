---
title: Proposal Intake Backend Contract
---

# Proposal Intake Backend Contract

## Purpose

This page defines the backend contract for the proposal intake interface.

A repo-local durable intake backend is installed as a Node script.

A public browser/API endpoint is not installed yet.

## Current Status

```text
repo_local_backend: installed
backend_script: scripts/proposal-intake-backend.mjs
durable_candidate_write: installed
durable_receipt_issuance: installed_repo_local
durable_queue_write: installed_repo_local
queue_index_write: installed_repo_local
browser_api_endpoint: not_installed
automatic_ai_review: not_installed
automatic_decision_publication: not_installed
```

## Repo-Local Command

```text
npm run intake:proposal -- fixtures/intake/submission.valid.example.json
```

The command writes durable artifacts under:

```text
static/governance/intake/candidates/
static/governance/intake/receipts/
static/governance/intake/queue/
static/governance/intake/queue/index.json
```

## Runtime Validation

The runtime validator executes the backend in a temporary directory and verifies candidate, receipt, queue, and index output without polluting the repository.

```text
npm run validate:proposal-intake-runtime
```

## Intended Endpoint Shape

```text
POST /api/wiki/proposals/intake
```

This endpoint shape is reserved for a future browser/API wrapper around the repo-local backend contract.

## Request Body

```json
{
  "manifest": {
    "schema": "admissibility_wiki_submission_manifest.v1"
  },
  "receipt_request": {
    "include_submission_timing": true,
    "include_hashes": true,
    "include_replay_expectation": true
  },
  "submission_context": {
    "origin": "browser | api | ecosystem_agent | maintainer_tool",
    "user_visible_mode": "guided_builder | direct_paste",
    "submitted_at_client": "2026-06-19T00:00:00Z"
  }
}
```

## Response Body

```json
{
  "receipt": {
    "schema": "admissibility_wiki_submission_receipt.v1",
    "receipt_id": "receipt.generated.example",
    "proposal_id": "proposal.generated.example",
    "received_at": "2026-06-19T00:00:00Z",
    "receipt_issued_at": "2026-06-19T00:00:05Z",
    "submission_lane": "lane_1_manifest_receipt",
    "preference_posture": "preferred_triage",
    "validation_posture": "valid_manifest",
    "tasks": []
  },
  "queue_result": {
    "queued": true,
    "queue_id": "queue.generated.example",
    "review_route": "admissibility_wiki_ai_entity"
  },
  "non_claims": [
    "Receipt does not accept the proposal.",
    "Receipt does not prove the submitted claim.",
    "Receipt does not create equivalent-term standing.",
    "Queue placement does not create decision authority."
  ]
}
```

## Required Backend Tasks

The backend records timing for:

```text
receive_request
parse_manifest
validate_manifest_schema
classify_submission_lane
assign_preference_posture
compute_submission_hashes
write_candidate_record
write_queue_record
issue_submission_receipt
```

## Required Hashes

A backend implementation should generate hashes for:

- raw submitted body;
- normalized manifest;
- issued receipt;
- queue record;
- related evidence attachments when present.

## Queue Boundary

Queue placement does not accept a proposal.

Queue placement only means the proposal is available for review.

## Review Boundary

AI review may recommend classification, duplicate status, relationship type, transition-origin posture, and evidence posture.

AI review must not silently publish glossary changes or decision records.

## Decision Boundary

Only a decision record can accept, deny, defer, escalate, refuse, or supersede a proposal.

Receipt issuance and queue placement are not decision records.

## Browser/API Active Criteria

The public browser/API backend can be called active only when:

- a deployed endpoint accepts a manifest/receipt preview object;
- schema validation runs server-side;
- malformed submissions produce bounded error receipts or rejection records;
- valid submissions receive durable receipt IDs;
- queue records are written durably;
- timing tasks are recorded;
- hashes are recorded;
- decision records remain separate from receipts;
- test fixtures exist for guided-builder and direct-paste submissions.

## Related Pages

- [Proposal Intake Interface](./proposal-intake-interface.md)
- [Manifest Receipt Submission](./manifest-receipt-submission.md)
- [Proposal Lifecycle](./proposal-lifecycle.md)
- [Decision Record](./decision-record.md)
