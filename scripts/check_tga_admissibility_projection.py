#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'docs' / 'governance' / 'temporal-governed-analysis.md'
HANDOFF = ROOT / 'docs' / 'TGA_ADMISSIBILITY_PROJECTION_MIRROR_HANDOFF.md'


def main() -> int:
    for path in (PAGE, HANDOFF):
        if not path.is_file():
            print(f'TGA_ADMISSIBILITY_PROJECTION=FAIL missing={path.relative_to(ROOT)}')
            return 1
    page = PAGE.read_text(encoding='utf-8')
    handoff = HANDOFF.read_text(encoding='utf-8')
    markers = [
        'Canonical representation is not canonical reality',
        'Counterfactual application must be labeled as such',
        'does not create adjudicative authority',
        'event time, legal effective time, interpretation time, and enforcement practice',
        'SUPPORTED', 'UNSUPPORTED', 'UNRESOLVED', 'CONTRADICTORY',
        'Publication, visibility, validation, reconstruction',
    ]
    missing = [marker for marker in markers if marker not in page]
    if missing:
        print('TGA_ADMISSIBILITY_PROJECTION=FAIL missing_markers=' + repr(missing))
        return 1
    if 'authority_effect: NONE_EXPLANATORY_ONLY' not in handoff:
        print('TGA_ADMISSIBILITY_PROJECTION=FAIL authority_boundary_missing')
        return 1
    print('TGA_ADMISSIBILITY_PROJECTION=PASS')
    print('authority_effect=NONE_EXPLANATORY_ONLY')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
