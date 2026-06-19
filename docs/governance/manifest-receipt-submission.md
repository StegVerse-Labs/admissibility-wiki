---
title: Manifest Receipt Submission
---

# Manifest Receipt Submission

## Purpose

Manifest receipt submission is the preferred structured intake path for Admissibility Wiki proposals.

It allows a user, researcher, maintainer, browser flow, LLM-assisted process, or ecosystem agent to submit a proposal as a governed data object instead of only as free text.

## Core Rule

A proposal submitted with a valid transition manifest and submission receipt may receive routing preference because it is easier to validate, route, replay, compare, and reconstruct.

Preference is a processing posture only.

Preference does not mean acceptance.

## Dual-Mode Intake Interface

The proposal intake interface should provide two input options that write to the same manifest/receipt preview window.

### Option 1: Guided Builder

The user enters each required manifest and receipt field through fillable fields.

As fields are completed, the page generates the manifest and receipt structure in a preview window below the fields.

This mode is for users who understand the proposal but do not yet know the manifest schema.

### Option 2: Direct Manifest/Receipt Paste

The user pastes an existing manifest/receipt structure into the same preview window.

This mode is for users already familiar with the StegVerse-compatible structure.

The pasted structure should be parsed, validated, and reflected back into the guided fields when possible.

## Shared Preview Rule

Both modes use the same output window.

```text
fillable fields -> manifest/receipt preview
pasted structure -> manifest/receipt preview
```

The preview window is the candidate governed data object.

The preview does not submit, approve, validate, or accept the proposal by itself.

## Why This Exists

The wiki accepts broad input, but broad input should not collapse into untraceable editorial discretion.

A manifest/receipt submission lets the proposal arrive with:

- declared proposer class;
- target page or artifact;
- proposal class;
- claimed relationship type;
- transition origin claim;
- evidence references;
- timing record;
- non-claims;
- replay expectation;
- decision-route request.

This makes the proposal compatible with StegVerse ecosystem governance from the point of intake.

## Submission Lanes

```text
lane_1_manifest_receipt:
  status: preferred
  description: Structured proposal submitted with transition manifest and receipt fields.

lane_2_structured_form:
  status: accepted
  description: User completes guided fields but does not provide a full manifest.

lane_3_plain_text:
  status: accepted
  description: User submits a plain-language proposal that must be normalized before review.

lane_4_external_reference:
  status: accepted
  description: User submits a source, paper, standard, implementation, counterexample, or dispute reference.
```

## Priority Meaning

Priority means:

- earlier triage when queues are constrained;
- lower normalization burden;
- easier duplicate detection;
- easier relationship classification;
- easier transition-origin review;
- easier replay and reconstruction;
- easier conversion into a decision record.

Priority does not mean:

- automatic acceptance;
- correctness;
- authority;
- proof;
- endorsement;
- commit-time validity;
- equivalent-term standing.

## Required Manifest Fields

```json
{
  "schema": "admissibility_wiki_submission_manifest.v1",
  "proposal_id": "pending",
  "submitted_at": "2026-06-19T00:00:00Z",
  "submitter_class": "user | researcher | maintainer | browser_originated | llm_assisted | ecosystem_agent",
  "target": {
    "type": "glossary_page | governance_page | ontology_entry | proof_path | external_reference | dispute",
    "path": "docs/glossary/example.md"
  },
  "proposal": {
    "class": "term_proposal | term_revision | equivalence_claim | overlap_claim | adjacency_claim | implementation_mapping | external_reference | counterexample | dispute | proof_path_example",
    "summary": "Short proposal summary.",
    "requested_outcome": "ALLOW | ALLOW_AS_OVERLAP | DENY | ESCALATE | REFUSE | DEFER | SUPERSEDE"
  },
  "transition_origin_claim": {
    "derived_from": "Transition Table | Transition Blocks | Both | External Mapping | Unknown",
    "transition_table_elements": [],
    "transition_blocks": [],
    "standing": "Native StegVerse Concept | Derived StegVerse Concept | External Equivalent | External Overlap | External Adjacent | Unclassified"
  },
  "relationship_claims": [],
  "evidence_refs": [],
  "non_claims": [],
  "receipt_request": {
    "include_submission_timing": true,
    "include_hashes": true,
    "include_replay_expectation": true
  }
}
```

## Required Receipt Fields

```json
{
  "schema": "admissibility_wiki_submission_receipt.v1",
  "receipt_id": "receipt.pending.example",
  "proposal_id": "proposal.pending.example",
  "received_at": "2026-06-19T00:00:00Z",
  "receipt_issued_at": "2026-06-19T00:00:05Z",
  "submission_lane": "lane_1_manifest_receipt",
  "preference_posture": "preferred_triage",
  "validation_posture": "valid_manifest | invalid_manifest | partial_manifest | unstructured",
  "tasks": [
    {
      "task": "capture_submission",
      "started_at": "2026-06-19T00:00:00Z",
      "completed_at": "2026-06-19T00:00:01Z",
      "status": "completed",
      "timing_posture": "recorded"
    }
  ],
  "non_claims": [
    "Receipt does not accept the proposal.",
    "Receipt does not prove the submitted claim.",
    "Receipt does not create equivalent-term standing."
  ]
}
```

## Intake Decision Rule

A valid manifest can affect routing priority.

It cannot decide the proposal outcome.

The proposal still requires:

- review posture;
- evidence posture;
- relationship classification;
- transition-origin classification;
- authority class;
- decision record;
- replay record where mature;
- reconstruction note where mature.

## Compatibility With StegVerse Ecosystem

A manifest/receipt submission should be treated as an incoming governed piece of data.

Default posture:

```text
incoming_governed_data
not_effect_capable_by_default
not_accepted_by_receipt
requires_review_before_standing
```

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Related Pages

- [Proposal Lifecycle](./proposal-lifecycle.md)
- [Decision Record](./decision-record.md)
- [Transition Origin Governance](./transition-origin-governance.md)
- [Terminology Convergence](./terminology-convergence.md)
