---
title: Proposal Intake API Deployment
---

# Proposal Intake API Deployment

## Purpose

This page defines how the proposal intake API should be deployed when the wiki is ready to accept browser-originated submissions.

The local API server is installed.

The public deployed endpoint remains pending until an authorized runtime is selected, configured, and verified.

## Current Status

```text
local_api_server: installed
local_api_route: POST /api/wiki/proposals/intake
static_intake_page_can_submit_to_configured_endpoint: installed
deploy_config: installed
endpoint_verification_tooling: installed
public_browser_api_endpoint: deploy_pending
automatic_ai_review: not_installed
automatic_decision_publication: not_installed
```

## Local Run Command

```text
npm run intake:api
```

Default local route:

```text
http://127.0.0.1:8787/api/wiki/proposals/intake
```

Health route:

```text
http://127.0.0.1:8787/health
```

## Deployment Configuration

The repository includes a container deployment file and a Render-style service blueprint.

```text
Dockerfile.intake-api
render.intake-api.yaml
scripts/check-intake-api-deploy-config.mjs
```

Run the deployment-config validator directly with:

```text
node scripts/check-intake-api-deploy-config.mjs
```

## Endpoint Verification

The repository includes a verifier and a manual workflow for a deployed endpoint.

```text
scripts/verify-proposal-intake-public-endpoint.mjs
github/workflows/verify-intake-api-endpoint.yml
static/status/proposal-intake-endpoint-verification-status.json
scripts/check-proposal-intake-endpoint-verification-status.mjs
```

Note: paths that normally begin with a leading dot are shown without the leading dot in this page.

Run the verifier manually with:

```text
node scripts/verify-proposal-intake-public-endpoint.mjs https://example.org/api/wiki/proposals/intake
```

The verifier writes an observed deployment receipt only after testing:

```text
runtime_health_check
valid_manifest_submission
receipt_non_claims_present
queue_result_present
malformed_json_rejected
```

## Runtime Requirements

A deployed runtime must provide:

- Node 20 or compatible runtime;
- writable durable storage for candidate, receipt, queue, and index artifacts;
- controlled write access to the repo or a governed storage mirror;
- HTTPS endpoint;
- CORS policy appropriate to the GitHub.io wiki origin;
- request size limits;
- malformed-submission rejection path;
- logs sufficient to reconstruct intake attempts;
- no automatic decision publication.

## Required Environment Variables

```text
PORT=8787
HOST=0.0.0.0
INTAKE_OUTPUT_ROOT=static/governance/intake
MAX_BODY_BYTES=256000
```

## Public Endpoint Rule

The static intake page may submit only to an endpoint explicitly entered by the user or configured by a future deployment layer.

The GitHub.io static site itself does not provide server execution.

## Durable Artifact Rule

The deployed endpoint must produce the same artifact classes as the repo-local backend:

```text
candidate submission
submission receipt
queue record
queue index
```

## Boundary Rule

The endpoint may issue durable receipts and queue records.

The endpoint must not accept, deny, defer, escalate, refuse, supersede, or publish glossary changes by itself.

Only a decision record can do that.

## Verification Steps

Before marking the public browser/API endpoint active:

1. Validate deployment configuration.
2. Deploy the API runtime.
3. Run a health check.
4. Submit a valid manifest fixture.
5. Confirm candidate, receipt, queue record, and queue index are written durably.
6. Submit malformed JSON and confirm a bounded rejection response.
7. Confirm receipt non-claims remain present.
8. Confirm queue non-claims remain present.
9. Confirm no decision record is created by intake.
10. Record a deployment receipt.
11. Update status only after evidence exists.

## Not Yet Included

```text
automatic_ai_review
automatic_decision_publication
automatic_ontology_mutation
public_endpoint_active_status
```

## Related Pages

- [Proposal Intake Backend Contract](./proposal-intake-backend-contract.md)
- [Proposal Intake Interface](./proposal-intake-interface.md)
- [Manifest Receipt Submission](./manifest-receipt-submission.md)
- [Decision Record](./decision-record.md)
