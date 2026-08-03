# Admissibility Wiki Mirror Handoff Pointer

## Canonical repository handoff

The repository-wide handoff and task source of truth for `StegVerse-Labs/admissibility-wiki` is:

```text
ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
```

This file is retained only as a compatibility pointer for sessions or tools that search for the older `ADMISSIBILITY_MIRROR_HANDOFF.md` name. It does not own a separate task queue, workflow, claim, release condition, or authority surface.

## Goal-specific handoffs

Read a goal-specific handoff only after reading the canonical repository handoff:

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
  public-anchor reconstruction, dockets, and internal task execution

docs/WIKI_PUBLICATION_PIPELINE_MIRROR_HANDOFF.md
  completed legacy Pages publication repair and run-bound evidence

docs/WIKI_PUBLIC_ANCHOR_ACTIVATION_COORDINATION.md
  public-anchor activation coordination

docs/AI_LED_RADIOLOGY_MIRROR_HANDOFF.md
  AI-led radiology execution boundary

docs/ECOSYSTEM_CHAT_ACTIVATION_MIRROR_HANDOFF.md
  Ecosystem Chat activation projection

docs/MORRISON_RUNTIME_PROMOTION_HANDOFF.md
  Morrison Runtime promotion

docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md
  completed MindForge route publication and continuing evidence boundaries

docs/OBSERVER_BOUNDARY_MIRROR_HANDOFF.md
  three-stage and three-role observer boundary
```

Where a goal-specific handoff contains an older repository-wide source-of-truth declaration, the hierarchy in this pointer and `ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` supersedes that declaration. Goal-specific files retain authority only for their named bounded goals.

## Current publication standing

```text
legacy Pages repair: COMPLETE
MindForge public rendering: VERIFIED
canonical issue #56: CLOSED_COMPLETED
current CAT publication session inventory:
  data/session-consolidation/admissibility-wiki-publication-session-inventory.v1.json
canonical deployment workflow:
  .github/workflows/validate-chain-continuation.yml
separate publication observer workflow: none
manual user tasks: none
```

The directly observed publication evidence is recorded in:

```text
static/status/cat-governance-publication-verification.v1.json
docs/WIKI_PUBLICATION_PIPELINE_MIRROR_HANDOFF.md
docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md
GitHub Actions run 30837466398
```

## Downstream mapping

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

`StegVerse-Labs/Sit` does not exist and is not a destination.

## Boundary

```text
publication availability != semantic validation success
publication != proof
public rendering != authority
workflow success != certification
workflow failure != automatic deployment failure
route reachability != substantive correctness
```

## Archive posture

The legacy publication-repair and MindForge-publication tasks are complete, their claims are released, issue #56 is closed, and their continuation state is durable. Any current session must use the canonical repository handoff and session inventory to determine whether a separate active validation claim remains.
