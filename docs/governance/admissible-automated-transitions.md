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
-> transition-table elements are derived
-> permitted task is selected
-> prerequisites, evidence, policy, delegation, and authority are checked
-> bounded action is attempted
-> commit-time validity is checked
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

## Derived transition-table elements

The automation is not governed merely because it follows a schedule or reads a handoff. Before any consequence-bearing action, it must derive a transition candidate from the current event, repository state, handoff, policy boundaries, and available evidence.

| Transition-table element | Derivation for GitHub Handoff Watch |
|---|---|
| Transition ID | Stable automation identity plus run/event identity; catalog identity is `automation.github-handoff-watch.hourly.v1` |
| Input state | Unread GitHub notification, related repository state, current handoff, current checks, files, and receipts |
| Proposed action | Classify failure/completion, apply a bounded repair, verify completion, update handoff, or begin the next declared task |
| Actor | The scheduled bootstrap handoff executor acting as a non-sovereign tool participant |
| Target | The repository named by the event and resolved against the current handoff |
| Scope | Repository by default; cross-repository only when the handoff explicitly declares the target and action |
| Policy reference | Automation prompt boundaries, repository handoff constraints, repository workflow/release policy, and applicable ecosystem governance rules |
| Delegation reference | Explicit task or repair permission contained in the current handoff; absence or ambiguity fails closed |
| Evidence references | Email event, commit or workflow context, repository files, tests/checks, manifests, receipts, and prior handoff state |
| Authority class | Inspect and bounded repository mutation only when explicitly declared; no inferred release, deployment, merge, or ecosystem authority |
| Review posture | Automated review for bounded declared work; human review required at ambiguous, destructive, irreversible, credentialed, or cross-boundary transitions |
| Execution context | Hourly condition-watch run, resolved repository, branch/commit/PR context, available credentials, and current tool capabilities |
| Validity window | Current run only; evidence, handoff, policy, delegation, and repository state must still be current at commitment |
| Recoverability profile | Prefer additive, reversible, auditable changes; stop when rollback or recovery cannot be established |
| Admissibility result | `ALLOW`, `DENY`, or `FAIL_CLOSED` for the proposed transition, not for the automation as a whole |
| Commit-time validity | Re-check handoff version, target state, evidence freshness, authority, and stop conditions immediately before mutation |
| Output state | Verified repair, verified phase completion, updated handoff, next-task activation, blocker record, denial, or fail-closed result |
| Receipt chain | Run-specific receipt should bind event, derived elements, decision, action, verification, hashes/references, and resulting handoff state |
| Continuation rule | The next task may start only after current completion conditions are verified and the updated handoff explicitly declares it |

## Transition derivation path

```text
notification event
-> event identity and freshness check
-> repository and target resolution
-> handoff version resolution
-> proposed task or repair extraction
-> policy and delegation reference extraction
-> evidence collection
-> authority-class and scope evaluation
-> recoverability and stop-condition evaluation
-> ALLOW / DENY / FAIL_CLOSED
-> commit-time validity check
-> bounded action or no action
-> verification
-> run receipt
-> handoff continuation
```

A catalog entry describes the standing transition pattern. Each run still requires its own derived elements and receipt.

## Admissibility conditions

An automated transition is catalogued as admissible for operation only when all applicable conditions are satisfied:

1. The trigger can be associated with an identified repository or declared scope.
2. A current handoff exists and identifies the active task or permitted repair class.
3. The actor, target, proposed action, scope, policy reference, delegation reference, and evidence references can be derived.
4. The action remains within the handoff's declared authority class and boundary.
5. Required prerequisites, files, checks, and evidence are available and current.
6. The action is bounded and recoverable, or the handoff explicitly declares and authorizes the stronger consequence.
7. Commit-time validity can be checked immediately before mutation.
8. Completion can be verified through files, tests, checks, receipts, or other declared evidence.
9. The result and next task can be written back without fabricating standing.
10. Duplicate, stale, unrelated, and partial-progress events are rejected.

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
- derived transition-table elements;
- permitted and prohibited actions;
- verification requirements;
- commit-time validity requirements;
- recoverability and failure posture;
- current lifecycle state;
- receipt references.

## Receipt

The observatory installation receipt is stored at:

```text
receipts/admissible-automated-transitions-observatory-receipt.json
```

This receipt confirms that the catalog page, manifest, status artifact, validator, and navigation entry were installed. It does not certify the truth of every future event or grant authority to the automation.

Run-specific receipts remain required to show which transition-table elements were actually derived and whether the proposed action was allowed, denied, or failed closed.

## Run-specific final receipt

The schema for a completed automated transition is:

```text
schemas/automated-transition-run-receipt.schema.json
```

An illustrative, non-live receipt is published at:

```text
examples/automated-transition-run-receipt.json
```

A final run receipt binds:

- the event and run identity;
- origin class, actor, target, and scope;
- policy, delegation, and evidence references;
- the transition signature;
- the instantiated micro-node manifest reference;
- `ALLOW`, `DENY`, or `FAIL_CLOSED`;
- commit-time validity;
- action and verification results;
- input and output state hashes;
- prior receipt and resulting handoff references;
- Master-Records submission and reconstruction status.

The final run receipt is the continuity artifact intended for Master-Records custody. Master-Records may record its hash, continuity links, custody metadata, and reconstruction references. The observatory then renders a governed projection of those records.

```text
runtime evidence
-> final run receipt
-> Master-Records record
-> reconstruction
-> observatory continuity view
```

The example receipt is not evidence of a live automation run and is marked accordingly.

## Update protocol

The catalog should be updated whenever:

- an automation is created, materially changed, paused, retired, or superseded;
- its schedule, trigger class, authority source, or permitted effects change;
- a transition-table element or derivation source changes;
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

This page documents declared automated transitions, their derived transition-table elements, and their admissibility conditions. Publication here does not create execution authority, prove that every automation run succeeded, authorize cross-repository mutation, or replace run-specific receipts and evidence.
