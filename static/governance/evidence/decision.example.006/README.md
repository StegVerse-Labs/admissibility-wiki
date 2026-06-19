# Evidence Record — decision.example.006

Generated: 2026-06-19

## Purpose

This evidence record explains why `decision.example.006` accepted `policy-as-code` as overlapping with `Policy Reference` while refusing to treat it as an accepted equivalent term.

## Linked Records

```text
Proposal: ../proposals/proposal.example.006.json
Decision: ../decisions/decision.example.006.json
Replay: ../replay/decision.example.006.txt
Research note: ../../../docs/research/terminology-overlap-research-notes.md
```

## Source Family

```text
External term: policy-as-code
Source family: Open Policy Agent documentation
Source type: vendor-authored primary project documentation
Source URLs:
- https://www.openpolicyagent.org/docs
```

## Evidence Summary

Open Policy Agent documentation describes policy evaluation using structured input, policies, and data.

That overlaps with StegVerse `Policy Reference` because a policy-as-code artifact may supply the rule basis for a transition.

However, the StegVerse term `Policy Reference` is not the policy implementation itself. It is the specific rule, policy, standard, governance artifact, version, or formalism artifact cited as the governing basis for a proposed transition.

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

- it does not treat policy-as-code as equivalent to Policy Reference;
- it does not claim Open Policy Agent endorsement;
- it does not claim policy evaluation alone satisfies admissibility;
- it does not replace executable proof authority;
- it only accepts a glossary relationship placement.

## Reconstruction Question

Could a reviewer reconstruct why policy-as-code was accepted as overlapping but not equivalent?

Expected answer: yes. The proposal, decision, replay, evidence record, and research note show the source family, comparison dimensions, mismatches, accepted placement, and non-claims.

## Non-Claims

This evidence record does not prove that all policy-as-code systems are relevant to admissibility.

This evidence record does not prove that policy-as-code is equivalent to Policy Reference.

This evidence record does not replace formalism-tests or executable receipts.
