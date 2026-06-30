# Ecosystem Capability Status

## Purpose

This page explains the machine-readable ecosystem capability status example.

The status example shows how a capability can be implemented and internally validated while still remaining unreleased, publicly unverified, and non-operational.

## Status artifact

```text
static/status/ecosystem-capability-status.example.json
```

## Validator

```text
scripts/check_ecosystem_capability_status_example.py
```

## Current example state

```text
current_state: internally_validated
implemented: true
internally_validated: true
release_authorized: false
publicly_verified: false
operational: false
deprecated: false
```

## Boundary

A status record is not authority. Operational standing still requires current governance standing, release evidence, public verification evidence, and receipt binding.

## Current status

```text
ECOSYSTEM_CAPABILITY_STATUS_PAGE_PRESENT
```
