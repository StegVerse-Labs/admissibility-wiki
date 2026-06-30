# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

The current goal is to present StegVerse as a governed ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs. External frameworks remain one input class, not the center of the architecture.

## Current version

```text
0.8.0-capability-lifecycle-registry
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT
GOVERNED_TRANSITION_MAP_PRESENT
CAPABILITY_GENERATOR_ALIAS_PRESENT
CAPABILITY_BLOCKERS_ALIGNED_WITH_STATE_MODEL
CAPABILITY_LIFECYCLE_REGISTRY_PRESENT
CAPABILITY_LIFECYCLE_STATUS_PRESENT
CAPABILITY_LIFECYCLE_VALIDATOR_PRESENT
WORKFLOW_GREEN_REPORTED
LOCAL_DOCS_ONLY
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/current-task-sync.md
docs/governance/governed-ecosystem-transitions.md
docs/governance/external-frameworks-as-input-class.md
docs/governance/governed-input-classes.md
docs/governance/governed-output-classes.md
docs/governance/governed-transition-map.md
docs/governance/capability-lifecycle.md
static/status/capability-lifecycle-status.json
scripts/check_capability_lifecycle_status.py
docs/external-frameworks/generated-page-subsystem-capability.json
scripts/generate_external_framework_evaluation_results.py
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

## Core transition path

```text
input or request
  -> governed ingestion
  -> CGE fingerprinting
  -> GCAT / BCAT evaluation
  -> Transition Table standing
  -> ALLOW / DENY / FAIL-CLOSED
  -> receipt_chain / STRP record
  -> governed output
```

## Validation

```text
python scripts/check_capability_lifecycle_status.py
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
  - validate capability lifecycle registry through canonical workflow
  - public deployment verification for governed ecosystem pages
  - optional public navigation/index consolidation for governed ecosystem pages

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

Let the canonical validation workflow validate the capability lifecycle registry. If continuing before workflow evidence is visible, the next local build candidate is a machine-readable ecosystem capability status example using the lifecycle states.

## Handoff instruction

Continue from this file before relying on prior chat context.
