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
Goal: publish machine-testable framework pages for StegVerse, TA-14, ASRO, and additional participating frameworks, then execute neutral and reciprocal public tests without inherited hierarchy.
State: ASRO_FRAMEWORK_RECORD_AND_EXPECTED_RESULTS_INSTALLED_TEST_CASE_FREEZE_NEXT
Manual user action required: false
Authority granted: none
```

## Installed files

```text
docs/external-frameworks/reciprocal-architectural-evaluation.md
docs/external-frameworks/asro.md
static/schemas/reciprocal-framework-evaluation.schema.json
static/status/reciprocal-framework-evaluation-status.json
static/data/framework-evaluations/index.json
static/data/framework-evaluations/asro.json
static/data/framework-evaluations/asro/stegverse-companion-layer-declaration.json
static/data/framework-evaluations/asro/asro-author-provided-bounded-representative-object.json
static/data/framework-evaluations/asro/reviewer-profile.json
static/data/framework-evaluations/asro/correspondence-manifest.json
static/data/framework-evaluations/asro/expected-results.json
scripts/check_asro_bounded_comparison.py
docs/RECIPROCAL_EVALUATION_MIRROR_HANDOFF.md
```

The ASRO framework record, registry entry, expected-results fixture, public page, and validation guard are installed. The validator is integrated through `scripts/check_admissibility_automation_handoff.py` and therefore the canonical `npm run validate` path.

Site-side precursor files already exist:

```text
StegVerse-Labs/Site/framework-evaluations.html
StegVerse-Labs/Site/docs/RECIPROCAL_ARCHITECTURAL_EVALUATION.md
StegVerse-Labs/Site/data/schemas/framework-evaluation.schema.json
StegVerse-Labs/Site/data/framework-evaluations/index.json
```

## ASRO bounded comparison contract

```text
ASRO object classification: ASRO-author-provided bounded representative object
ASRO object canonical status: non-canonical
Released ASRO-native schema status: false
StegVerse Companion Layer declaration: controlling source declaration
Reviewer-side profile: derivative
Reviewer issuer: unresolved until an accountable reviewer is designated
Reference test: object identity + version + hash + applicable time + explicit collection membership
Label equality alone: insufficient
Correspondence result: no truth, sufficiency, validity, admissibility, authority, execution, or custody inheritance
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
static/data/framework-evaluations/test-cases/asro-declared-reference-membership-v1.json
static/data/framework-evaluations/runs/asro-declared-reference-membership-v1-stegverse-run-001.jsonl
scripts/check_reciprocal_framework_evaluations.py
scripts/check_reciprocal_boundary_symmetry.py
scripts/check_reciprocal_evaluation_replay.py
```

Next implementation objective:

```text
freeze the bounded test package
-> issue stable test_case_id
-> bind all input artifact hashes
-> define pass, fail-closed, and unresolved outcomes
-> emit first deterministic JSONL event stream
-> validate replay and independent reconstruction
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
correspondence != truth
correspondence != sufficiency
correspondence != validity
correspondence != authority inheritance
reviewer role != accountable issuer
```

No framework is assigned parent status by the schema, display order, evaluator identity, or test environment.

## Remaining destinations

```text
StegVerse-Labs/admissibility-wiki — frozen ASRO test case, first JSONL run, reciprocal validators, replay and reconstruction evidence
StegVerse-Labs/Site — synchronized interactive mirror after wiki records validate
GCAT-BCAT-Engine/Publisher — publication projection after handoff review
StegVerse-002/stegguardian-wiki — guardian interpretation after handoff review
master-records/orchestration — custody and reconstruction integration when authorized
```

## Archive posture

This handoff, the repository-wide handoff, the wiki doctrine, schema, status artifact, ASRO framework record, registry entry, expected-results fixture, public page, bounded comparison packet, validator integration, and Site precursor files preserve all current continuation information. The complete thread is ready for archiving without any additional part of the thread needed to move forward.
