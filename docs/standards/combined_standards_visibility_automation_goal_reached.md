# Combined Standards Visibility Automation Goal Reached

## Goal

Build a combined standards visibility automation that runs all current standards visibility validators in one command.

## Done state

The admissibility wiki now contains:

- combined automation at `tools/standards_visibility_automation.py`;
- pattern automation at `tools/registry_backed_visibility_pattern_automation.py`;
- external artifact repo visibility automation at `tools/external_reviewable_artifact_repos_wiki_automation.py`;
- standards index automation at `tools/standards_index_automation.py`.

## Required command

```bash
python tools/standards_visibility_automation.py
```

## Expected pass condition

```text
ALLOW standards_visibility_automation_passed
```

## Validators covered

```text
tools/validate_registry_backed_visibility_pattern.py
tools/validate_external_reviewable_artifact_repos_wiki.py
tools/validate_standards_index.py
```

## Boundary

This goal provides combined validation for downstream standards visibility only. It does not change source registry scope, standards authority, repo review status, release status, deployment status, or artifact repo claims.

## Next goal

Build wiki standards handoff readiness so reviewers know the single command, indexed pages, and authoritative source boundary.
