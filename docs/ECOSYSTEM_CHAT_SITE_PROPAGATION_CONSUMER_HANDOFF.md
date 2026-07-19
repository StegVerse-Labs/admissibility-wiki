# Ecosystem Chat Site Propagation Consumer Handoff

## Installed result

```text
Repository: StegVerse-Labs/admissibility-wiki
Result: AUTONOMOUS_FAIL_CLOSED_SITE_PROPAGATION_CONSUMER_INSTALLED
Manual user action required: false
Canonical workflow: .github/workflows/validate-chain-continuation.yml
Standalone workflow added: false
```

## Installed files

```text
scripts/check_ecosystem_chat_activation_projection.py
static/status/ecosystem-chat-activation-status.json
```

The consumer runs through `scripts/check_admissibility_automation_handoff.py` and `npm run validate` inside the existing hourly canonical workflow. No dispatch, browser action, copying, or user intervention is required.

## Acceptance gates

`VERIFIED_INGESTION_READY` requires valid Site state and packet hashes, matching state binding, a declared admissibility-wiki destination, Site `ACTIVATION_COMPLETE`, packet `READY_FOR_DOWNSTREAM_INGESTION`, destination `ingestion_ready=true`, no manual action, and all authority flags false.

Otherwise the public projection remains `ACTIVATION_EVIDENCE_PENDING` and records exact blockers.

## Current source state

```text
Site state: ACTIVATION_PENDING_EVIDENCE
Site propagation: PENDING_ACTIVATION_EVIDENCE
Destination declared: true
Destination ingestion ready: false
Required action: wait_for_verified_activation_state
Blockers: site_activation_not_complete; destination_ingestion_not_ready
```

## Boundary

The projection is not activation, release, publication, custody, admissibility, or execution authority.

## Continuation

1. The canonical hourly workflow refreshes the projection from Site.
2. Source failures retain and validate the last fail-closed projection.
3. Pending evidence creates no user task.
4. A valid ready packet advances the projection automatically.
5. Public deployment publishes the refreshed status through the existing Pages build.

## Remaining blocker

```text
Upstream: StegVerse-org/LLM-adapter, then StegVerse-Labs/Site
Blocker: live_activation_observation_not_yet_recorded
Manual user action required: false
```

No tag or release is authorized by this consumer.
