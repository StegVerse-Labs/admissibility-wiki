# iOS No-Period Mirror

## Assumption

Some clients cannot reliably create or move paths that begin with a leading period. This repository may use `iosnoperiod/` as a mirror for workflow bootstrap files when needed.

## Mapping

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml -> .github/workflows/validate-chain-continuation.yml
```

The left side is the iOS-safe mirror path. The right side is the canonical GitHub Actions path.

## Current status

The canonical workflow is ahead of the iOS-safe mirror after governed LLM route verification was added.

The controlled patch note is:

```text
iosnoperiod/github/workflows/validate-chain-continuation.patch.md
```

## Done Criteria

The mirror is ready when the workflow file exists under `iosnoperiod/github/workflows/` and can be copied to the canonical path without content changes.

Until the patch note is applied to the mirror file, the mirror must be treated as stale and not activation-ready.

## Boundary

The mirror is not activation evidence. It is a path-safe copy of workflow content.
