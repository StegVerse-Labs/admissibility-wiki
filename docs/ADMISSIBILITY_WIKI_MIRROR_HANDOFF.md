# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

## Current version

```text
1.1.0-ecosystem-capability-status-package-wired
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT
GOVERNED_TRANSITION_MAP_PRESENT
CAPABILITY_LIFECYCLE_REGISTRY_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_EXAMPLE_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_PAGE_PRESENT
ECOSYSTEM_CAPABILITY_STATUS_PACKAGE_WIRED
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

## Validation

```text
python scripts/check_capability_lifecycle_status.py
python scripts/check_ecosystem_capability_status_example.py
python scripts/check_ecosystem_capability_status_page.py
npm run validate:capability-lifecycle
npm run validate:ecosystem-capability-status-example
npm run validate:ecosystem-capability-status-page
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

## Known remaining installation targets

```text
StegVerse-Labs/admissibility-wiki:
  - validate through canonical workflow
  - public deployment verification for governed ecosystem pages

StegVerse-Labs/Site:
  - mirror public summary after admissibility-wiki validation

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after admissibility-wiki validation

stegguardian-wiki:
  - downstream summary after admissibility-wiki validation
```

## Boundary rules

This wiki records vocabulary, proof framing, lifecycle classification, and public explanation paths.

This wiki does not claim live connector installation, production authority, canonical STRP admission, or release status.

## Next build candidate

Let the canonical validation workflow validate the package-wired lifecycle and status pages. If continuing before workflow evidence is visible, the next local candidate is public navigation/index consolidation for governed ecosystem pages.

## Handoff instruction

Continue from this file before relying on prior chat context.
