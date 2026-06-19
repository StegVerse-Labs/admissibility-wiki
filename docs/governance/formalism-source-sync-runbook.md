---
title: Formalism Source Sync Runbook
---

# Formalism Source Sync Runbook

## Purpose

This runbook defines how the Admissibility Wiki should react when canonical formalism content changes or becomes available.

The goal is to keep the wiki aligned with formalism sources while preserving the correct authority boundary.

## Authority Boundary

```text
Admissible-Existence defines formalisms.
Publisher publishes papers and public exposition.
Admissibility Wiki mirrors, relates, crosswalks, and discovers relationships.
```

The wiki must not become the canonical source of a formalism.

## Trigger Sources

A wiki update may be required when any of these change:

```text
Admissible-Existence canonical formalism definition
Admissible-Existence formalism scope
Admissible-Existence ontology or relationship file
Admissible-Existence mathematical candidate
Admissible-Existence proof candidate
Admissible-Existence validation candidate
Publisher paper
Publisher public exposition artifact
Approved public visual reference
```

## Trigger Outcomes

Each detected change should resolve to one of these outcomes:

```text
no_wiki_change_required
wiki_update_required
wiki_update_proposed
wiki_update_applied
blocked_private_source
blocked_missing_source
superseded
```

## Sync Procedure

1. Read `static/sync/formalism-source-sync.v0.1.json`.
2. For each source, inspect public-safe canonical source refs and Publisher refs.
3. Compare the current refs with the last known refs.
4. If content changed or became available, mark the source as `wiki_update_required`.
5. Create or update the target wiki page only with public-safe content.
6. Record source, Publisher, wiki target, and non-claims.
7. Leave private source material out of the public wiki unless a public mirror boundary exists.
8. Validate with `npm run validate`.
9. Confirm publication through the visible Pages deployment path.

## Required Receipt Fields

A sync receipt should include:

```text
receipt_id
source_id
formalism_term
canonical_source_repository
canonical_source_ref
publisher_artifact_ref
wiki_target_path
prior_wiki_ref
new_wiki_ref
sync_outcome
reason
non_claims
```

## Non-Claims

```text
A sync record does not define the formalism.
A sync record does not prove the formalism.
A sync record does not validate the formalism.
A sync record does not grant execution authority.
A sync record only records that the wiki mirrored or crosswalked public-safe changes.
```

## Next Safe Build Target

Add an automated workflow that validates the sync manifest and emits a sync-needed artifact or issue when source refs change.
