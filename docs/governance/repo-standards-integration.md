# Repo Standards Integration

## Purpose

This page records how `StegVerse-Labs/admissibility-wiki` should reference the generalized `repo-standards` control-plane surface after the upstream release tag is created.

The page is intentionally release-gated. It may describe the pending integration path, but it must not treat an untagged upstream state as final release authority.

## Upstream Repository

```text
StegVerse-Labs/repo-standards
```

## Integration Role

`repo-standards` provides the reusable operating surface for repository governance and session orchestration:

- compact runtime bootstrap rules;
- task profiles;
- AI Entity Task Manager orchestration;
- workstream claims;
- task lifecycle rules;
- parallel execution rules;
- status and task-registry schemas;
- org-profile portability layer;
- validation and release-gate reporting;
- downstream sync preflight rules.

## Admissibility-Wiki Role

`admissibility-wiki` remains the public doctrine and vocabulary layer. It should reference `repo-standards` only as a standards and orchestration source, not as an execution authority.

This distinction matters:

| Layer | Function | Authority |
| --- | --- | --- |
| `repo-standards` | Defines reusable repo/session operating standards. | Standards and validation guidance. |
| `admissibility-wiki` | Explains admissibility concepts publicly. | Public vocabulary and doctrine only. |
| Runtime repos | Execute or simulate governed transitions. | Only as granted by their own policy, receipts, and validation path. |

## Release-Gated Reference Rule

Do not publish a final release reference until upstream has:

1. successful `Declared Tasks` validation on `main`;
2. release-readiness report updated;
3. Git tag/release created;
4. downstream sync issue activated.

Current known upstream state:

```text
Manual main validation: observed successful
Tag/release: pending outside current connector capability
```

## Post-Release Update

After the tag exists, update this page with:

```text
repo-standards release tag:
release URL:
bundle source:
validation report path:
org-profile adoption path:
downstream sync issue:
```

## Non-Claims

This page does not claim:

- that `repo-standards` executes transitions;
- that repository validation equals admissibility;
- that a release tag grants runtime authority;
- that a bundle install is sufficient for governance standing.

## Current Status

```text
PENDING_UPSTREAM_TAG_RELEASE
```
