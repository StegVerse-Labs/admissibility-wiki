---
title: External Framework Command Capture Runbook
---

# External Framework Command Capture Runbook

## Purpose

This runbook operates the reusable external-framework command capture engine for MCP, A2A, Guardrails AI, Llama Guard, and NeMo Guardrails.

The engine records a single exact execution as `captured_unverified`. It does not claim replayability, compatibility, certification, standing, or execution authority.

## Required inputs

- a framework capture manifest;
- an exact implementation identifier;
- a command that prints the exact runtime, client, server, or model version;
- an execution command that accepts canonical JSON on standard input;
- the complete configuration, authorization, and freshness context needed to interpret the result.

## Commands

```bash
python scripts/capture_external_command_observation.py \
  --manifest docs/external-frameworks/capture/mcp/capture-manifest.json \
  --implementation '<exact client/server implementation>' \
  --version-command '<exact version command>' \
  --execute-command '<exact command that reads JSON from stdin>'
```

Replace the manifest for:

```text
docs/external-frameworks/capture/a2a/capture-manifest.json
docs/external-frameworks/capture/guardrails-ai/capture-manifest.json
docs/external-frameworks/capture/llama-guard/capture-manifest.json
docs/external-frameworks/capture/nemo-guardrails/capture-manifest.json
```

## Receipt contents

The engine writes:

- framework and case identifiers;
- exact implementation identifier;
- exact version and execution commands;
- UTC capture timestamp;
- canonical source and source-version posture;
- exact input and output;
- exit code and standard error;
- SHA-256 hashes for the manifest, input, output, error output, and version output;
- explicit authority and freshness boundaries;
- limitations;
- replay instructions.

## State boundary

```text
capture harness installed != runtime executed
captured_unverified != observed_partial
single matching output != replayability
protocol response != authority
classifier result != admissibility
blocked flow != certification
allowed flow != execution authority
```

An independent replay must verify the exact versioned artifacts and output hashes before the record can advance beyond `captured_unverified`.
