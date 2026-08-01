---
title: Personal Data Control and Deletion Layer
sidebar_label: Personal Data Control and Deletion
slug: /standards/personal-data-control-and-deletion-layer
---

# Personal Data Control and Deletion Layer

## Purpose

This layer prevents account creation, authenticated testing, or data ingestion from becoming a one-way boundary in which entry is available but access, restriction, deletion, and closure are not operationally reachable.

It applies reciprocally to StegVerse and to external frameworks reviewed by StegVerse.

## Core rule

> A system may not claim governed handling of personal or account-linked data unless the data subject can identify the responsible controller, submit an authenticated request through a functioning channel, observe the request state, receive a bounded response, challenge an incomplete response, and obtain a durable completion receipt.

A theoretical legal right is not an activated governance capability.

## Required states

Every personal-data request must move through explicit states:

```text
NOT_REQUESTED
-> REQUEST_PREPARED
-> DELIVERY_ATTEMPTED
-> DELIVERED
-> ACKNOWLEDGED
-> IDENTITY_VERIFICATION_REQUIRED | IDENTITY_VERIFIED
-> PROCESSING_RESTRICTED
-> INVENTORY_PROVIDED
-> DELETION_IN_PROGRESS
-> PROCESSOR_PROPAGATION_IN_PROGRESS
-> COMPLETED | PARTIALLY_COMPLETED | DENIED | CHANNEL_FAILED
-> APPEALED | CLOSED
```

No state may be inferred from silence.

## Minimum request surface

A conforming implementation must provide:

```text
controller identity
privacy or data-rights contact
account deletion route
authenticated request method
request identifier
acknowledgment receipt
retention and exception explanation
processor or service-provider propagation status
appeal route
completion receipt
```

## Fail-closed rules

```text
account creation available + deletion route unavailable
-> DATA_CONTROL_LAYER_FAIL_CLOSED

request channel unavailable
-> CHANNEL_FAILED
-> preserve evidence
-> prohibit claim that the request was denied
-> continue alternate-route discovery automatically

request delivered + no acknowledgment evidence
-> ACKNOWLEDGMENT_NOT_ESTABLISHED

controller identity unresolved
-> CONTROLLER_NOT_ESTABLISHED

processor propagation unverified
-> DELETION_COMPLETION_NOT_ESTABLISHED

public record preserved
!= continued authority to process private account data
```

## Internal task execution rule

This layer does not create unlocated or external tasks. Every task must contain:

```text
task_id
repository
path
owner_role
input_evidence
completion_predicate
status
receipt_path
```

A task is incomplete only when its completion predicate is false. The repository validator recomputes status from files rather than relying on prose.

## Initial implementation locations

```text
Standard:
StegVerse-Labs/admissibility-wiki/docs/standards/personal-data-control-and-deletion-layer.md

Machine-readable task and capability manifest:
StegVerse-Labs/admissibility-wiki/static/data/governance/personal-data-control-layer.v1.json

Activation status:
StegVerse-Labs/admissibility-wiki/static/status/personal-data-control-layer-status.json

Deterministic validator:
StegVerse-Labs/admissibility-wiki/scripts/check_personal_data_control_layer.py

Aggregate canonical binding:
StegVerse-Labs/admissibility-wiki/scripts/check_admissibility_automation_handoff.py

First external observation:
StegVerse-Labs/admissibility-wiki/docs/external-frameworks/ta-14-account-data-request-channel-observation-2026-08-01.md
```

## Authority boundary

```text
layer PASS != legal compliance adjudication
request receipt != proof of deletion
account closure != processor deletion
public documentation != controller identity
channel availability != request completion
preserved evidence != permission for secondary use
StegVerse review != regulatory enforcement
```
