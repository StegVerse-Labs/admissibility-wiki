# Wiki Standards Handoff Readiness

## Purpose

This handoff tells reviewers how to inspect the admissibility wiki standards visibility surface, run the single combined validation command, and verify that authoritative registry scope remains outside the wiki unless explicitly delegated.

## Single validation command

```bash
python tools/standards_visibility_automation.py
```

Expected output:

```text
ALLOW standards_visibility_automation_passed
```

## Indexed pages

```text
docs/standards/README.md
docs/standards/registry_backed_visibility_pattern.md
docs/standards/registry_backed_visibility_pattern_status.md
docs/standards/external-reviewable-artifact-repos.md
docs/standards/external-reviewable-artifact-repos-status.md
```

## Supporting automation

```text
tools/registry_backed_visibility_pattern_automation.py
tools/external_reviewable_artifact_repos_wiki_automation.py
tools/standards_index_automation.py
```

## Authoritative source boundary

The admissibility wiki is a downstream visibility surface. Authoritative registry scope remains in the relevant source repository unless explicitly delegated through a governed registry update.

## Initial authoritative source

```text
StegVerse-Labs/repo-standards
```

## Initial registered artifact repo

```text
StegVerse-Labs/soil-to-structure-matrix
```

## Reviewer sequence

1. Inspect `docs/standards/README.md`.
2. Inspect the registry-backed visibility pattern page.
3. Inspect the external reviewable artifact repos visibility page.
4. Run `python tools/standards_visibility_automation.py`.
5. Verify the authoritative registry in `StegVerse-Labs/repo-standards`.

## Boundary

This handoff provides reviewer navigation only. It does not change source registry scope, standards authority, repo review status, release status, deployment status, or artifact repo claims.
