# iOS No-Period Mirror

## Assumption

Some clients cannot reliably create or move paths that begin with a leading period. This repository may use `iosnoperiod/` as a mirror for workflow bootstrap files when needed.

## Mapping

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml -> .github/workflows/validate-chain-continuation.yml
iosnoperiod/github/workflows/validate.yml -> .github/workflows/validate.yml
```

The left side is the iOS-safe mirror path. The right side is the canonical GitHub Actions path.

## Current status

`iosnoperiod/github/workflows/validate.yml` contains the Goal 5 wiki validation path:

```text
npm ci
python scripts/check_governed_llm_pages.py
python scripts/check_governed_llm_demo_docs.py
npm run build
```

The mirror preserves the max-two-workflows rule. It is intended to become the single canonical validate workflow if canonical workflow activation is authorized.

The controlled patch note for the older chain-continuation workflow is:

```text
iosnoperiod/github/workflows/validate-chain-continuation.patch.md
```

## Done Criteria

The mirror is ready when the workflow file exists under `iosnoperiod/github/workflows/` and can be copied to the canonical path without content changes.

Until a mirror is copied to its canonical `.github/workflows/` destination, the mirror must be treated as prepared-but-not-activated CI evidence.

## Boundary

The mirror is not activation evidence. It is a path-safe copy of workflow content.
