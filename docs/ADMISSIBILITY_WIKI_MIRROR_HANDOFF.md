# Admissibility Wiki Mirror Handoff

This file is the source of truth for continuing `StegVerse-Labs/admissibility-wiki` work across sessions.

## Current goal

```text
governed-ecosystem-transition-framing
```

The current goal is to present StegVerse as a governed ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs. External frameworks remain one input class, not the center of the architecture.

## Current version

```text
0.3.0-external-framework-input-class
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_STATUS_PRESENT
GOVERNED_ECOSYSTEM_TRANSITION_VALIDATOR_PRESENT
EXTERNAL_FRAMEWORK_INPUT_CLASS_FRAMING_PRESENT
EXTERNAL_FRAMEWORK_INPUT_CLASS_STATUS_PRESENT
EXTERNAL_FRAMEWORK_INPUT_CLASS_VALIDATOR_PRESENT
README_LINK_PRESENT
CURRENT_TASK_SYNC_UPDATED
LOCAL_DOCS_ONLY
```

## Source-of-truth documents

```text
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
docs/governance/current-task-sync.md
docs/governance/governed-ecosystem-transitions.md
docs/governance/external-frameworks-as-input-class.md
static/status/governed-ecosystem-transitions-status.json
static/status/external-framework-input-class-status.json
scripts/check_governed_ecosystem_transitions_status.py
scripts/check_external_framework_input_class_status.py
README.md
package.json
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

## External-framework input-class path

```text
external framework artifact
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
python scripts/check_external_framework_input_class_status.py
npm run validate:governed-ecosystem-transitions
npm run validate:external-framework-input-class
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

External framework pages remain valid but are now presented as one governed input class. Generated compatibility reports and page-status blocks are compatibility evidence only and do not grant certification, endorsement, formalism adoption, admissibility proof, execution authority, or canonical STRP admission.

## Known remaining installation targets

```text
StegVerse-Labs/admissibility-wiki:
  - public deployment verification for governed ecosystem transition and external-framework input-class pages
  - optional generated status surface grouping all input classes

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

Let the canonical validation workflow validate and deploy the new pages. If continuing before workflow evidence is visible, the next local build candidate is an input-class registry/status surface grouping external frameworks, LLM or agent outputs, human requests, repo tasks, SDK requests, runtime observations, and receipt-chain continuations.

## Handoff instruction

Continue from this file before relying on prior chat context.
