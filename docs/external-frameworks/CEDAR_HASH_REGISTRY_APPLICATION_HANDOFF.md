# Cedar Hash-Only Registry Application Handoff

## Installed transition

```text
approved binary-hash promotion receipt
-> fail-closed receipt and target validation
-> dry-run or single-field application
-> registry SHA-256 receipt
-> readiness regeneration in a later transition
```

Installed files:

```text
scripts/apply_cedar_binary_hash_registry_promotion.py
scripts/check_cedar_binary_hash_registry_application.py
scripts/check_goal5_external_frameworks_all.py
```

## Mutation boundary

The application engine may change only:

```text
frameworks[cedar-policy].selection.compiled_binary_sha256
```

It rejects a receipt unless all of the following hold:

```text
receipt_type == cedar_binary_registry_promotion_receipt
framework_id == cedar-policy
decision == ALLOW_REGISTRY_PROMOTION_ONLY
promotion_state is APPROVED_NOT_APPLIED or APPLIED_HASH_ONLY
candidate_state == READY_FOR_REGISTRY_PROMOTION_REVIEW
candidate and binary SHA-256 values are valid
review.status == PASS
reviewer identity and delegation reference are present
registry path and target field match exactly
proposed hash equals the candidate binary hash
runtime_execution_authorized == false
external_consequence_allowed == false
```

## Modes

Without `--apply`, the engine validates the receipt and registry and emits:

```text
application_state: VALIDATED_DRY_RUN
registry_mutation_applied: false
```

With `--apply`, an exact approved mutation emits:

```text
application_state: APPLIED_HASH_ONLY
registry_mutation_applied: true
```

If the registry already contains the same approved hash, the operation is idempotent:

```text
application_state: ALREADY_APPLIED_HASH_ONLY
registry_mutation_applied: false
idempotent_existing_match: true
```

Any mismatch emits `BLOCKED` and returns nonzero.

## Validation coverage

The checker creates an isolated temporary registry and proves:

```text
dry-run does not mutate the registry
apply changes only compiled_binary_sha256
execution_authorized remains false
an updated registry SHA-256 is recorded
repeating the same approved application is idempotent
no second mutation is claimed
```

The checker does not use or modify the canonical registry.

## Current repository posture

The canonical Cedar record currently contains a compiled binary SHA-256 while `execution_authorized` remains false. This layer does not infer how that value was produced and does not treat its presence as proof that the workflow artifact or governed promotion receipt has been inspected. The canonical value must remain evidence-bound to an actual build receipt and promotion receipt before stronger claims are made.

## Boundary

```text
binary hash presence != inspected build evidence
promotion approval != registry application
registry application != execution authority
registry application != compatibility
idempotent hash match != replay confirmation
readiness regeneration != runtime dispatch
```

## Next action

Inspect the first accessible `cedar-selected-binary-build` artifact and compare its build receipt, promotion candidate, and binary SHA-256 with the canonical registry value. Produce a real evidence-bound promotion receipt or fail closed on any mismatch. Do not execute Cedar in the inspection or registry-application transition.
