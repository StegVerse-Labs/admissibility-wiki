---
title: Publication Chain Guard
---

# Publication Chain Guard

## Purpose

The Admissibility Wiki must be able to publish visible public updates when source content changes or when an allowed wiki transition is applied.

A full governance validator failure should not silently hide otherwise valid page updates.

## Current Guard Rule

```text
Pages publication must have a build-only job inside the canonical workflow.
Full governance validation may run separately.
Pages publication must not depend only on npm run validate.
Manual republish from main must remain available through workflow_dispatch.
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

The repo preserves these paths inside one canonical workflow:

```text
Build-only Pages publication job
  Purpose: make public page state visible.
  Command boundary: npm run build.

Governance validation job
  Purpose: validate registries, receipts, manifests, and governance artifacts.
  Command boundary: npm run validate.

Manual republish path
  Purpose: recover public publication without adding a second workflow.
  Trigger boundary: workflow_dispatch on main.
```

## Current Workflow Path

```text
github/workflows/validate-chain-continuation.yml
```

The path is shown without the leading dot for iOS readability. The actual workflow path uses the leading dot directory.

## Non-Claims

```text
Build-only publication does not prove governance validity.
Governance validation does not itself publish public state.
A committed wiki update is not complete until public visibility can be verified.
A public page is not a canonical formalism source.
A single canonical workflow does not remove the separation between validation and publication jobs.
```

## Guard Check

The publication guard validates that the canonical workflow includes:

```text
build-pages
deploy-pages
verify-public-pages
npm run build
actions/deploy-pages@v4
push on main
workflow_dispatch on main
```
