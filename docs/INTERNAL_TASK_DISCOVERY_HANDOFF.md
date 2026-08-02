# Internal Task Discovery Handoff

## Determination

```text
Layer: continuous internal task discovery
Repository: StegVerse-Labs/admissibility-wiki
State: BUILT_AND_ACTIVATED_INTERNAL
External tasks: none
Manual task requirement: none
```

This layer observes repository-owned completion evidence, creates or refreshes located internal tasks, and prevents missing observations from being converted into external work or global development stops.

## Authoritative locations

```text
Discovery runner: scripts/discover_internal_tasks.py
Discovery validator: scripts/check_internal_task_discovery.py
Discovered task registry: static/status/internal-task-registry.json
Discovery report: reports/internal-task-discovery.json
Task mesh registry: static/status/wiki-public-anchor-task-mesh-registry.json
Task mesh runner: scripts/run_wiki_public_anchor_task_mesh.py
Canonical workflow: .github/workflows/validate-chain-continuation.yml
```

## Discovery contract

Every discovered task records:

```text
task_id
title
owner_record
work_locations
completion_path
completion_field
completion_value
completion_predicate
fallback
priority
state
last_observed
blocking=false
external_task=false
```

## Active discovered tasks

### DISC-TA14-PUBLICATION

```text
Owner: docs/external-frameworks/TA14_PUBLICATION_ACTIVATION_COORDINATION.md
Source: docs/external-frameworks/ta-14-testing-support-determination-2026-08-01.md
Observer: scripts/observe_ta14_determination_publication.py
Evidence: reports/ta14-determination-publication-observation.json
Completion: public_state=PASS_PUBLIC_CONTENT_VERIFIED
```

### DISC-TASK-MESH

```text
Owner: docs/WIKI_PUBLIC_ANCHOR_TASK_MESH_HANDOFF.md
Runner: scripts/run_wiki_public_anchor_task_mesh.py
Validator: scripts/check_wiki_public_anchor_task_mesh.py
Evidence: reports/wiki-public-anchor-task-mesh-execution.json
Completion: overall_state=PASS_INTERNAL
```

## Non-halting behavior

```text
missing report -> READY_INTERNAL
failed observation -> READY_INTERNAL with exact evidence retained
missing external evidence -> evidence gap, never an external task
one discovered task failure -> unrelated work continues
no task may omit repository locations or a completion predicate
```

## Continuation sequence

```text
run scripts/discover_internal_tasks.py
-> validate static/status/internal-task-registry.json
-> register discovery queue in the task mesh
-> execute each queue independently
-> preserve exact failures
-> re-run discovery
-> mark tasks COMPLETE_INTERNAL only from repository-owned completion evidence
-> continue canonical validation, build, deploy, and public verification
```

This layer coordinates internal development only. It grants no certification, custody, reviewer standing, government recognition, endorsement, or execution authority.
