# Evidence Record — decision.example.008

Generated: 2026-06-19

## Purpose

This evidence record explains why `decision.example.008` accepted `Policy decision` as overlapping with `Commit-Time Authority` while refusing to treat it as an accepted equivalent term.

## Linked Records

```text
Proposal: ../proposals/proposal.example.008.json
Decision: ../decisions/decision.example.008.json
Replay: ../replay/decision.example.008.txt
Research note: ../../../docs/research/terminology-overlap-research-notes.md
```

## Source Family

```text
External term: Policy decision
Source family: Open Policy Agent documentation
Source type: vendor-authored primary project documentation
Source URLs:
- https://www.openpolicyagent.org/docs
```

## Evidence Summary

Open Policy Agent documentation describes policy evaluation using supplied input, policies, and data.

That overlaps with StegVerse `Commit-Time Authority` when a policy decision contributes to authorization at or near the binding moment.

However, the StegVerse term `Commit-Time Authority` is not merely a policy-engine result. It is the authority basis that exists when a transition binds, including the relevant authority class, evidence posture, review posture, continuity posture, and consequence boundary.

## Decision Basis

```text
Decision: ALLOW_AS_OVERLAP
Placement: Overlapping Terms
Equivalent status: not accepted
Evidence posture: present
Commit-time validity: true
```

## Boundary Evidence

The decision remains bounded because:

- it does not treat policy decision as equivalent to Commit-Time Authority;
- it does not claim outside project endorsement;
- it does not claim policy evaluation alone satisfies admissibility;
- it does not replace executable proof authority;
- it only accepts a glossary relationship placement.

## Reconstruction Question

Could a reviewer reconstruct why policy decision was accepted as overlapping but not equivalent?

Expected answer: yes. The proposal, decision, replay, evidence record, and research note show the source family, comparison dimensions, mismatches, accepted placement, and non-claims.

## Non-Claims

This evidence record does not prove that all policy decisions are relevant to admissibility.

This evidence record does not prove that policy decision is equivalent to Commit-Time Authority.

This evidence record does not replace formalism-tests or executable receipts.
