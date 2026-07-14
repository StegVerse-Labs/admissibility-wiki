# External Translation Reconstruction Publication Status

## Goal

```text
Goal: Publish and verify the generated external-translation reconstruction receipt without manual steps.
Repository: StegVerse-Labs/admissibility-wiki
State: checkpoint_reached
Automation posture: AUTOMATED_FAIL_CLOSED
```

## Build-Time Publication

The Docusaurus build now loads:

```text
plugins/external-translation-reconstruction-plugin.js
```

During every site build, the plugin:

1. runs `scripts/generate_external_translation_reconstruction_receipt.py`;
2. requires a `PASS` reconstruction result;
3. copies the generated receipt into the built Pages artifact at:

```text
/status/external-translation-reconstruction-receipt.json
```

No checked-in generated receipt needs to be updated manually.

## Public Endpoint

```text
https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json
```

## Automatic Post-Deployment Verification

The existing canonical `verify-public-pages` job runs:

```text
python scripts/check_governed_llm_deployment_status.py
```

That verifier now includes the reconstruction endpoint in its remote route set. A missing or unreachable endpoint causes `FAIL_CLOSED` and a non-zero result.

The public activation receipt also binds the endpoint under:

```text
external_translation_reconstruction_receipt_reachable
```

and links it as:

```text
linked_receipts.external_translation_reconstruction
```

## End-to-End Automated Path

```text
record mutation or scheduled run
-> canonical workflow
-> full validation chain
-> reconstruction receipt generation
-> cross-record validation
-> Docusaurus build plugin regeneration
-> Pages artifact publication
-> GitHub Pages deployment
-> remote endpoint verification
-> public activation receipt
```

## Manual Tasks

```text
manual_tasks_required: none
```

External evidence acquisition and specialist review remain independently owned evidence events. Their absence is automatically represented as `DEFER_NO_SUPERSESSION`; no person must manually preserve or recompute that posture.

## Authority Boundary

Publication and endpoint verification prove only that the generated reconstruction artifact was built and publicly reachable for the observed workflow run. They do not validate physics, create peer review, establish formal equivalence, promote a source record, or grant execution authority.

## Next Goal

The next goal is canonical workflow observation: confirm that a workflow run executes the new chain and produces a passing full-validation artifact plus a reachable reconstruction endpoint. That observation is workflow-owned and requires no manual repository mutation.
