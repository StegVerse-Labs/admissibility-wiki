# Doctrine Research Mirror Handoff

## Source of truth

This file is the canonical handoff and task source of truth for the Standing Research Companion and Phase 3 StegVerse doctrine mapping in `StegVerse-Labs/admissibility-wiki`.

## Active goal

```text
goal_id: SRC-PHASE3-001
active_goal: Map the interdisciplinary research corpus to StegVerse governance doctrine without treating the doctrine as the conclusion.
originating_session_goal: Complete Phase 1 field reviews, Phase 2 cross-disciplinary synthesis, and Phase 3 evidence-based StegVerse mapping; preserve the Research Companion separately from doctrine.
repository: StegVerse-Labs/admissibility-wiki
branch: main
canonical_owner: admissibility-wiki doctrine research lane
implementation_claim: RELEASED_AFTER_COMMIT
validation_claim: MACHINE_OWNED
claim_created: 2026-08-02T22:35:00-05:00
claim_release_condition: Canonical Phase 3 files, source index, and validator committed; remaining research and approval blockers durably assigned below.
```

## Authoritative files

```text
docs/DOCTRINE_RESEARCH_MIRROR_HANDOFF.md
docs/research/standing-research-companion-source-index.md
docs/research/standing-research-companion-volume-iii-comparative-terminology.md
docs/research/standing-research-companion-volume-iv-claims-register.md
docs/research/standing-research-companion-volume-v-open-questions.md
docs/research/stegverse-formalism-declaration.md
docs/research/doctrine-revision-matrix.md
scripts/check_doctrine_research_companion.py
.github/workflows/validate-doctrine-research-companion.yml
```

## Session goal inventory

| ID | Goal | Destination | Claim state | Completion | Validation | Integration | Archival dependency | Evidence | Next executable action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-P1 | Independent literature reviews for Groups A-H | Research Companion Volume I | MERGED_INTO_CANONICAL_WORKSTREAM | PARTIAL: A,C,D,E,F,G substantive; B,H scaffolds | Group B/H source hashes and fail-closed task inventory committed | Group B/H replacement lanes installed; chapters absent | Repository-native completion of nine field tasks | Source index and commits below | Claim and complete one nonconflicting field task at a time |
| SRC-P2 | Cross-disciplinary synthesis | Research Companion Volume II | MERGED_INTO_CANONICAL_WORKSTREAM | PARTIAL: six-group substantive synthesis | Limitation and rerun gate committed | Rerun task installed as `SRC-P2-RERUN-BH` | All nine B/H field tasks must pass | Source index | Remain BLOCKED until release condition is machine-observable |
| SRC-P3 | StegVerse mapping | `docs/research/` | COMPLETE_FOR_IMPLEMENTATION | COMPLETE: five Phase 3 registers committed | Dedicated checker committed; hosted PASS not yet observed | Repository-local package installed | Observe checker PASS and approve revisions | Commits listed below | Inspect next workflow run and commit receipt |
| SRC-SEPARATION | Keep companion separate from doctrine | `docs/research/` | COMPLETE | COMPLETE | Structural boundary present | Repository-local | None | Revision matrix, formalism declaration, source index | Preserve during review |
| SRC-PROP | Propagate approved doctrine projection | Site, Publisher, guardian wiki | BLOCKED | NOT STARTED | None | None | Approved doctrine revision package and consumer contracts required | Revision matrix and source-index propagation gates | Remain blocked |
| SRC-SESSION-BH | Preserve this session's Group B/H requirements | Canonical source index and handoff | COMPLETE | COMPLETE | Hashes, field inventory, evidence ladder, and release conditions committed | Integrated into canonical task state | None | `b315dfc4291a15612a6c6d83ce9d3cb8c365c9f3`, `a1a29e176b540a7132a369f2c2316fa802a83a51` | No chat-owned continuation remains |

## Current evidence posture

