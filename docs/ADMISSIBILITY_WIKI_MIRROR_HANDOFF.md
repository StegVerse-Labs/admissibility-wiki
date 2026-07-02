# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
repo-standards-integration-and-installation-bundle-pending-release
```

## Current version

```text
1.5.1-repo-standards-validation-report-wired
```

## Current status

```text
REPO_STANDARDS_INTEGRATION_PAGE_WIRED
REPO_STANDARDS_INSTALLATION_BUNDLE_PAGE_WIRED
REPO_STANDARDS_INTEGRATION_VALIDATOR_WIRED
REPO_STANDARDS_INTEGRATION_STATUS_WIRED
REPO_STANDARDS_RELEASE_UPDATE_QUEUE_WIRED
REPO_STANDARDS_INSTALLATION_BUNDLE_PLAN_WIRED
REPO_STANDARDS_INSTALLATION_VALIDATION_REPORT_WIRED
SIDEBAR_NAVIGATION_PRESENT
UPSTREAM_REPO_STANDARDS_RELEASE_READY
UPSTREAM_TAG_RELEASE_PENDING_OUTSIDE_CONNECTOR
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

## Repo-standards integration pages

```text
docs/governance/repo-standards-integration.md
docs/governance/repo-standards-installation-bundle.md
```

Sidebar entries:

```text
governance/repo-standards-integration
governance/repo-standards-installation-bundle
```

Machine-readable status:

```text
static/status/repo-standards-integration-status.json
static/status/repo-standards-integration-release-update-queue.json
static/status/repo-standards-installation-bundle-plan.json
static/status/repo-standards-installation-validation-report.json
```

Validator:

```text
scripts/check_repo_standards_integration.py
```

Package command:

```text
npm run validate:repo-standards-integration
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/repo-standards-integration.md
docs/governance/repo-standards-installation-bundle.md
static/status/repo-standards-integration-status.json
static/status/repo-standards-integration-release-update-queue.json
static/status/repo-standards-installation-bundle-plan.json
static/status/repo-standards-installation-validation-report.json
docs/governance/governed-ecosystem-index.md
docs/governance/ecosystem-capability-status.md
static/status/governed-ecosystem-index-status.json
static/status/ecosystem-capability-status.example.json
static/status/ecosystem-capability-status-page.json
static/status/guardian-destination-resolution-status.json
scripts/check_repo_standards_integration.py
scripts/check_governed_ecosystem_index_status.py
scripts/check_ecosystem_capability_status_example.py
scripts/check_ecosystem_capability_status_page.py
sidebars.js
package.json
```

## Validation

```text
python scripts/check_repo_standards_integration.py
npm run validate:repo-standards-integration
python scripts/check_governed_ecosystem_index_status.py
npm run validate:governed-ecosystem-index
npm run validate
```

Expected current state from prior handoff:

```text
GOVERNED_ECOSYSTEM_INDEX_PACKAGE_WIRED
SIDEBAR_NAVIGATION_PRESENT
```

Additional current docs state:

```text
REPO STANDARDS INTEGRATION: PASS - integration, installation bundle, and validation report surfaces present
```

## Upstream repo-standards state

```text
Repository: StegVerse-Labs/repo-standards
Manual main validation: successful via Declared Tasks #5 screenshot
Release readiness report: updated with tag_allowed true
Actual Git tag/release: pending outside current connector action set
```

## Remaining targets

```text
StegVerse-Labs/admissibility-wiki:
  - run local/wiki validation after repo-standards installation validation report wiring
  - update repo-standards integration and installation pages after upstream tag/release exists
  - public deployment verification

StegVerse-Labs/Site:
  - mirror public summary after wiki validation and repo-standards tag/release

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness after wiki validation and repo-standards tag/release

StegVerse-002/stegguardian-wiki:
  - downstream public Guardian summary after wiki validation and repo-standards tag/release

StegVerse-002/StegGuardian:
  - private Guardian implementation standing-boundary awareness after wiki validation
```

## Boundary rules

This wiki records vocabulary, proof framing, lifecycle classification, public explanation paths, release-gated integration references, and release-gated bundle installation doctrine.

It does not claim production authority or release status.

It must not treat an untagged upstream release as final authority.

It must not treat bundle installation as admissibility or runtime authority.

## Handoff instruction

Continue from this file before relying on prior chat context.
