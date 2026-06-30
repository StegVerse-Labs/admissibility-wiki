# Governed Input Classes

## Purpose

This page records the initial public registry of input classes that may enter StegVerse as governed transition candidates.

Each input class is governed by the same high-level transition boundary:

```text
input or request
  -> governed ingestion
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output
```

## Registered input classes

| Input class | Description | Current status |
| --- | --- | --- |
| External framework outputs | Outputs, reports, traces, or artifacts produced by external frameworks. | Registered as governed input class. |
| LLM or agent outputs | Outputs produced by LLM interfaces, agents, or tool-capable local systems. | Registered as governed input class. |
| Human requests | Human-originated requests, claims, proposals, corrections, or desired outputs. | Registered as governed input class. |
| Repo tasks | Repository tasks, patches, manifests, plans, workflow results, and build artifacts. | Registered as governed input class. |
| SDK requests | Requests entering through SDK, API, or adapter surfaces. | Registered as governed input class. |
| Runtime observations | Runtime status, traces, monitoring events, or system observations. | Registered as governed input class. |
| Receipt-chain continuations | Prior transition receipts, STRP records, or continuity records proposed for continuation. | Registered as governed input class. |

## Boundary

Registration as an input class does not mean the class is automatically admissible.

Each instance must still pass the applicable governed ingestion, CGE, GCAT/BCAT, Transition Table, and receipt-chain requirements before it can become consequence-bearing state.

## Current status

```text
GOVERNED_INPUT_CLASS_REGISTRY_PRESENT
```