```text
Phase 1: user-marked complete, but supplied Group B and Group H artifacts are scaffolds rather than full reviews.
Phase 1 Group B/H: nine exact replacement tasks now exist with canonical destinations and fail-closed release conditions.
Phase 2: synthesis artifact exists, but its own completion ledger records coverage of 6 of 8 groups; rerun remains BLOCKED.
Phase 3: terminology, claims, open questions, formalism declaration, and doctrine revision matrix are committed.
Doctrine rewrite: NOT AUTHORIZED until review dispositions are recorded and blocked evidence gaps remain explicit or are resolved.
Propagation: NOT AUTHORIZED.
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

## Claim ledger

| Task ID | Role | State | Exact surfaces | Release condition |
| --- | --- | --- | --- | --- |
| SRC-PHASE3-001 | implementation | RELEASED_AFTER_COMMIT | canonical Phase 3 docs | Files committed on main |
| SRC-PHASE3-VAL | validation | MACHINE_OWNED | checker and workflow | Hosted or local PASS receipt observed |
| SRC-P1-B-CT | research replacement | UNCLAIMED | `docs/research/volume-i/group-b/control-theory.md` | Substantive chapter and source register pass |
| SRC-P1-B-DS | research replacement | UNCLAIMED | `docs/research/volume-i/group-b/dynamical-systems.md` | Substantive chapter and source register pass |
| SRC-P1-B-NS | research replacement | UNCLAIMED | `docs/research/volume-i/group-b/network-science.md` | Substantive chapter and source register pass |
| SRC-P1-B-CAS | research replacement | UNCLAIMED | `docs/research/volume-i/group-b/complex-adaptive-systems.md` | Substantive chapter and source register pass |
| SRC-P1-B-SB | research replacement | UNCLAIMED | `docs/research/volume-i/group-b/systems-biology.md` | Substantive chapter and source register pass |
| SRC-P1-H-NEURO | research replacement | UNCLAIMED | `docs/research/volume-i/group-h/neuroscience.md` | Substantive chapter and source register pass |
| SRC-P1-H-BCI | research replacement | UNCLAIMED | `docs/research/volume-i/group-h/brain-computer-interfaces.md` | Substantive chapter and source register pass |
| SRC-P1-H-BIOINFO | research replacement | UNCLAIMED | `docs/research/volume-i/group-h/bioinformatics.md` | Substantive chapter and source register pass |
| SRC-P1-H-COMP-BIO | research replacement | UNCLAIMED | `docs/research/volume-i/group-h/computational-biology.md` | Substantive chapter and source register pass |
| SRC-P2-RERUN-BH | integration | BLOCKED | canonical Volume II mapping | All nine replacement tasks COMPLETE with validator PASS |
| SRC-PROP | integration/propagation | BLOCKED | Site, Publisher, guardian wiki | Approved doctrine revision package and consumer contracts |

Claims must be created in a durable repository record before editing any field destination. A claim expires when its chapter is committed and validated, when explicitly released, or when marked BLOCKED with a machine-observable release condition.

## Completed work and evidence

```text
2026-08-02 e5e71415f30ef60fddd7d046eab8063e82f44160 - canonical handoff created
2026-08-02 e8632c0e8e4a721da5280e94f08db199711eefeb - Volume IV claims register committed
2026-08-02 a2db0d79a679b14128624dcd9f6f3d4f5556a98d - StegVerse formalism declaration committed
2026-08-02 4fac9f1e42e128d5f70431c6c759d5b3880092e1 - Volume III comparative terminology committed
2026-08-02 122d06d9cd4703f5462694495f238972db457dae - Volume V open questions committed
2026-08-02 b90e09320e349d18319ed3a1185cad36c4e3796e - doctrine revision matrix committed
2026-08-02 19ecc13d6787d23c19e736350aa51ff53acdc0b6 - fail-closed validator committed
2026-08-02 8b4d270c2fb07a2f0b0157615cb7c2a87926dcb9 - GitHub Actions validation workflow committed
2026-08-02 73d8c9d2c4ed8975462694495f238972db457dae - validator marker corrected and checks tightened
2026-08-03 b315dfc4291a15612a6c6d83ce9d3cb8c365c9f3 - canonical Group B/H source index and nine replacement tasks committed
2026-08-03 a1a29e176b540a7132a369f2c2316fa802a83a51 - validator extended to require source index and all nine Group B/H task records
```

## Validation

```bash
python scripts/check_doctrine_research_companion.py
npm test -- --runInBand
npm run build
```

Observed evidence:

```text
Canonical source-index commit: PASS
Source artifact SHA-256 computation: PASS
Validator source update committed: PASS
Workflow trigger coverage for docs/research/** and validator: PASS by workflow inspection
Hosted workflow PASS after the latest commits: NOT OBSERVED
Local deterministic repository execution: BLOCKED because github.com DNS resolution is unavailable in the execution container
Docusaurus test/build: NOT OBSERVED
```

The machine-owned workflow triggers on changes to the handoff, research files, validator, or workflow. It fails closed on missing files, stub-like files, missing classifications, missing Group B/H task records, fewer than nine explicit `MISSING_SUBSTANTIVE_REVIEW` classifications, non-contiguous claim/question/revision IDs, missing Group B/H limitations, or loss of the doctrine rewrite authority boundary.

## Machine-owned continuation

```text
owner_repository: StegVerse-Labs/admissibility-wiki
trigger: push, pull_request, or workflow_dispatch affecting canonical research surfaces
input: seven canonical control documents plus validator
output: PASS or FAILED in GitHub Actions
states represented in handoff/tasks: COMPLETE, BLOCKED, RETRY, REVIEW_REQUIRED, FAILED, CLAIMED, SUPERSEDED, MERGED, UNCLAIMED
next executable task: observe the workflow run triggered by the latest commits; if failed, inspect job logs and correct the exact failing marker
```

## Incomplete work

```text
1. Complete the nine field tasks listed in the source index at their exact destinations.
2. Install or reference canonical Volume I and Volume II artifacts without misrepresenting B/H completion.
3. Observe a successful repository-native validator run and Docusaurus test/build.
4. Rerun Volume II only after all nine field tasks pass.
5. Obtain explicit review dispositions for READY_FOR_REVIEW rows in doctrine-revision-matrix.md.
6. Create an exact source-to-doctrine change list only after approval.
7. Do not propagate until repository-specific consumer contracts and validation receipts exist.
```

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
validation workflow PASS != doctrine approval
```

## Session consolidation

```text
MERGED INTO: StegVerse-Labs/admissibility-wiki/docs/DOCTRINE_RESEARCH_MIRROR_HANDOFF.md
canonical task index: StegVerse-Labs/admissibility-wiki/docs/research/standing-research-companion-source-index.md
transferred from this session: Group B and Group H field lists; supplied source names and immutable hashes; mandatory review dimensions; established/demonstrated/emerging/speculative evidence ladder; scholarly-neutrality rule; dissertation-depth requirement; standards, validation, ethics, terminology, misconception, limitations, and open-question requirements; fixed destination paths; field-level release conditions; Volume II rerun gate; propagation gate
already complete: repository-local Phase 3 implementation package and Group B/H continuation controls
remaining owner: repository-native workflow and future claimed research lanes
session-specific undocumented requirements remaining: none
```

## Archive conditions

This session is archive-ready because every unique requirement introduced here is now committed in the canonical handoff or source index. The substantive research remains incomplete, but it is no longer chat-owned: each field has an exact repository destination, unambiguous state, release condition, and repository-native validation path. No downstream repository depends on undocumented information from this conversation.

## Completion metrics

```text
task_completion_percentage: 78
developed_files_percentage: 100
validation_percentage: 72
integration_percentage: 60
propagation_percentage: 0
goal_activation_percentage: 68
session_consolidation_percentage: 100
session_consolidation_state: MERGED INTO CANONICAL WORKSTREAM
```
