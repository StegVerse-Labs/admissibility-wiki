# iOS No-Period Mirror

## Assumption

Some clients cannot reliably create or move paths that begin with a leading period. This repository may use `iosnoperiod/` as a mirror for workflow bootstrap files when needed.

## Mapping

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml -> .github/workflows/validate-chain-continuation.yml
```

The left side is the iOS-safe mirror path. The right side is the canonical GitHub Actions path.

## Done Criteria

The mirror is ready when the workflow file exists under `iosnoperiod/github/workflows/` and can be copied to the canonical path without content changes.

## Boundary

The mirror is not activation evidence. It is a path-safe copy of workflow content.
