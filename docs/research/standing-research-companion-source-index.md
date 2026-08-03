# Standing Research Companion Source Index

## Purpose

This document is the canonical source and replacement-task index for the Standing Research Companion corpus used by `StegVerse-Labs/admissibility-wiki`.

It preserves the supplied source artifacts without treating plans, prompts, summaries, or scaffolds as completed literature reviews. It also defines the exact completion and release conditions for the Group B and Group H replacement lanes.

## Authority boundary

```text
source presence != substantive completion
research plan != literature review
review prompt != literature review
field summary != dissertation-grade chapter
citation presence != source quality
repository commit != scientific validation
cross-disciplinary analogy != equivalence
```

## Supplied source artifacts

| Source ID | Original file name | SHA-256 | Lines | Words | Bytes | Evidence class | Canonical classification | Permitted use | Prohibited representation |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| SRC-B-INPUT-001 | `2-TIME-deep-research-report(3).md` | `6eca9fb26946605cabfb3be0c94f26aaf4443e6785e529ea8ba1d66856f99871` | 272 | 1,990 | 15,384 | Session-supplied research planning artifact | `SCAFFOLD_RESEARCH_PLAN` | Scope definition, sequencing, review template, terminology and validation requirements for Group B | A completed Control Theory, Dynamical Systems, Network Science, Complex Adaptive Systems, or Systems Biology review |
| SRC-H-INPUT-001 | `8-BIO-INT-deep-research-report(3).md` | `8a6459efe124e4769c571c33ac5f21fd5491375ba189cbdea8cd11072b6e5d41` | 71 | 631 | 4,956 | Session-supplied review prompt artifact | `SCAFFOLD_REVIEW_PROMPT` | Scope definition, analytical considerations, evidence-status requirements, validation and ethics requirements for Group H | A completed Neuroscience, Brain-Computer Interfaces, Bioinformatics, or Computational Biology review |

The source bytes are not represented as repository-installed review chapters. Their hashes identify the exact supplied artifacts that informed this task index.

## Group B replacement inventory

Canonical group: **Time and Dynamic Systems**

| Task ID | Field | Required destination | Claim state | Current state | Required evidence-status sections | Release condition |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-P1-B-CT | Control Theory | `docs/research/volume-i/group-b/control-theory.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-B-DS | Dynamical Systems | `docs/research/volume-i/group-b/dynamical-systems.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-B-NS | Network Science | `docs/research/volume-i/group-b/network-science.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-B-CAS | Complex Adaptive Systems | `docs/research/volume-i/group-b/complex-adaptive-systems.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-B-SB | Systems Biology | `docs/research/volume-i/group-b/systems-biology.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |

## Group H replacement inventory

Canonical group: **Biological Interpretation**

| Task ID | Field | Required destination | Claim state | Current state | Required evidence-status sections | Release condition |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-P1-H-NEURO | Neuroscience | `docs/research/volume-i/group-h/neuroscience.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-H-BCI | Brain-Computer Interfaces | `docs/research/volume-i/group-h/brain-computer-interfaces.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-H-BIOINFO | Bioinformatics | `docs/research/volume-i/group-h/bioinformatics.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |
| SRC-P1-H-COMP-BIO | Computational Biology | `docs/research/volume-i/group-h/computational-biology.md` | `UNCLAIMED` | `MISSING_SUBSTANTIVE_REVIEW` | Established knowledge; demonstrated implementations; emerging research; speculative proposals | Chapter committed, source register complete, validator PASS |

## Required chapter structure

Every replacement chapter must independently cover:

1. Accepted definitions and scope boundaries.
2. Historical development and major milestones.
3. Current consensus, including where no consensus exists.
4. Competing theories, models, or schools.
5. Established engineering or scientific practice.
6. Representative systems, tools, workflows, datasets, or technologies.
7. Standards, conventions, metadata requirements, and reproducibility practices.
8. Validation methods and evidence limitations.
9. Major limitations and unresolved problems.
10. Active research and recent advances.
11. Common terminology and overloaded terms.
12. Known misconceptions and recurring methodological errors.
13. Open research questions.
14. Evidence-status summary.
15. Terminology register.
16. Standards and validation register.
17. Limitations register.
18. Open-questions register.
19. Representative primary and synthesis references.

## Source requirements

A replacement chapter is not releasable unless it:

- prioritizes primary literature, formal standards, official scientific or engineering societies, canonical monographs, and major peer-reviewed reviews;
- distinguishes source-derived claims from author inference;
- provides stable source locators sufficient for independent verification;
- avoids relying primarily on encyclopedic or promotional sources;
- identifies publication date and access date when temporally relevant;
- records disagreement rather than silently selecting one position;
- does not map the field to StegVerse or treat StegVerse terminology as the review frame;
- marks claims as `ESTABLISHED`, `DEMONSTRATED`, `EMERGING`, or `SPECULATIVE`;
- identifies standards as mandatory, voluntary, de facto, proposed, or domain-specific;
- states when a field lacks a single authoritative standard or validation regime.

## Validation contract

The repository-native checker must fail closed when any of the following is true:

```text
- a required Group B or Group H chapter is absent;
- a destination contains only a prompt, outline, plan, placeholder, or summary;
- a chapter lacks one or more evidence-status categories;
- a chapter lacks definitions, history, consensus, competing theories, practice, limitations, active research, validation, misconceptions, or open questions;
- cited sources cannot be located from the committed source register;
- the chapter attempts to prove or validate StegVerse doctrine;
- Volume II mapping is marked complete before all nine replacement tasks pass;
- downstream propagation is marked complete without consumer validation receipts.
```

## Volume II dependency

The existing six-group synthesis remains `PARTIAL`.

The following task is blocked until all nine Group B/H tasks are `COMPLETE` and repository validation passes:

```text
task_id: SRC-P2-RERUN-BH
owner: StegVerse-Labs/admissibility-wiki doctrine research lane
state: BLOCKED
surface: docs/research/standing-research-companion-volume-ii-cross-disciplinary-mapping.md
release_condition: all SRC-P1-B-* and SRC-P1-H-* tasks COMPLETE with validator PASS
required_action_after_release: rerun the fixed comparison matrix and replace reserved or limitation-only Group B/H seams with source-supported mappings
```

## Propagation dependency

No Group B/H claim or mapping may propagate to Site, Publisher, or guardian documentation until:

1. all nine review tasks pass;
2. the Volume II rerun passes;
3. Phase 3 revision rows receive explicit disposition;
4. repository-specific consumer contracts exist;
5. propagation receipts are committed and validated.

## Session consolidation record

```text
originating_session_goal: complete independent field reviews without using the fields to prove doctrine
transferred_requirements: Group B and Group H field lists, mandatory review dimensions, four-level evidence ladder, scholarly neutrality requirement, dissertation-grade depth requirement, validation and standards requirements, and mapping deferral requirement
canonical_continuation: StegVerse-Labs/admissibility-wiki/main/docs/DOCTRINE_RESEARCH_MIRROR_HANDOFF.md
canonical_task_index: StegVerse-Labs/admissibility-wiki/main/docs/research/standing-research-companion-source-index.md
chat-only requirements remaining after this commit: none
```
