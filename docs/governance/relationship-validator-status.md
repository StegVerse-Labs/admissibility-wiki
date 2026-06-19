---
title: Relationship Validator Status
---

# Relationship Validator Status

## Purpose

This page records the local validator for the accepted relationship-status summary.

## Validator

```text
scripts/check-relationship-status-summary.mjs
```

## Command

```text
node scripts/check-relationship-status-summary.mjs
```

## Checked Source

```text
docs/governance/relationship-status-summary.md
```

## Required Records

```text
proposal.example.005 / decision.example.005
proposal.example.006 / decision.example.006
proposal.example.007 / decision.example.007
proposal.example.008 / decision.example.008
```

## Required Boundary

```text
All four records must remain ALLOW_AS_OVERLAP.
Equivalent status must remain not accepted.
```

## Activation Boundary

This validator does not change public activation state.

Public activation still requires deployment, DNS, HTTPS, ontology reachability, and governance-record reachability verification.

## Next Safe Action

Future relationship work should use a new proposal ID only for a materially new source family.
