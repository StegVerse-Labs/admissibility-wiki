---
title: Generated Page Surfaces Handoff
---

# Generated Page Surfaces Handoff

This file is the source-of-truth addendum for generated external-framework page sections.

## Source Of Truth

Machine-readable inventory:

```text
docs/external-frameworks/generated-page-surfaces.json
```

Validator:

```text
scripts/check_external_framework_page_surfaces.py
```

## Active Generated Surfaces

```text
metadata
mapping
page_status
analysis_boundary
closeout_state
workflow_entrypoint_migration
entrypoint_closeout_propagation
release_evidence_bundle
```

## Inactive Generated Surfaces

```text
terms
```

`terms` is installed but not active because `mapping` is the current generated manifest term surface.

## No-Manual Task Rule

Generated page surfaces must be discovered from the machine-readable inventory, not reconstructed from chat history.

No generated surface listed as active requires a manual wiring task.

## Boundary

Generated page surfaces are descriptive compatibility evidence only. They do not create certification, endorsement, formalism adoption, admissibility proof, or execution authority.
