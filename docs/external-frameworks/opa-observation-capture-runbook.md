---
title: OPA Observation Capture Runbook
---

# OPA Observation Capture Runbook

## Purpose

This runbook produces an exact, hashed, non-authorizing OPA observation receipt. It does not treat an OPA policy decision as execution authority, compatibility proof, or StegVerse standing.

## Inputs

```text
docs/external-frameworks/capture/opa/policy.rego
docs/external-frameworks/capture/opa/input-allow.json
docs/external-frameworks/capture/opa/input-deny.json
scripts/capture_opa_observation.py
```

## Capture commands

```bash
python scripts/capture_opa_observation.py \
  --input docs/external-frameworks/capture/opa/input-allow.json \
  --case-id opa-allow-read-001 \
  --output reports/external-frameworks/opa-allow-read-001.json

python scripts/capture_opa_observation.py \
  --input docs/external-frameworks/capture/opa/input-deny.json \
  --case-id opa-deny-write-001 \
  --output reports/external-frameworks/opa-deny-write-001.json
```

The harness requires a locally available `opa` executable. It captures:

```text
OPA version
UTC timestamp
exact policy and input paths
exact query and command
stdout and stderr
exit code
policy, input, stdout, and stderr SHA-256 hashes
authority and freshness context
limitations
replay command and required files
```

## Evidence state

A successful first execution produces:

```text
capture_state: captured_unverified
```

That state may advance only after an independent replay confirms the pinned policy, input, runtime version, output, and hashes.

## Boundary

```text
OPA ALLOW != execution authority
OPA DENY != StegVerse certification
single capture != replayability
matching output != current delegation
capture receipt != compatibility proof
```

The output remains evidence for a Commitment Candidate. Current authority and admissibility must still be reconstructed at the commit boundary.
