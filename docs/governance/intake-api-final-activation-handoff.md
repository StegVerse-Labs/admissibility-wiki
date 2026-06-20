---
title: Intake API Final Activation Handoff
---

# Intake API Final Activation Handoff

## Purpose

This handoff identifies the final remaining activation step for the Admissibility Wiki proposal intake API.

The repository-side build is complete enough for ecosystem-managed continuation.

## Installed Repo-Side Capabilities

```text
static_dual_mode_intake_ui: installed
repo_local_durable_backend: installed
local_api_server: installed
authorized_intake_workflow: installed
deploy_config: installed
endpoint_verification_tooling: installed
endpoint_verification_workflow: installed
pending_receipt_template: installed
status_artifacts: installed
```

## Installed Runtime Files

```text
scripts/lib/proposal-intake-core.mjs
scripts/proposal-intake-backend.mjs
scripts/proposal-intake-api-server.mjs
scripts/check-proposal-intake-backend-runtime.mjs
scripts/check-proposal-intake-api-server.mjs
scripts/verify-proposal-intake-public-endpoint.mjs
Dockerfile.intake-api
render.intake-api.yaml
github/workflows/intake-proposal.yml
github/workflows/verify-intake-api-endpoint.yml
```

Note: paths that normally begin with a leading dot are shown without the leading dot in this handoff.

## Current Public Endpoint Status

```text
public_browser_api_endpoint: deploy_pending
```

The public endpoint must not be marked active until a deployed runtime is verified and an observed deployment receipt is recorded.

## Final External Activation Step

Deploy an authorized runtime using:

```text
Dockerfile.intake-api
```

or:

```text
render.intake-api.yaml
```

Then run the manual verification workflow:

```text
github/workflows/verify-intake-api-endpoint.yml
```

Input required:

```text
endpoint_url: https://<deployed-runtime>/api/wiki/proposals/intake
fixture_path: fixtures/intake/submission.valid.example.json
```

## Evidence Required Before Active Status

The observed receipt must show:

```text
runtime_health_check: passed
valid_manifest_submission: passed
receipt_non_claims_present: passed
queue_result_present: passed
malformed_json_rejected: passed
```

## Boundary Rules

Even after endpoint verification:

- receipt issuance does not accept a proposal;
- queue placement does not create decision authority;
- automatic AI review remains not installed unless separately built;
- automatic decision publication remains not installed unless separately built;
- only a decision record can accept, deny, defer, escalate, refuse, or supersede a proposal.

## Next Safe Action

Do not add more intake scaffolding unless a verification result identifies a gap.

The next safe action is external activation:

```text
deploy runtime -> run endpoint verification -> commit observed receipt -> update public endpoint status
```
