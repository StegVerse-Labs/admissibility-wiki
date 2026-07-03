---
title: Repository Preflight
---

# Repository Preflight

## Status

```text
repo_preflight: installed
source_standard: StegVerse-Labs/repo-standards ST-015 Repository Preflight
execution_surface: single canonical validation workflow or local command
status_artifact: static/status/repo-preflight-status.json
script: scripts/repo_preflight.mjs
```

## Purpose

Repository preflight is a diagnostic layer for catching validation, generated-artifact, workflow, handoff, status-artifact, and MDX render hazards before GitHub Actions becomes the repair loop.

The immediate lesson from the governed LLM / admissibility-wiki activation work is that validators should converge locally before publication. Preflight records the checks that help expose multiple likely blockers in one pass.

## Local Command

```bash
node scripts/repo_preflight.mjs
```

The command writes:

```text
static/status/repo-preflight-status.json
```

## Checked Categories

```text
handoff_state
workflow_policy
governance_validation
status_artifact_state
generated_artifact_state
render_build
```

## Boundary

```text
Preflight does not replace release readiness.
Preflight does not authorize deployment.
Preflight does not prove runtime admissibility.
Preflight does not create execution authority.
```

## Downstream Use

Other StegVerse repositories should adapt the checker to their own stack while preserving:

1. PASS / WARN / FAIL / SKIP classes;
2. category-separated findings;
3. a machine-readable status artifact;
4. no additional active workflow requirement;
5. clear non-claims.
