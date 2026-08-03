# Admissible Structural Invariants — Literature Matrix

Status: research comparison artifact; novelty not determined.

This matrix distinguishes exact precedent from partial analogue. It does not claim that any cited field already supplies the complete StegVerse construct.

| Field | Established object | What it contributes | Missing relative to this research object | Classification |
| --- | --- | --- | --- | --- |
| Formal verification | Safety and inductive invariants | Demonstrates preservation across reachable states | Does not by itself determine whether continued preservation remains authorized or purpose-consistent | PARTIAL_ANALOGUE |
| Refinement and simulation | Trace preservation, refinement relations, bisimulation | Supports behavioral continuity across implementations | Usually treats the preserved relation as the correctness target rather than a governed candidate subject to commit-time review | PARTIAL_ANALOGUE |
| Dynamical systems | Invariant sets, manifolds, attractors | Describes persistence under system dynamics | Does not reconstruct policy, delegation, affected-entity standing, or execution authority | PARTIAL_ANALOGUE |
| Category theory | Structure-preserving morphisms and naturality | Supplies languages for identity-preserving mappings and composition | Structure preservation alone does not establish governance admissibility | PARTIAL_ANALOGUE |
| Runtime assurance | Safety envelopes, monitors, fallback controllers | Shows that operational permission may depend on runtime context | Usually evaluates actions or trajectories, not whether preservation of the invariant itself has become obsolete or purpose-inverting | CLOSE_PARTIAL_ANALOGUE |
| Policy and authorization systems | Context-sensitive authorization decisions | Establishes that permission may change while an object remains unchanged | Usually lacks continuity-thread identity, invariant succession, and independent reconstruction requirements | CLOSE_PARTIAL_ANALOGUE |
| Constitutional and legal change | Entrenchment, amendment, continued validity | Shows that preserved rules may lose validity or be lawfully superseded | Legal validity is domain-specific and does not provide the complete computational decision record | CLOSE_PARTIAL_ANALOGUE |
| Distributed systems | State-machine safety, quorum authority, epoch changes | Separates state consistency from current authority epochs | Does not generally model purpose inversion, relational admissibility, or governed invariant replacement as one formal object | CLOSE_PARTIAL_ANALOGUE |
| Provenance and audit | Evidence chains and reconstructability | Supports later reconstruction of why a state or decision occurred | Reconstruction does not itself establish commit-time admissibility | PARTIAL_ANALOGUE |
| Multi-agent governance | Joint constraints, bargaining, social choice, deontic conflicts | Supports conflicting entity-relative constraints and aggregation | Often lacks receipt-bound continuity and explicit invariant succession semantics | CLOSE_PARTIAL_ANALOGUE |

## Candidate gap

The candidate contribution is the explicit separation of:

1. invariant preservation;
2. admissibility of preserving that invariant at commit time;
3. authority and purpose under which preservation is evaluated;
4. affected-entity dispositions and aggregation;
5. receipt-bound invariant succession; and
6. later independent reconstructability.

No exact precedent is asserted here. The machine-readable companion must retain `novelty_status: NOT_DETERMINED` until primary sources are reviewed and independently assessed.

## Research discipline

Each future source record must include a stable citation, source type, exact proposition supported, overlap classification, important limitation, and whether it changes the novelty posture. Similar vocabulary alone is not evidence of conceptual equivalence.
