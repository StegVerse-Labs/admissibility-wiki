# Governed Transition Map

## Purpose

This page ties governed input classes to governed output classes through the shared StegVerse transition path.

The map is not a permission table. It is a public explanation of how candidate inputs and desired outputs remain bound to transition governance.

## Shared transition path

```text
input class instance
  -> governed ingestion
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> output class instance
```

## Input-to-output map

| Input class | Possible governed output classes |
| --- | --- |
| External framework outputs | Admitted response, denial receipt, fail-closed receipt, STRP handoff, state-transition summary |
| LLM or agent outputs | Admitted response, denial receipt, fail-closed receipt, STRP handoff, receipt-chain continuation, state-transition summary |
| Human requests | Admitted response, denial receipt, fail-closed receipt, committed repo change, STRP handoff, state-transition summary |
| Repo tasks | Committed repo change, denial receipt, fail-closed receipt, receipt-chain continuation, state-transition summary |
| SDK requests | Admitted response, denial receipt, fail-closed receipt, STRP handoff, receipt-chain continuation, state-transition summary |
| Runtime observations | Denial receipt, fail-closed receipt, STRP handoff, receipt-chain continuation, state-transition summary |
| Receipt-chain continuations | Receipt-chain continuation, admitted response, denial receipt, fail-closed receipt, STRP handoff, state-transition summary |

## Boundary

A listed output is only a possible governed result. It is not authorized by this map.

Each concrete transition still requires current standing, applicable authority, evidence sufficiency, boundary recoverability, and receipt binding.

## Current status

```text
GOVERNED_TRANSITION_MAP_PRESENT
```
