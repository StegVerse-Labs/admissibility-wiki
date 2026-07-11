---
title: Cedar Observation Capture Runbook
---

# Cedar Observation Capture Runbook

## Purpose

Capture exact Cedar authorization output without treating authorization as StegVerse execution authority or compatibility proof.

The harness is implementation-neutral because Cedar can be exposed through different CLIs, libraries, and wrappers. The operator must supply the exact version command and authorization command template used by the selected implementation.

## Installed artifacts

```text
docs/external-frameworks/capture/cedar/policy.cedar
docs/external-frameworks/capture/cedar/request-allow.json
docs/external-frameworks/capture/cedar/request-deny.json
scripts/capture_cedar_observation.py
```

## Required execution form

```bash
python scripts/capture_cedar_observation.py \
  --implementation-id '<exact implementation name>' \
  --version-command '<command that prints exact version>' \
  --evaluate-command '<command using {policy} and {request} placeholders>' \
  --request docs/external-frameworks/capture/cedar/request-allow.json \
  --case-id cedar-allow-read-001 \
  --output reports/external-frameworks/cedar-allow-observation.json
```

Repeat with `request-deny.json` and a distinct output path.

## Receipt contents

The generated `captured_unverified` receipt records:

- exact implementation identifier;
- exact version command and output;
- exact evaluation command;
- UTC capture time;
- policy and request content;
- stdout, stderr, and exit code;
- SHA-256 hashes of policy, request, stdout, and stderr;
- authority and freshness context;
- replay commands and expected hashes;
- explicit limitations.

## Advancement rule

A capture remains `captured_unverified` until another environment independently replays the same pinned policy and request and confirms the relevant hashes and semantic output.

```text
Cedar PERMIT != execution authority
Cedar FORBID != StegVerse certification
single run != replayability
matching replay != current delegation
```
