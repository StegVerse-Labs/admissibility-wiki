# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

## Current version

```text
1.3.0-governed-ecosystem-index-package-wired
```

## Current status

```text
GOVERNED_ECOSYSTEM_INDEX_PACKAGE_WIRED
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
npm run validate:governed-ecosystem-index
npm run validate
```

## Remaining targets

```text
StegVerse-Labs/admissibility-wiki:
  - canonical workflow verification
  - public deployment verification

StegVerse-Labs/Site:
  - mirror public summary after wiki validation

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after wiki validation

stegguardian-wiki:
  - downstream summary after wiki validation
```

## Boundary rules

This wiki records vocabulary, proof framing, lifecycle classification, and public explanation paths.

It does not claim production authority or release status.

## Handoff instruction

Continue from this file before relying on prior chat context.
