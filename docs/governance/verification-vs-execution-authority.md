---
title: Verification Is Not Execution Authority
---

# Verification Is Not Execution Authority

## Governance signal

Virginia's 2026 SB 384 / HB 797 directs the Joint Commission on Technology and Science to evaluate a framework for Independent Verification Organizations (IVOs). The supplied public announcement describes independent, expert-led bodies that verify whether AI systems meet outcome-based safety goals.

Source observed:

```text
https://www.prnewswire.com/news-releases/fathom-applauds-governor-spanbergers-signing-of-landmark-ai-governance-legislation-302739994.html
Published: 2026-04-13
Source class: organization-issued public announcement distributed by PR Newswire
```

This source is evidence of a policy direction and of the announced study mandate. It is not, by itself, the enacted bill text, an operational IVO standard, proof of implementation, or evidence that an IVO holds live authority over individual executions.

## The distinction

Independent verification can answer questions such as:

- whether a system was assessed against stated criteria;
- whether documentation and evidence were available to reviewers;
- whether an external expert body found the system consistent with a safety target;
- whether a product earned a verification status or seal.

Those functions matter. They do not answer the narrower commit-time question:

> Who or what was authorized to let this specific consequential decision become real?

Verification evaluates a system, artifact, process, or claim. Execution authority determines whether a particular state transition may be committed now, under a named institution's authority, against current policy, delegation, evidence, scope, and recoverability constraints.

## Required live control point

For a high-risk action, governance remains incomplete unless the workflow preserves a point at which execution can still be denied before consequence attaches.

```text
verified system
  != authorized action

review completed
  != current delegation

impact assessment
  != commit-time admissibility

explainable result
  != permission to execute
```

A governed execution boundary should bind at least:

1. the proposed action and target;
2. the actor or requesting entity;
3. the institution under whose name the action would execute;
4. the current policy reference;
5. the current delegation or authority class;
6. the evidence and review posture;
7. the execution context and validity window;
8. the recoverability or rollback profile;
9. the authority able to return `ALLOW`, `DENY`, or `FAIL_CLOSED`;
10. the receipt proving what was admitted or refused.

## Institutional test

The decisive institutional question is not only whether the model or system was reviewed. It is whether the institution retained authority over what could execute under its name.

A useful public test is:

> Show where the workflow can still say "NO."

If no reachable denial point exists before commitment, the institution may possess documentation, assurance, or after-the-fact accountability without retaining live execution authority.

## Relationship to the StegVerse triad

| Layer | Question | Virginia/IVO relevance |
|---|---|---|
| Transition governance | Can this transition be considered? | Verification may establish evidence and review posture. |
| Admissibility governance | Can this transition be committed now? | Requires current execution authority and a reachable refusal point. |
| Continuity governance | Can the decision path be reconstructed later? | Requires receipts for assessment, authority resolution, execution, or denial. |

The IVO concept can strengthen evidence quality and independent review. It should enter the governed transition path as an evidence and review input, not be silently promoted into execution authority.

## Boundary statement

```text
independent verification != execution authority
certification != standing to commit a specific transition
system approval != action-level admissibility
post-event explanation != pre-consequence refusal
```

The next governance phase is therefore not limited to "show your work." It must also show where the institution can still refuse the work's conversion into consequence.
