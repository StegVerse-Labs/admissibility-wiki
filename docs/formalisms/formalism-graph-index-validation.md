---
title: Formalism Graph Index Validation
---

# Formalism Graph Index Validation

## Purpose

This page documents the validation contract for the Canonical Formalism Graph Index.

## Validator

```text
scripts/check-formalism-graph-index.mjs
```

## Validated Inputs

```text
static/formalisms/formalism-registry.v0.1.json
docs/formalisms/formalism-graph-index.md
```

## Done Condition

The validator passes only when:

```text
1. The main formalism registry exists.
2. The graph index exists.
3. The graph index includes Purpose, Source Boundary, Current Graph Coverage, and Non-Claims sections.
4. Every mirrored registry record has a matching graph-index link.
5. Every mirrored registry record has its source authority represented in the graph index.
6. The graph index preserves the required non-claims.
```

## Manual Command

```bash
node scripts/check-formalism-graph-index.mjs
```

## Workflow Status

Workflow wiring is pending because direct workflow creation was blocked by connector safety checks during this build pass.

Expected workflow path once wiring is permitted:

```text
github/workflows/validate-formalism-graph-index.yml
```

Displayed path omits the leading period. The actual repository path should begin with a leading period.

## Non-Claims

```text
This validation contract does not define any formalism.
This validation contract does not prove any formalism.
This validation contract does not validate formalism truth.
This validation contract only validates graph-index coverage and boundary language.
```
