---
title: Proposal Intake Interface
---

# Proposal Intake Interface

## Purpose

The proposal intake interface is the user-facing entry point for submitting governed Admissibility Wiki proposals.

It supports both guided users and users who already know the manifest/receipt structure.

## Interface Rule

The interface has two input modes and one shared output window.

```text
Option 1: Guided Builder
Option 2: Direct Manifest/Receipt Paste
Shared Output: Manifest/Receipt Preview Window
```

## Option 1: Guided Builder

The user enters each required field through form controls.

The interface generates the manifest and receipt preview from those fields.

This mode is intended for users who know what they want to submit but do not yet know the complete schema.

## Option 2: Direct Paste

The user pastes a manifest/receipt object into the same preview window.

This mode is intended for users, researchers, maintainers, LLM-assisted workflows, and ecosystem agents already familiar with the structure.

## Shared Preview Window

Both options produce the same candidate governed data object.

The preview window does not submit, accept, prove, or activate the proposal.

## Preferred Triage Boundary

A valid manifest/receipt object may receive preferred triage because it can be parsed, validated, compared, and routed more easily.

Preferred triage is not acceptance authority.

## Static Scaffold

A static browser scaffold exists at:

```text
/intake/manifest-receipt-intake.html
```

Expected GitHub.io path after deployment:

```text
https://stegverse-labs.github.io/admissibility-wiki/intake/manifest-receipt-intake.html
```

## Current Implementation Posture

```text
ui_scaffold: installed
static_preview_generation: installed
paste_parse_preview: installed
backend_submission: not_installed
automatic_receipt_issuance: not_installed
automatic_queue_write: not_installed
automatic_ai_review: not_installed
automatic_decision_publication: not_installed
```

## Done Criteria For Active Intake

The proposal submission mechanism is active only when:

- the public interface loads;
- guided fields generate a manifest/receipt preview;
- pasted JSON is parsed into the same preview window;
- submission creates or routes an incoming governed data object;
- the system issues a durable submission receipt;
- the proposal enters a review queue;
- the receipt records submission timing;
- review and decision records remain separate from the receipt.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Related Pages

- [Manifest Receipt Submission](./manifest-receipt-submission.md)
- [Proposal Lifecycle](./proposal-lifecycle.md)
- [Decision Record](./decision-record.md)
- [Transition Origin Governance](./transition-origin-governance.md)
