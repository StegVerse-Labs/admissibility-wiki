---
title: Publication Chain Guard
---

# Publication Chain Guard

## Purpose

The Admissibility Wiki must be able to publish visible public updates when source content changes or when an allowed wiki transition is applied.

A full governance validator failure should not silently hide otherwise valid page updates.

## Current Guard Rule

```text
Pages publication must have a build-only path.
Full governance validation may run separately.
Pages publication must not depend only on npm run validate.
```

## Why This Exists

The repo has previously shown this failure mode:

```text
repository commits succeed
workflow/status visibility is empty or absent
visible public page does not update
full validation is coupled to Pages deploy
```

That is not only a deployment problem. It mirrors the same class of transition problem the wiki is meant to govern:

```text
allowed mutation exists
publication transition does not complete
observer sees no public state change
claim is not externally verifiable
```

## Required Publication Paths

The repo should preserve two separate paths:

```text
Build-only Pages publication
  Purpose: make public page state visible.
  Command boundary: npm run build.

Governance validation
  Purpose: validate registries, receipts, manifests, and governance artifacts.
  Command boundary: npm run validate.
```

## Current Workflow Paths

```text
github/workflows/pages-build-only.yml
github/workflows/deploy.yml
```

Paths are shown without the leading dot for iOS readability. Actual workflow paths use the leading dot directory.

## Non-Claims

```text
Build-only publication does not prove governance validity.
Governance validation does not itself publish public state.
A committed wiki update is not complete until public visibility can be verified.
A public page is not a canonical formalism source.
```

## Next Safe Build Target

Add a validator that checks the build-only Pages workflow remains present and does not run `npm run validate` before publication.
