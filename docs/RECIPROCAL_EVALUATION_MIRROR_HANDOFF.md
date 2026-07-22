# Reciprocal Evaluation Mirror Handoff

## Source of truth

This file is the current continuation source for reciprocal architectural evaluation work in `StegVerse-Labs/admissibility-wiki`.

The repository-wide authority remains `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`. This file narrows that authority to the reciprocal evaluation workstream.

## Display ownership

```text
Primary public explanatory and framework-page display: StegVerse-Labs/admissibility-wiki
Interactive comparison mirror: StegVerse-Labs/Site
Publication projection: GCAT-BCAT-Engine/Publisher, only after destination handoff review
Guardian projection: StegVerse-002/stegguardian-wiki, only after destination handoff review
Canonical custody and reconstruction: external to the display layers
```

The wiki is the primary display for framework declarations, evaluator determinations, live results, evidence posture, disputes, confidence, uncertainty, replay, and reconstruction status. The Site may provide synchronized interactive views of the same records but must not become a separate source of truth.

## Current goal

```text
Goal id: reciprocal-architectural-evaluation
Goal: publish machine-testable framework pages for StegVerse, TA-14, and additional participating frameworks, then execute neutral and reciprocal public tests without inherited hierarchy.
State: DOCTRINE_AND_SCHEMA_INSTALLED_LIVE_TEST_PENDING
Manual user action required: false
Authority granted: none
```

## Installed files

```text
docs/external-frameworks/reciprocal-architectural-evaluation.md
static/schemas/reciprocal-framework-evaluation.schema.json
static/status/reciprocal-framework-evaluation-status.json
docs/RECIPROCAL_EVALUATION_MIRROR_HANDOFF.md
```

Site-side precursor files already exist:

```text
StegVerse-Labs/Site/framework-evaluations.html
StegVerse-Labs/Site/docs/RECIPROCAL_ARCHITECTURAL_EVALUATION.md
StegVerse-Labs/Site/data/schemas/framework-evaluation.schema.json
StegVerse-Labs/Site/data/framework-evaluations/index.json
```

## Required framework deliverables

Every participating framework requires:

```text
self-declaration
StegVerse determination
TA-14 determination
additional evaluator determinations
frozen shared test case
live execution JSONL
artifact and evidence references
receipts and signatures
replay result
reconstruction result
dispute records
confidence and uncertainty
content hashes and publication timestamp
```

## Required next files

Destination `StegVerse-Labs/admissibility-wiki`:

```text
static/data/framework-evaluations/index.json
static/data/framework-evaluations/stegverse.json
static/data/framework-evaluations/ta-14.json
static/data/framework-evaluations/test-cases/<test_case_id>.json
static/data/framework-evaluations/runs/<run_id>.jsonl
scripts/check_reciprocal_framework_evaluations.py
scripts/check_reciprocal_boundary_symmetry.py
scripts/check_reciprocal_evaluation_replay.py
```

Navigation and canonical validation integration must follow the existing single-workflow rule in `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`. Do not create another active workflow.

## Test sequence

```text
publish criteria
-> freeze framework self-declarations
-> hash shared test package
-> issue stable test_case_id
-> each evaluator maps each framework
-> each system executes the same input
-> capture canonical event streams
-> validate schemas and references
-> publish all determinations on each framework page
-> replay and reconstruct
-> preserve disagreements
-> emit bounded non-authoritative receipts
-> mirror validated records to Site
```

## Authority boundaries

```text
comparison != authority
comparison != admissibility
self-declaration != independent validation
scope overlap != parentage
historical priority != containment
execution success != architectural completeness
private execution != public verification
page publication != custody
reconstruction PASS != execution authority
```

No framework is assigned parent status by the schema, display order, evaluator identity, or test environment.

## Remaining destinations

```text
StegVerse-Labs/admissibility-wiki — framework records, validators, navigation, canonical workflow integration
StegVerse-Labs/Site — synchronized interactive mirror after wiki records validate
GCAT-BCAT-Engine/Publisher — publication projection after handoff review
StegVerse-002/stegguardian-wiki — guardian interpretation after handoff review
master-records/orchestration — custody and reconstruction integration when authorized
```

## Archive posture

This handoff, the repository-wide handoff, the wiki doctrine, schema, status artifact, and Site precursor files preserve all current continuation information. The complete thread is ready for archiving without any additional part of the thread needed to move forward.
