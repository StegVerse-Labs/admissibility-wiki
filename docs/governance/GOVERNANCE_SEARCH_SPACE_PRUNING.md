# Governance as Search-Space Pruning

Status: bounded doctrine note

## Originating observation

AI can compress the proposal-to-evaluation cycle by simulating, ranking, and ruling out proposed builds faster than those builds can be physically constructed and studied for classification. The intent of an individual who later uses the resulting knowledge is a separate governance variable from the capability to explore the design space.

Governance can further reduce recursive modeling where known data attributes have already been ruled out. It therefore acts before, during, and after modeling rather than only as a final approval layer.

## Core distinction

Keep these variables separate:

1. **Exploration capability** — how quickly and broadly candidate states can be proposed and evaluated.
2. **Knowledge/actionability** — what the exploration establishes about candidate states and how actionable that knowledge becomes.
3. **Actor intent** — what a particular actor proposes to do with that knowledge.
4. **Governance/admissibility** — whether the proposed transition is permitted under the applicable actor, authority, purpose, evidence, target, constraints, and time.
5. **Execution** — whether an admitted transition is actually committed or observed.

Capability, knowledge, intent, admissibility, and execution are not interchangeable state variables.

## Search-space reduction

Let `X` be a candidate state or proposal space. Let `R(G,E,C,t)` be the subset ruled out by governance state `G`, evidence `E`, context `C`, and evaluation time `t`.

The active modeling space is:

```text
X_active = X \\ R(G,E,C,t)
```

This is **conditional exclusion**, not deletion of knowledge. A ruled-out branch retains the evidence and governance basis for its exclusion. If governance, evidence, context, or time changes, the branch may become eligible for reevaluation.

A naive recursive loop is:

```text
generate -> simulate -> classify -> reject -> regenerate
```

A governed loop is:

```text
reconstruct applicable governance
-> exclude already-resolved inadmissible regions
-> model admissible or unresolved regions
-> simulate/rank candidates
-> evaluate the proposed transition at the applicable boundary
-> commit only if the transition remains admissible
-> preserve receipt/evidence for continuity and future reconstruction
```

## Consequence

Governance is not merely a downstream safety or compliance check. When prior determinations are reconstructable and applicable, governance becomes a computational mechanism that prevents repeated exploration of already-resolved regions of the state space.

This produces three distinct efficiencies:

```text
AI/modeling compresses empirical exploration.
Governance compresses the active admissible search space.
Continuity prevents repeated rediscovery of already-resolved constraints.
```

The architecture must fail closed when the applicability, validity, freshness, provenance, or authority of a prior exclusion cannot be reconstructed. A historical rejection must not be treated as permanently valid merely because it exists.

## Biological-design example boundary

In biological design, computational systems may evaluate or rank candidate constructs faster than physical candidates can be built and experimentally classified. That capability increase does not by itself establish malicious intent or an inadmissible transition. Governance evaluates the actor and proposed transition separately from the existence of the underlying knowledge or modeling capability.

As simulation quality improves, a consequential governance boundary can occur before physical synthesis: a broad design space can become a small set of highly actionable candidates. The transition from exploratory information to actionable candidate knowledge may therefore require governance even when no physical build has occurred.

This note does not classify biological constructs, provide biological design instructions, or grant authority to synthesize, test, publish, or execute any candidate.

## Required invariants

- `capability != intent`
- `knowledge != authority`
- `simulation != execution`
- `prior rejection != perpetual rejection`
- `governance pruning != deletion`
- `modeling efficiency != admissibility`
- `admission != commitment`
- `missing reconstruction evidence -> fail closed`

## Integration posture

This doctrine is additive to the repository's existing commit-time admissibility, reconstruction, continuity, and authority-boundary work. It does not supersede canonical validation issue #50, the repository-wide handoff, or any active implementation claim.
