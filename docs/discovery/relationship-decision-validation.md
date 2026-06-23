---
title: Relationship Decision Validation
---

# Relationship Decision Validation

## Purpose

This page defines the validation contract for reviewed relationship decisions.

## Validated Store

```text
static/discovery/relationship-decisions.json
```

## Expected Validator

```text
scripts/discovery/check-relationship-decisions.mjs
```

## Required Checks

The validator should fail unless:

```text
1. The decision store exists.
2. The schema is admissibility_wiki_relationship_decisions.v0.1.
3. authority_boundary is present.
4. required_record_fields is present and non-empty.
5. allowed_decisions is present and non-empty.
6. allowed_relationship_types is present and non-empty.
7. records is an array.
8. non_claims is present and non-empty.
9. Every record contains every required field.
10. Every decision is in allowed_decisions.
11. Every relationship_type is in allowed_relationship_types.
12. Every decision preserves source_origin_a and source_origin_b.
13. Every decision preserves evidence_a and evidence_b.
14. Every decision contains a decision_basis.
```

## Required Non-Claims

```text
A decision record does not define either term.
A decision record does not replace either source origin.
A decision record must preserve both source origins.
No candidate is promoted without a recorded decision.
```

## Current Wiring Status

The script write for this validator was blocked during this build pass. This contract preserves the intended validation behavior until direct script creation is permitted.

## Non-Claims

```text
This validation contract does not accept any relationship.
This validation contract does not reject any relationship.
This validation contract does not define either term.
This validation contract only describes how relationship decisions should be checked.
```
