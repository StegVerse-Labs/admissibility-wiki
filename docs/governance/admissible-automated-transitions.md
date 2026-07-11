# Admissible Automated Transitions

## Purpose

This page is the public observability surface for automated transitions that currently affect the StegVerse development ecosystem.

It catalogs automation that can inspect, verify, repair, continue, notify, or update repository state under an explicit handoff and declared authority boundary.

The page is an observatory. It does not itself authorize, execute, deploy, merge, release, or mutate any system.

## Governing rule

```text
event wakes the automation
-> repository or scope is resolved
-> current *_MIRROR_HANDOFF.md is read
-> permitted task is selected
-> prerequisites and authority are checked
-> bounded action is attempted
-> result is verified
-> receipt and handoff are updated
-> next declared task may begin
```

The triggering email, workflow result, schedule, or manual request does not determine the task. The current handoff remains the task source of truth.

## Current transition catalog

### GitHub Handoff Watch

| Field | Current declaration |
|---|---|
| Transition ID | `automation.github-handoff-watch.hourly.v1` |
| Scope | Repository and explicitly declared cross-repository follow-up |
| Trigger | Hourly Gmail condition watch for GitHub notifications |
| Event classes | Failure; completion or progress |
| Task authority | Current repository `*_MIRROR_HANDOFF.md` |
| Permitted effects | Inspect, classify, apply bounded authorized repair, verify, update handoff, begin next declared bounded task |
| Prohibited by default | Archive, delete, deploy, release, tag, merge, send email, or modify external repositories without explicit handoff authority |
| Failure posture | Stop and notify on ambiguous authority, destructive action, unavailable credentials, unverifiable tests, or missing next task |
| Status | `ACTIVE_BOOTSTRAP_ORCHESTRATION` |

This automation temporarily supplies continuity while repository, cross-repository, organization, cross-organization, and ecosystem orchestrators are not yet self-operational.

## Admissibility conditions

An automated transition is catalogued as admissible for operation only when all applicable conditions are satisfied:

1. The trigger can be associated with an identified repository or declared scope.
2. A current handoff exists and identifies the active task or permitted repair class.
3. The action remains within the handoff's declared authority and boundary.
4. Required prerequisites, files, checks, and evidence are available.
5. The action is bounded and recoverable, or the handoff explicitly declares otherwise.
6. Completion can be verified through files, tests, checks, receipts, or other declared evidence.
7. The result and next task can be written back without fabricating standing.
8. Duplicate, stale, unrelated, and partial-progress events are rejected.

## Transition states

```text
DECLARED
READY
RUNNING
VERIFICATION_REQUIRED
COMPLETED
BLOCKED
DENIED
FAIL_CLOSED
SUPERSEDED
RETIRED
```

`COMPLETED` means the declared completion conditions were verified. It does not imply release, deployment, certification, or ecosystem-wide standing.

## Manifest

The machine-readable catalog is published at:

```text
static/governance/admissible-automated-transitions.v0.1.json
```

The manifest records:

- transition identity and version;
- trigger and schedule class;
- scope;
- handoff authority source;
- permitted and prohibited actions;
- verification requirements;
- failure and escalation posture;
- current lifecycle state;
- receipt references.

## Receipt

The installation and declaration receipt is stored at:

```text
receipts/admissible-automated-transitions-observatory-receipt.json
```

This receipt confirms that the catalog page, manifest, and navigation entry were installed. It does not certify the truth of every future event or grant authority to the automation.

## Update protocol

The catalog should be updated whenever:

- an automation is created, materially changed, paused, retired, or superseded;
- its schedule, trigger class, authority source, or permitted effects change;
- a new repair or continuation class is introduced;
- a repository migrates from bootstrap email/handoff orchestration to native orchestration;
- a receipt schema or canonical event identity changes.

Each material update should produce or reference a new receipt and preserve prior versions for reconstruction.

## Migration posture

The current bootstrap path is temporary:

```text
email and scheduled condition watch
-> handoff-aware bootstrap executor
-> repository-native orchestrator
-> organization orchestrator
-> cross-organization orchestration
-> ecosystem orchestration
```

As native orchestration becomes operational, entries should move from `ACTIVE_BOOTSTRAP_ORCHESTRATION` to `OBSERVE_ONLY`, then `RETIRED`, only after replacement behavior and recovery paths are verified.

## Boundary

This page documents declared automated transitions and their admissibility conditions. Publication here does not create execution authority, prove that every automation run succeeded, authorize cross-repository mutation, or replace run-specific receipts and evidence.
