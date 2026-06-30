# Governed Output Classes

## Purpose

This page records the initial public registry of output classes for governed transition results.

A desired output is not treated as valid merely because it can be requested or produced. It remains governed until the relevant transition reaches a valid commitment point.

## Core output path

```text
admitted input or request
  -> governed evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output
```

## Registered output classes

| Output class | Description | Current status |
| --- | --- | --- |
| Admitted response | A response or explanation that has passed the applicable governance boundary. | Registered. |
| Denial receipt | A receipt showing that a proposed transition was denied. | Registered. |
| Fail-closed receipt | A receipt showing that the system stopped because required authority, evidence, or standing was missing. | Registered. |
| Committed repo change | A repository mutation that has passed the applicable transition and authority path. | Registered. |
| STRP handoff | A state transition record package passed to another ecosystem, repo, entity, or layer. | Registered. |
| Receipt-chain continuation | A continuity record that links a prior transition to the next governed transition. | Registered. |
| State-transition summary | A bounded summary of what was requested, evaluated, allowed, denied, or failed closed. | Registered. |

## Boundary

Registration as an output class does not make any output instance valid by itself.

Each output instance must be tied to the applicable transition record, authority posture, and receipt-chain requirements before it can become consequence-bearing state.

## Current status

```text
GOVERNED_OUTPUT_CLASS_REGISTRY_PRESENT
```
