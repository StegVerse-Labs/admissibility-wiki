# External Translation Automation Status

## Goal

```text
Goal: Eliminate manual validation and reconstruction tasks from the external physics translation chain.
Repository: StegVerse-Labs/admissibility-wiki
State: checkpoint_reached
Automation posture: AUTOMATED_FAIL_CLOSED
```

## Canonical Automation

The external translation chain is registered inside the repository's single canonical workflow:

```text
.github/workflows/validate-chain-continuation.yml
```

The workflow runs on:

```text
push
pull_request
workflow_dispatch
hourly schedule at minute 17
```

No separate workflow is required for translation records, bibliographic intake, promotion governance, locator routing, specialist receipts, or supersession evaluation.

## Automatic Execution Sequence

```text
ST-017 sandbox
-> generate external translation reconstruction receipt
-> validate disciplinary translation records
-> validate mathematics crosswalk
-> validate external physics records
-> validate bibliographic intake
-> validate promotion governance
-> validate locator and specialist routing
-> validate review receipts and supersession
-> validate reconstruction receipt
-> embed reconstruction receipt in full validation report
-> enforce canonical validation result
```

## Generated Evidence

```text
reports/external-translation/reconstruction-receipt.json
reports/full_validation_chain_report.json#external_translation_reconstruction
```

The reconstruction receipt hashes every machine-readable input and verifies that the locator, route, required review classes, current promotion decision, and supersession state agree in the same run.

## Current Fail-Closed State

```text
locator_verification: UNRESOLVED
specialist_receipts: 3 placeholder_fail_closed
current_decision: decision-lai-intake-defer-v0-1
supersession_result: DEFER_NO_SUPERSESSION
```

Every canonical validation run regenerates this posture. No manual coordination is required to preserve the deferral or detect inconsistent records.

## Removed Workflow Sprawl

The standalone promotion-governance and source-locator workflows were removed after their validators were registered in the canonical chain. Their obsolete iOS mirrors were also removed.

The canonical workflow remains the only executable workflow surface for this chain.

## Manual Tasks

```text
manual_tasks_required: none
```

A stable external locator and actual specialist review outputs are external evidence events, not manual continuation tasks owned by this build session. When those records change, the canonical chain automatically re-evaluates eligibility and supersession posture.

## Machine-Readable Status

```text
static/status/external-translation-automation-status.json
```

## Authority Boundary

Automation proves that declared records were generated, linked, hashed, and checked together. It does not create source evidence, specialist endorsement, peer review, physical-theory validity, promotion authority, or execution authority.

## Next Goal

The next goal is public publication of the generated reconstruction receipt and automatic endpoint verification through the existing Pages build and public-verification jobs.
