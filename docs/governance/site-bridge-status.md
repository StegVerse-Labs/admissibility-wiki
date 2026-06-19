---
title: Site Bridge Status
---

# Site Bridge Status

## Purpose

This page records the coordination boundary between `StegVerse-Labs/admissibility-wiki` and `StegVerse-Labs/Site`.

The Admissibility Wiki is the governed vocabulary, terminology convergence, proposal-review, ontology, and proof-path surface.

The Site repository may later link, summarize, or display selected wiki material, but Site work must not silently redefine wiki governance posture.

## Page Status

```text
active
```

## Page Posture

```text
governance policy
```

## Maturity Posture

```text
conceptual
```

## Authority Boundary

This page coordinates repository boundaries. It does not authorize Site deployment, change DNS, publish the public domain, or replace the Site handoff.

## Bridge Rule

Before changing Site-facing display or public presentation behavior for Admissibility Wiki material, check the current Site handoff.

```text
StegVerse-Labs/Site/docs/SITE_MIRROR_HANDOFF.md
```

Do not assume that a wiki page is ready for Site display merely because it exists in the wiki.

## Current Wiki Source Of Truth

The current Admissibility Wiki source-of-truth files are:

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/current-task-sync.md
static/status/admissibility-wiki-status.json
```

## Current Site Bridge Posture

```text
bridge_status: pending_site_handoff_reconciliation
site_display_authority: not_granted_by_this_page
wiki_source_authority: admissibility-wiki-governance
activation_dependency: admissibility.stegverse.org public validation
```

## What May Be Linked Or Displayed

After Site handoff reconciliation, the Site repo may link or display:

- the public wiki landing page;
- glossary pages;
- terminology convergence policy;
- proposal lifecycle policy;
- decision record policy;
- proof-path examples;
- ontology JSON;
- public status JSON.

## What Must Not Be Presented As Authority

The Site repo must not present any of the following as executable proof authority unless the relevant proof artifact is linked:

- glossary definitions;
- terminology equivalence claims;
- proposal examples;
- decision examples;
- replay examples;
- status JSON.

These artifacts explain governance posture. They do not replace formalism-tests or executable receipts.

## Governance Links

```yaml
governance:
  proposal_link: "not_applicable"
  decision_link: "not_applicable"
  replay_link: "not_applicable"
  reconstruction_link: "not_applicable"
```

## Related Pages

- [Current Task Sync](./current-task-sync.md)
- [Terminology Convergence](./terminology-convergence.md)
- [Proposal Lifecycle](./proposal-lifecycle.md)
- [Decision Record](./decision-record.md)
