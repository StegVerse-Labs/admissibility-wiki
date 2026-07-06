# Device Continuity Layer Admissibility

Source: `StegVerse-Labs/device-continuity-layer`
Candidate tag: `v0.1.0-offline-baseline`
Status: ecosystem documentation record

## Boundary

Device Continuity Layer records are handoff candidates only. They do not grant destination authority.

## Admissibility Posture

A device record is admissible for review when it preserves:

- source repository reference,
- candidate tag or commit context,
- destination repo reference,
- handoff payload,
- destination receipt,
- reconstructable validation path.

## Installed Destination Repos

- `StegVerse-Labs/StegTalk`
- `StegVerse-Labs/StegMusic`

## Review Rule

Destination repos must issue their own receipts before treating a handoff candidate as accepted for destination use.
