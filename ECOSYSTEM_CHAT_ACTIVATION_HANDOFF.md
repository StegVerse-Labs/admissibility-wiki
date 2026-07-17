# Ecosystem Chat Activation Handoff

## Scope

This record preserves the automatic downstream activation projection for `StegVerse-Labs/admissibility-wiki`.

## Source chain

```text
StegVerse-Labs/Site activation state
-> GCAT-BCAT-Engine/Publisher hourly importer
-> Publisher data/ecosystem-chat-activation-status.json
-> admissibility-wiki importer
-> static/status/ecosystem-chat-publisher-activation.json
-> canonical hourly workflow build and Pages publication
```

## Installed files

```text
scripts/import_publisher_ecosystem_chat_activation.py
scripts/generate_external_framework_page_status.py
static/status/ecosystem-chat-publisher-activation.json (generated)
.github/workflows/validate-chain-continuation.yml (existing canonical owner)
```

The existing canonical workflow already calls `generate_external_framework_page_status.py` during validation and Pages construction. That script now invokes the Publisher importer first. No new workflow, manual dispatch, artifact download, file movement, or user confirmation is required.

## Acceptance boundary

The importer requires:

- Publisher schema `stegverse.publisher.ecosystem_chat_activation_status.v1`;
- every Publisher authority flag to remain `false`;
- `manual_user_action_required=false`;
- `status=VERIFIED_ACTIVATION_IMPORTED` and `activation_complete=true` before recording a verified projection.

Missing Publisher state is recorded as `PENDING_PUBLISHER_ACTIVATION`. Invalid schema or authority fields fail closed as `REJECTED_PUBLISHER_ACTIVATION`.

## Authority boundary

The wiki projection is not publication authority, release authority, custody, execution authority, deployment authority, or an admissibility determination.

## Commits

```text
d0f9501f38737520992a3ccb288c30feceb2222e  add importer
61d8131d84a89949c4576d6d3da40a477f5a56ab  integrate importer into canonical generation path
```

GitHub exposed no combined status checks for `61d8131`. Missing status is not treated as validation success; the repository-owned hourly workflow remains responsible for producing evidence.

## Manual-task posture

```text
manual_user_action_required: false
continuation_owner: canonical hourly workflow
source_observation_owner: Publisher hourly importer
```

## Archive readiness

No future continuation requires the conversation that installed this consumer. Remaining activation is determined by upstream machine-generated evidence and the repository-owned canonical workflow.
