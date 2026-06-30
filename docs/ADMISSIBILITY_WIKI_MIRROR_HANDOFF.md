# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

## Current version

```text
1.2.0-governed-ecosystem-public-index
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
GOVERNED_ECOSYSTEM_INDEX_PRESENT
GOVERNED_ECOSYSTEM_INDEX_STATUS_PRESENT
GOVERNED_ECOSYSTEM_INDEX_VALIDATOR_PRESENT
SIDEBAR_NAVIGATION_PRESENT
LOCAL_DOCS_ONLY
```

## Public-facing verification page

```text
https://stegverse-labs.github.io/admissibility-wiki/governance/ecosystem-capability-status
```

## Public-facing index page

```text
https://stegverse-labs.github.io/admissibility-wiki/governance/governed-ecosystem-index
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/governed-ecosystem-index.md
docs/governance/ecosystem-capability-status.md
static/status/governed-ecosystem-index-status.json
static/status/ecosystem-capability-status.example.json
static/status/ecosystem-capability-status-page.json
scripts/check_governed_ecosystem_index_status.py
scripts/check_ecosystem_capability_status_example.py
scripts/check_ecosystem_capability_status_page.py
sidebars.js
package.json
```

## Validation

```text
python scripts/check_governed_ecosystem_index_status.py
python scripts/check_ecosystem_capability_status_example.py
python scripts/check_ecosystem_capability_status_page.py
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
  - wire governed ecosystem index validator into aggregate package validation if desired
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

## Handoff instruction

Continue from this file before relying on prior chat context.
