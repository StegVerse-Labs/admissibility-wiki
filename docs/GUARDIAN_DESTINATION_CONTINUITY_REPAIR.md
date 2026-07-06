# Guardian Destination Continuity Repair

Status: draft repair proposed

## Failure class

Recent `Validate chain continuation` failures are concentrated around the admissibility-wiki activation/continuation path. The repo had two mirror handoff surfaces:

```text
ADMISSIBILITY_MIRROR_HANDOFF.md
docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md
```

The docs handoff is the active source of truth, while the root file was stale enough to confuse session and tool orientation.

The Guardian destination resolver also checked only old `StegVerse-Labs/*` destination candidates while the current status artifact and handoff identify canonical `StegVerse-002/*` destinations.

## Repair

This branch:

- replaces the root handoff with a continuity pointer to `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md`;
- updates `scripts/check_guardian_destination.py` to resolve and verify the canonical public and private Guardian destinations;
- keeps the boundary fail-closed if canonical destinations cannot be confirmed.

## Non-claims

This repair does not claim public deployment success, release status, production authority, execution authority, certification, endorsement, or commit-time standing.

## Next verification

```bash
python scripts/check_guardian_destination.py
python scripts/check_admissibility_wiki_mirror_handoff_guardian_destinations.py
npm run validate:guardian-destination-resolution
npm run validate:guardian-handoff-destinations
```
