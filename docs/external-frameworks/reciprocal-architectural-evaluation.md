---
title: Reciprocal Architectural Evaluation
sidebar_label: Reciprocal evaluation
---

# Reciprocal Architectural Evaluation

This is the authoritative wiki explanation and framework-by-framework display model for public reciprocal architectural testing. `StegVerse-Labs/Site` may mirror and visualize these records, but the Site projection does not replace this wiki vocabulary or the canonical machine-readable evidence.

## Two valid test models

### Neutral public test

Each participating framework:

1. declares its own scope and boundary;
2. receives the same normalized test package;
3. executes under criteria frozen and published before the run;
4. emits complete machine-readable results;
5. preserves evidence, errors, refusals, uncertainty, receipts, and reconstruction material;
6. permits public inspection and independent replay.

### Reciprocal architectural evaluation

Each evaluator independently determines the claimed boundary, functions, dependencies, exclusions, limitations, and failure conditions of every evaluated framework. Each evaluator then runs the same live test and publishes its determination and results on the evaluated framework's page.

TA-14 may determine StegVerse's boundary. StegVerse may determine TA-14's boundary. Both determinations remain visible beside the framework's own declaration and the live evidence.

No evaluator may overwrite another evaluator's determination. Disagreement remains part of the inspectable record.

## Framework page contract

Every participating framework receives a page containing:

| Record | Required content |
|---|---|
| Framework declaration | The framework's own claimed scope, functions, dependencies, limitations, exclusions, and evidence. |
| StegVerse determination | StegVerse's independent reconstruction of that framework's boundary. |
| TA-14 determination | TA-14's independent reconstruction of that framework's boundary. |
| Additional determinations | Independent maps from other participating evaluators. |
| Shared test package | Stable test-case identifier, frozen criteria, input hash, and expected deliverables. |
| Live execution record | Stable run and event identifiers, output hash, result class, errors, refusals, and timing. |
| Evidence package | Evidence, artifacts, policies, continuity references, signatures, and receipts. |
| Replay and reconstruction | Replay status, reconstruction status, custody reference, and unresolved defects. |
| Disagreement record | Conflicting claims and boundary maps preserved without forced ontology collapse. |
| Confidence and uncertainty | Explicit evaluator confidence, uncertainty, source class, and observation class. |

## Required observation classes

```text
DECLARED
OBSERVED
DERIVED
RECONSTRUCTED
DISPUTED
```

A displayed statement must identify which class produced it. A framework's self-description is not presented as independent validation.

## Result classes

```text
PASS
PARTIAL
FAIL
ERROR
REFUSE
NOT_TESTED
INCONCLUSIVE
DISPUTED
```

No result is inferred when evidence is missing or a machine-readable record cannot be validated.

## Parentage and containment claims

A claim that one architecture is the parent of another is separately testable. The following do not independently establish parentage:

```text
scope overlap
historical priority
broader vocabulary
private execution
successful execution of one test
ability to describe another framework using the evaluator's own ontology
```

A parentage determination must identify the asserted inheritance relation, evidence, counterevidence, confidence, uncertainty, and whether the external framework can be reconstructed without first treating it as subordinate.

## Public display architecture

```text
canonical evaluation JSON / JSONL
-> admissibility-wiki framework page and vocabulary projection
-> StegVerse-Labs/Site interactive mirror
-> Publisher and guardian projections only after destination handoff review
```

The wiki is the primary public explanatory and framework-page display. The Site is the interactive comparison mirror. Neither is custody, execution authority, admissibility authority, certification, or proof authority.

## Stable identifiers

```text
evaluation_id
framework_id
evaluator_id
claim_id
determination_id
test_case_id
run_id
event_id
evidence_id
artifact_id
dispute_id
receipt_id
```

Cross-page correlation must use these stable identifiers, never text matching.

## Authority boundary

```text
comparison != authority
comparison != admissibility
self-declaration != independent validation
evaluator determination != evaluated-framework consent
execution success != architectural completeness
execution failure != universal invalidity
scope overlap != parentage
historical priority != containment
page publication != custody
reconstruction PASS != execution authority
```

The public record may validate that a bounded test occurred and that its artifacts reconstruct. It does not silently grant architectural supremacy, ownership, execution permission, certification, or universal standing.

## Machine-readable resources

The reciprocal evaluation schema is published at:

```text
/static/schemas/reciprocal-framework-evaluation.schema.json
```

The bounded publication status is published at:

```text
/static/status/reciprocal-framework-evaluation-status.json
```

Framework-specific records and live run streams remain `NOT_TESTED` until actual declarations, frozen test packages, and observed executions exist.
