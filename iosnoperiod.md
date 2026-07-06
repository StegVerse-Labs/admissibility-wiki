# iOS No-Period Mirror

## Assumption

Some clients cannot reliably create or move paths that begin with a leading period. This repository may use `iosnoperiod/` as a mirror for workflow bootstrap files when needed.

## Mapping

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml -> .github/workflows/validate-chain-continuation.yml
```

The left side is the iOS-safe mirror path. The right side is the canonical GitHub Actions path.

## Current status

`iosnoperiod/github/workflows/validate-chain-continuation.yml` is the only approved iOS mirror workflow file.

The mirror preserves the single-canonical-workflow policy enforced by `scripts/check_workflow_sprawl.py`:

```text
active workflows must equal [validate-chain-continuation.yml]
iOS mirror workflows must equal [validate-chain-continuation.yml]
```

Legacy or prepared-but-not-activated workflow files must not remain in `iosnoperiod/github/workflows/` because the mirror is validated as an activation-facing workflow surface.

The controlled patch note for the older chain-continuation workflow is:

```text
iosnoperiod/github/workflows/validate-chain-continuation.patch.md
```

## Done Criteria

The mirror is ready when exactly one workflow file exists under `iosnoperiod/github/workflows/` and can be copied to the canonical path without content changes:

```text
validate-chain-continuation.yml
```

Until a mirror is copied to its canonical `.github/workflows/` destination, the mirror must be treated as prepared-but-not-activated CI evidence.

## Boundary

The mirror is not activation evidence. It is a path-safe copy of workflow content.
