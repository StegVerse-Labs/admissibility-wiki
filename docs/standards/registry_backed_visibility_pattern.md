# Registry-Backed Visibility Pattern

## Purpose

This page generalizes the downstream visibility pattern used for external reviewable artifact repos so additional standards can be displayed in the admissibility wiki without moving authority away from their source registries.

## Pattern

A downstream standards visibility page should declare:

- the visible standard title;
- the authoritative source repository;
- the authoritative standard path;
- the authoritative registry path when one exists;
- the upstream Site mirror path when one exists;
- the local wiki visibility path;
- the explicit boundary that the wiki is display-only.

## Required source-of-truth rule

The wiki must not become the registry authority unless the authoritative source repo explicitly delegates that role through a governed registry update.

## Required validation rule

Each registry-backed wiki page should have a validator that checks:

- the local visibility page exists;
- the local status page exists;
- the authoritative source repo is named;
- the registry path is named when applicable;
- the display-only boundary is present.

## Current applied standard

```text
docs/standards/external-reviewable-artifact-repos.md
```

## Current automation

```bash
python tools/external_reviewable_artifact_repos_wiki_automation.py
```

## Boundary

This pattern is a publication and visibility rule only. It does not change source registry scope, standards authority, repo review status, release status, deployment status, or artifact repo claims.
