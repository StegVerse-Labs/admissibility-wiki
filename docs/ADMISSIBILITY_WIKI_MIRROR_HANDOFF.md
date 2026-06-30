# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

The current goal is to present StegVerse as a governed ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs. External frameworks remain one input class, not the center of the architecture.

## Current version

```text
1.0.0-ecosystem-capability-status-page
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT
GOVERNED_TRANSITION_MAP_PRESENT
CAPABILITY_LIFECYCLE_REGISTRY_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_EXAMPLE_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_EXAMPLE_VALIDATOR_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_PAGE_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_PAGE_VALIDATOR_PRESENT
WORKFLOW_GREEN_REPORTED
LOCAL_DOCS_ONLY
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/capability-lifecycle.md
docs/governance/ecosystem-capability-status.md
static/status/capability-lifecycle-status.json
static/status/ecosystem-capability-status.example.json
static/status/ecosystem-capability-status-page.json
scripts/check_capability_lifecycle_status.py
scripts/check_ecosystem_capability_status_example.py
scripts/check_ecosystem_capability_status_page.py
package.json
```

## Capability lifecycle states

```text
proposed
implemented
internally_validated
release_authorized
publicly_verified
operational
deprecated
```

## Validation

```text
python scripts/check_capability_lifecycle_status.py
python scripts/check_ecosystem_capability_status_example.py
python scripts/check_ecosystem_capability_status_page.py
npm run validate:capability-lifecycle
npm run validate
```

## Path display rule

Paths normally beginning with a leading dot are displayed without that leading dot in this handoff for iOS readability. Actual repository paths that display as `github/...` use `.github/...` in the repository.

## Workflow policy

Only one active workflow is intended to exist:

```text
github/workflows/validate-chain-continuation.yml
```

The iOS-safe mirror is:

```text
iosnoperiod/github/workflows/validate-chain-continuation.yml
```

Do not add a second active workflow for this goal.

## Known remaining installation targets

```text
StegVerse-Labs/admissibility-wiki:
  - add package validation wiring for ecosystem capability status example and page if accepted
  - validate through canonical workflow
  - public deployment verification for governed ecosystem pages

StegVerse-Labs/Site:
  - mirror/public summary of governed ecosystem transition framing after admissibility-wiki validation

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness for governed ecosystem transition framing after admissibility-wiki validation

stegguardian-wiki:
  - downstream summary of governed input/output transition boundary once admissibility-wiki validation is stable
```

## Boundary rules

This wiki records vocabulary, proof framing, lifecycle classification, and public explanation paths.

This wiki does not claim live connector installation, production authority, canonical STRP admission, or release status.

## Next build candidate

Let the canonical validation workflow validate the lifecycle and status pages. If continuing before workflow evidence is visible, package validation wiring remains the only local integration gap and may be retried carefully.

## Handoff instruction

Continue from this file before relying on prior chat context.
