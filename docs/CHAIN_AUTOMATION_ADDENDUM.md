# Chain Automation Addendum

## Assumption

This addendum supplements `docs/CHAIN_STATUS_HANDOFF.md` and records that the chain continuation validation route is now automated.

## Canonical Workflow

Canonical path displayed without the leading dot:

```text
github/workflows/validate-chain-continuation.yml
```

Actual repository path includes the leading dot.

## iOS-Safe Mirror

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

## Workflow Manifest

```text
workflow_manifest.json
```

The workflow manifest now records:

```text
canonical_workflow_installed: true
manual_workflow_install_required: false
```

## Automated Checks

```bash
python scripts/check_chain_status_continuation.py
python scripts/check_chain_snapshot_receipt.py
```

Expected:

```text
CHAIN CONTINUATION: PASS
CHAIN SNAPSHOT RECEIPT: PASS
```

## Boundary

This automation validates the blocked continuation package. It does not create the missing Guardian destination repository and does not claim activation, closure, endorsement, adoption, or consequence-binding standing.

## Remaining Blocked Condition

```text
Create or identify the Guardian standing-boundary repository before continuing Guardian-side propagation.
```
