# Repo Standards Installation Bundle

## Purpose

This page defines the release-gated bundle installation path for applying `repo-standards` into another organization or repository ecosystem.

It is part of the admissibility-wiki public explanation layer. It does not perform installation, grant authority, or mark any downstream repository as admissible by itself.

## Upstream Source

```text
StegVerse-Labs/repo-standards
```

## Current Upstream State

```text
manual_main_validation: success
release_readiness: tag_allowed_true
tag_release: pending_outside_connector
```

## Bundle Contents Expected After Tag

A complete release bundle should include:

```text
runtime/
orchestration/
task-profiles/
standards/
schemas/
templates/
tools/
config/org-profile.yaml
docs/ORG_PROFILE_ADOPTION.md
REPO_STANDARDS_MIRROR_HANDOFF.md
reports/release-readiness.report.json
reports/downstream-sync-preflight.report.md
orchestration/task-registry.json
```

## Installation Boundary

Installing the bundle into another organization means the target organization receives reusable standards, validation tools, runtime bootstrap rules, and task-manager structure.

Installation does not mean:

- the target organization has execution authority;
- the target repository is admissible;
- downstream runtime decisions are valid;
- StegVerse governance has accepted the target as a trusted actor;
- local validation can be skipped.

## Required Target-Side Steps

1. Copy or import the release bundle.
2. Edit `config/org-profile.yaml` for the target organization.
3. Create or update the target `*_MIRROR_HANDOFF.md`.
4. Run the target validator.
5. Record validation evidence.
6. Declare downstream sync targets.
7. Treat any runtime authority as separate from repository-standards installation.

## Cross-Org Install Test

The first cross-org installation should prove:

| Test | Required Result |
| --- | --- |
| Org profile replacement | Target org values replace StegVerse defaults without editing core runtime files. |
| Handoff discovery | Target handoff becomes the local source of truth. |
| Validator execution | Target validator produces recorded evidence. |
| Downstream sync queue | Target-specific downstream destinations are declared. |
| Authority boundary | No install claim becomes runtime authority. |

## Release-Gated Placeholder

After the upstream release is created, update:

```text
repo_standards_release_tag:
repo_standards_release_url:
bundle_source:
bundle_hash:
validation_report:
first_cross_org_target:
```

## Current Status

```text
PENDING_UPSTREAM_TAG_RELEASE
```
