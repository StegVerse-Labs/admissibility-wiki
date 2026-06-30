# Governed Ecosystem Transitions

## Purpose

This page reframes the Admissibility Wiki around the broader StegVerse claim:

```text
StegVerse is a governed transition ecosystem for inputs, proposed actions, desired outputs, and receipt-bound outputs.
```

External frameworks remain important, but they are one input class rather than the center of the system.

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

## Meaning

StegVerse does not merely review artifacts.

StegVerse governs how artifacts become transitions.

That means the governance question is not only:

```text
What did an external framework produce?
```

The governance question becomes:

```text
Can this input, action, communication, or desired output become an admitted transition under current standing?
```

## Input classes

The same transition path may govern multiple input classes:

```text
external framework outputs
LLM or agent outputs
human requests
repo tasks
SDK requests
memory or KnowledgeVault entries
runtime observations
receipt-chain continuations
```

Each class may require different evidence, authority, boundary, privacy, or continuity constraints, but each must enter through governed transition handling before it can become consequence-bearing state.

## Output classes

The same transition path also governs outputs:

```text
admitted response
committed repo change
receipt record
STRP handoff
state-transition summary
denial receipt
fail-closed receipt
```

A desired output is not treated as admissible merely because a tool can produce it. It must remain governed until the point of commitment.

## Relationship to external frameworks

External frameworks are now presented as one input category:

```text
external framework artifact -> governed ingestion -> admissibility path -> receipt-bound result
```

This avoids over-centering the comparison surface and keeps the public claim focused on the ecosystem:

```text
StegVerse can accept many kinds of inputs, evaluate transition standing, and return governed outputs with receipts.
```

## Relationship to StegClaw

StegClaw provides the current working example of a governed tool/agent transition path:

```text
StegClaw task
  -> standing envelope
  -> ingestion candidate
  -> outbound envelope
  -> live integration manifest
  -> target-side handoff
  -> ecosystem verification
```

The generated StegClaw artifacts demonstrate how a tool or agent output can remain local-only, non-mutating, non-networked, and receipt-bound until admitted by target-side governance.

## Relationship to STRP

STRP is the transition-record continuity layer for passing transition state between systems or entities.

A governed output should carry enough final transition data for the next system to evaluate:

```text
what was requested
what was evaluated
what was allowed or denied
what hashes and receipts bind the transition
what authority was or was not present
```

## Boundary

This page is a public framing document. It does not claim live connector installation, production mutation authority, canonical STRP admission, or external certification.

## Current status

```text
GOVERNED_ECOSYSTEM_TRANSITION_FRAMING_PRESENT
```
