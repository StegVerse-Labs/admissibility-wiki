# Cedar Binary Provenance Reconciliation Handoff

## Installed transition

```text
canonical compiled_binary_sha256
+ selected-binary build receipt
+ promotion candidate
+ applied promotion receipt
+ registry application result
-> binary provenance reconciliation
```

Installed:

```text
scripts/reconcile_cedar_registry_binary_provenance.py
scripts/check_cedar_binary_provenance_reconciliation.py
scripts/check_goal5_external_frameworks_all.py
```

## Reconciliation contract

The reconciler requires the same valid lowercase SHA-256 value at all six locations:

```text
canonical selection registry
build receipt binary.sha256
promotion candidate binary_sha256
promotion receipt source binary_sha256
promotion receipt proposed registry value
application result approved registry value
```

It also requires:

```text
build state: BUILT_HASHED_UNEXECUTED
promotion candidate: READY_FOR_REGISTRY_PROMOTION_REVIEW
promotion decision: ALLOW_REGISTRY_PROMOTION_ONLY
promotion state: APPLIED_HASH_ONLY
application state: APPLIED_HASH_ONLY or ALREADY_APPLIED_HASH_ONLY
Cedar execution_authorized: false
runtime execution authorized/requested: false
external consequence allowed: false
```

Successful reconciliation produces only:

```text
reconciliation_state: PROVENANCE_RECONCILED_HASH_ONLY
all_hashes_equal: true
```

Missing, malformed, or unequal evidence produces:

```text
reconciliation_state: PROVENANCE_UNRESOLVED_FAIL_CLOSED
```

## Validator behavior

The structural validator constructs an isolated complete provenance chain, verifies successful reconciliation, introduces a deliberate candidate-hash mismatch, and requires the mismatch to fail closed. It does not modify the canonical registry, build Cedar, dispatch a job, or execute a policy decision.

## Current evidence posture

The canonical registry presently contains a Cedar compiled-binary hash, but the corresponding workflow build receipt, promotion candidate, applied promotion receipt, and application result have not been retrieved and inspected through the available connector. Therefore:

```text
canonical hash present: yes
provenance reconciliation tooling: installed
canonical provenance reconciled: not established
runtime execution authorized: no
compatibility established: no
```

## Boundary

```text
matching binary hashes != compatibility
matching binary hashes != execution authority
registry promotion != standing
provenance reconciliation != dispatch authority
provenance reconciliation != observed execution
```

## Next action

Retrieve the first accessible `cedar-selected-binary-build` artifact and the related governed promotion/application receipts. Run the reconciler against those exact files. Do not mark the canonical Cedar hash as evidenced unless the generated result is `PROVENANCE_RECONCILED_HASH_ONLY` and every artifact hash is retained for reconstruction.
