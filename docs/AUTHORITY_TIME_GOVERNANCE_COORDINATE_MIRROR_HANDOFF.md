# Authority × Time Governance Coordinate Mirror Handoff

## Source of truth

```text
task_id: AUTHORITY-TIME-GOVERNANCE-COORDINATE-001
repository: StegVerse-Labs/admissibility-wiki
cross_repo_owner: StegVerse-Labs/.github#1154
local_issue: #134
local_pull_request: #135
branch: fix/authority-time-governance-coordinate
state: IMPLEMENTED_PENDING_EXACT_HEAD_VALIDATION_AND_MERGE
authority_effect: NONE
```

This handoff is authoritative for the bounded Authority × Time semantic/publication correction only. `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` remains authoritative for the broader wiki program.

## Canonical primitive

```text
Governance = Authority × Time
G = (Authority, Time)
```

Authority and Time are the coordinates of governance. State, evidence, verification, policy, delegation, identity, scope, recoverability, transition geometry, autonomy, consensus, and capability are evaluated context or evidence at that coordinate; none replaces either coordinate.

Temporal non-causality:

```text
Delta-time -/-> Delta-authority
```

Elapsed time alone does not create, destroy, transfer, renew, or revoke Authority. Time remains a governance coordinate.

## Installed correction surfaces

```text
docs/governance/authority-time-governance-coordinate.md
docs/governance/verification-vs-execution-authority.md
docs/formalisms/runtime-transition-governance.md
docs/glossary/commit-time-authority.md
scripts/check_verification_execution_authority.py
sidebars.js
```

## Semantic results

- Verification is evidence/context evaluated at `(Authority, Time)`; it is not a governance coordinate.
- RTG is transition geometry evaluated at `(Authority, Time)`; it is not a governance coordinate system.
- Commit-Time Authority is explicitly Authority resolved at the governing Time.
- The public Governance sidebar exposes the Authority × Time page before the verification doctrine.
- The doctrine validator now requires the coordinate page and corrected language.

## README impact

The public documentation navigation, doctrine, glossary, formalism page, and validator are the user-facing semantic entrypoints for this change. The repository README is not the canonical semantic/navigation surface for individual wiki doctrines; changing it is not required for this bounded lane. This no-change determination is evidence-supported by the existing Docusaurus `sidebars.js` navigation and `docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md` program ownership.

## Validation

Canonical workflow: `.github/workflows/validate-chain-continuation.yml`.

Exact PR #135 head must pass after the doctrine checker and sidebar changes. Historical/publication validation before those commits does not validate this correction.

## Remaining

1. exact-head validation;
2. repair only proven validator/build defects;
3. merge PR #135 after validation/review gates;
4. observe public publication after merge;
5. propagate through `StegVerse-Labs/.github#1156` to Site, Publisher, stegguardian-wiki, and other required awareness/index surfaces.

## Collision rule

Do not use this correction to modify TA-14, Conectrr, public-anchor reconstruction, unrelated external-framework dockets, or their task registries. Those remain owned by their existing handoffs/registries.

## Archive

This file plus `.github#1154` contains the bounded continuation state. The originating chat is not required for continuation.
