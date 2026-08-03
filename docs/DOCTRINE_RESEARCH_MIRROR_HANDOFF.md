# Doctrine Research Mirror Handoff

## Source of truth

This file is the canonical handoff and task source of truth for the Standing Research Companion and Phase 3 StegVerse doctrine mapping in `StegVerse-Labs/admissibility-wiki`.

## Active goal

```text
goal_id: SRC-PHASE3-001
active_goal: Map the completed interdisciplinary research corpus to the StegVerse governance doctrine without treating the doctrine as the conclusion.
originating_session_goal: Complete Phase 1 field reviews, Phase 2 cross-disciplinary synthesis, and Phase 3 evidence-based StegVerse mapping; preserve the Research Companion separately from doctrine.
repository: StegVerse-Labs/admissibility-wiki
branch: main
canonical_owner: admissibility-wiki doctrine research lane
claim_state: CLAIMED_FOR_IMPLEMENTATION
claim_created: 2026-08-02T22:35:00-05:00
claim_release_condition: Claims register, terminology register, formalism declaration, open-questions register, and doctrine revision matrix committed and validated; downstream projection obligations recorded.
```

## Authoritative files

```text
docs/DOCTRINE_RESEARCH_MIRROR_HANDOFF.md
docs/research/standing-research-companion-volume-iii-comparative-terminology.md
docs/research/standing-research-companion-volume-iv-claims-register.md
docs/research/standing-research-companion-volume-v-open-questions.md
docs/research/stegverse-formalism-declaration.md
docs/research/doctrine-revision-matrix.md
```

## Session goal inventory

| ID | Goal | Destination | State | Evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| SRC-P1 | Independent literature reviews for Groups A-H | Research Companion Volume I | MERGED_INTO_CANONICAL_WORKSTREAM | Attached research artifacts; repository installation still pending | Install canonical source index and preserve source-status caveats |
| SRC-P2 | Cross-disciplinary synthesis | Research Companion Volume II | MERGED_INTO_CANONICAL_WORKSTREAM | Attached Volume II artifact | Install canonical Volume II or source pointer and reconcile incomplete Group B/H status |
| SRC-P3 | StegVerse mapping | `docs/research/` | CLAIMED_FOR_IMPLEMENTATION | This handoff | Complete claims, terminology, open questions, formalism, revision matrix |
| SRC-SEPARATION | Keep companion separate from doctrine | `docs/research/` and doctrine references | CLAIMED_FOR_INTEGRATION | This handoff | Add doctrine citations only after Phase 3 completion |
| SRC-PROP | Propagate approved doctrine projection | Site, Publisher, admissibility-wiki, stegguardian-wiki | BLOCKED | No approved revision package yet | Release when revision matrix is validated and approved |

## Current evidence posture

```text
Phase 1: user-marked complete, but supplied Group B and Group H artifacts are scaffolds rather than full reviews.
Phase 2: synthesis artifact exists, but its own completion ledger records coverage of 6 of 8 groups.
Phase 3: claims mapping and formalism declaration were generated in research output but were not previously installed in the repository.
Doctrine rewrite: NOT AUTHORIZED until Phase 3 registers are complete and gaps are explicit.
```

## Canonical classifications

```text
NATURAL_ALIGNMENT
COMPATIBLE_EXTENSION
TERMINOLOGY_CONFLICT
REQUIRES_MODIFICATION
EVIDENCE_INSUFFICIENT
NEW_STEGVERSE_FORMALISM
CONTRADICTED
UNKNOWN
```

## Active claims

| Task ID | Role | Exact surfaces | Collision boundary | Expected evidence |
| --- | --- | --- | --- | --- |
| SRC-PHASE3-001 | implementation | `docs/research/*` listed above | No doctrine-page rewrite; no Site/Publisher/wiki propagation until registers validate | commits and file-content inspection |
| SRC-PHASE3-VAL | validation | same files | distinct from implementation after files exist | deterministic link/structure checker or repository build |

Claims expire when the release condition is met or when no evidence-bearing commit occurs for 14 days. A stale claim must be released or renewed with a commit reference.

## Completed work

```text
2026-08-02: canonical repository identified from Site handoff authority map.
2026-08-02: no applicable doctrine research mirror handoff was found in admissibility-wiki.
2026-08-02: this canonical handoff created.
2026-08-02: Phase 3 claims register and formalism declaration scheduled for immediate installation.
```

## Incomplete work

```text
Install Volume III comparative terminology.
Install Volume IV claims register.
Install Volume V open questions.
Install doctrine revision matrix.
Install or reference canonical Volume I and Volume II source artifacts.
Resolve Group B and Group H scaffold status; do not represent them as completed literature reviews without substantive files.
Add deterministic validation for required headings, classifications, claim IDs, evidence status, and doctrine non-rewrite boundary.
After validation and authority approval, propagate approved projections to StegVerse-Labs/Site, GCAT-BCAT-Engine/Publisher, and StegVerse-002/stegguardian-wiki.
```

## Machine-owned continuation

```text
trigger: changes under docs/research/ or this handoff
inputs: canonical research registers and source index
outputs: validation receipt with COMPLETE, BLOCKED, REVIEW_REQUIRED, FAILED, SUPERSEDED, or MERGED
fail-closed: missing evidence status, source pointer, or classification yields BLOCKED
next executable task: create and validate the claims register and formalism declaration
```

## Validation commands

```bash
python scripts/check_doctrine_research_companion.py
npm test -- --runInBand
npm run build
```

The dedicated checker is not yet installed. Until it exists, file-content inspection is the available validation level.

## Cross-repository dependencies

```text
StegVerse-Labs/Site: public projection only after approved revision package
GCAT-BCAT-Engine/Publisher: publication projection only after approved revision package
StegVerse-002/stegguardian-wiki: guardian projection only after approved revision package
master-records/orchestration: future custody of immutable research/revision receipts if required by live contracts
```

## Authority boundary

```text
research evidence != doctrine truth
cross-disciplinary analogy != equivalence
formal proof != validation of the specification
provenance != correctness
replayability != current admissibility
consensus != truth
signal detectability != health, agency, consent, consciousness, or authority
repository publication != scientific validation
```

## Archive conditions

This session may be archived only when all unique goals are committed here or explicitly merged into durable tasks; the claims/formalism artifacts are installed; remaining Group B/H and validation work has exact repository ownership; and no unique session-only requirement remains.

## Completion metrics

```text
developed_files_percentage: 17
validation_percentage: 5
integration_percentage: 10
goal_activation_percentage: 20
session_consolidation_state: ACTIVE — UNIQUE WORK REMAINS
```
