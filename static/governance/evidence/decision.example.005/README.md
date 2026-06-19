# Evidence Record — decision.example.005

Generated: 2026-06-19

## Purpose

This evidence record explains why `decision.example.005` accepted `Provenance` as overlapping with `Reconstructability` while refusing to treat it as an accepted equivalent term.

## Linked Records

```text
Proposal: ../proposals/proposal.example.005.json
Decision: ../decisions/decision.example.005.json
Replay: ../replay/decision.example.005.txt
Research note: ../../../docs/research/terminology-overlap-research-notes.md
```

## Source Family

```text
External term: Provenance
Source family: W3C PROV
Source type: standards-based primary source
Source URLs:
- https://www.w3.org/TR/prov-overview/
- https://www.w3.org/TR/prov-primer/
```

## Evidence Summary

W3C PROV describes provenance information involving entities, activities, and agents involved in producing data or artifacts.

That overlaps with StegVerse reconstructability because provenance can help reconstruct origin, process, attribution, and history.

However, the StegVerse term `Reconstructability` is narrower in one important respect: it asks whether enough information can be recovered to understand not only what happened, but why a decision appeared to have standing.

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

- it does not treat provenance as equivalent to reconstructability;
- it does not claim W3C endorsement;
- it does not claim all provenance records reconstruct standing;
- it does not replace executable proof authority;
- it only accepts a glossary relationship placement.

## Reconstruction Question

Could a reviewer reconstruct why provenance was accepted as overlapping but not equivalent?

Expected answer: yes. The proposal, decision, replay, evidence record, and research note show the source family, comparison dimensions, mismatches, accepted placement, and non-claims.

## Non-Claims

This evidence record does not prove that all uses of provenance are relevant to admissibility.

This evidence record does not prove that provenance is equivalent to reconstructability.

This evidence record does not replace formalism-tests or executable receipts.
