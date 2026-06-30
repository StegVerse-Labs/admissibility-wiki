# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

The current goal is to present StegVerse as a governed ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs. External frameworks remain one input class, not the center of the architecture.

## Current version

```text
0.2.0-governed-ecosystem-transition-framing
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_STATUS_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_VALIDATOR_PRESENT
README_LINK_PRESENT
LOCAL_DOCS_ONLY
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/governed-ecosystem-transitions.md
static/status/governed-ecosystem-transitions-status.json
scripts/check_governed_ecosystem_transitions_status.py
README.md
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
python scripts/check_governed_ecosystem_transitions_status.py
npm run validate:governed-ecosystem-transitions
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

## Current external-framework posture

External framework pages remain valid but are now presented as one governed input class:

```text
external framework artifact
  -> governed ingestion
  -> admissibility path
  -> receipt-bound result
```

## Known remaining installation targets

```text
StegVerse-Labs/admissibility-wiki:
  - public deployment verification for governed ecosystem transition page
  - optional generated status surface linking external frameworks as one input class

StegVerse-Labs/Site:
  - mirror/public summary of governed ecosystem transition framing after admissibility-wiki validation

GCAT-BCAT-Engine/Publisher:
  - publication/import awareness for governed ecosystem transition framing after admissibility-wiki validation

stegguardian-wiki:
  - downstream summary of governed input/output transition boundary once admissibility-wiki validation is stable
```

## Boundary rules

This wiki records vocabulary, proof framing, and public explanation paths.

This wiki does not claim live connector installation, production mutation authority, canonical STRP admission, or release status.

## Next build candidate

Let the canonical validation workflow validate and deploy the new page. If validation fails, repair only the first failing validator field, build issue, public URL check, or handoff inconsistency identified by logs.

## Handoff instruction

Continue from this file before relying on prior chat context.
