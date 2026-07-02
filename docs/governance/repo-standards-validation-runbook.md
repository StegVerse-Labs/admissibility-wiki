# Repo Standards Validation Runbook

## Purpose

This runbook records the current single validation command for the repo-standards integration and installation bundle task.

## Current Command

```bash
python scripts/check_repo_standards_bundle.py
```

## Included Checks

```text
scripts/check_repo_standards_integration.py
scripts/check_repo_standards_downstream_activation.py
```

## Expected Result

```text
REPO STANDARDS BUNDLE: PASS - integration and downstream activation checks passed
```

## Current External Gates

```text
upstream repo-standards Git tag/release
local validation execution evidence
public deployment verification after site deploy
```

## Current Status

```text
READY_FOR_LOCAL_VALIDATION
```
