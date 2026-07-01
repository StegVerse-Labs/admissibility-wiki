# Standards Index

## Purpose

This index lists registry-backed standards visibility pages in the admissibility wiki and the validation commands used to confirm that they remain display-only mirrors of authoritative source registries.

## Registry-backed visibility pattern

```text
docs/standards/registry_backed_visibility_pattern.md
docs/standards/registry_backed_visibility_pattern_status.md
```

Validation:

```bash
python tools/registry_backed_visibility_pattern_automation.py
```

## External reviewable artifact repos

```text
docs/standards/external-reviewable-artifact-repos.md
docs/standards/external-reviewable-artifact-repos-status.md
```

Validation:

```bash
python tools/external_reviewable_artifact_repos_wiki_automation.py
```

## Authoritative source rule

The admissibility wiki is a downstream visibility surface. Authoritative registry scope remains in the relevant source repository unless explicitly delegated through a governed registry update.

## Boundary

This index does not change source registry scope, standards authority, repo review status, release status, deployment status, or artifact repo claims.
