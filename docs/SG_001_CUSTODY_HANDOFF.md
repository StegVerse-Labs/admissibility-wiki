# SG-001 Source Artifact Custody Handoff

## Purpose

This file preserves all session-specific continuation information for the recovered SG-001 image set so future work does not require access to the originating conversation.

## Authority

```text
Repository: StegVerse-Labs/admissibility-wiki
Authority page: docs/formalisms/original-drawing-reference.md
Custody manifest: static/provenance/sg-001-source-artifact-custody.json
Continuation issue: #13 Migrate exact SG-001 recovered JPEGs into repository custody
```

## Decisions Preserved

```text
Source Geometry ID: SG-001
Creator: Rigel Randolph
Classification: pre-BCAT/GCAT precursor source geometry
Current earliest preserved-copy date: 2026-03-05
Public rendered asset is a display reference only.
Exact source-file equivalence with the public rendered asset is not asserted.
Admissibility Wiki remains provenance authority.
Publisher and Site remain citation/display surfaces only.
```

## Recovered Evidence

The five recovered files, exact filenames, SHA-256 hashes, sizes, dimensions, and media types are recorded in:

```text
static/provenance/sg-001-source-artifact-custody.json
```

Current durable storage location:

```text
ChatGPT File Library
```

Retrieval method:

```text
Search File Library using each exact filename from the custody manifest.
Verify SHA-256 before any migration or use.
```

## Completed Work

```text
- Original Drawing Reference page updated with creator, chronology, source geometry ID, custody posture, and boundaries.
- Public rendered reference linked from the formalism page.
- Machine-readable custody manifest committed.
- Exact filenames and SHA-256 hashes committed.
- Repository migration target declared.
- GitHub Issue #13 created with migration completion conditions.
- Original Drawing Reference page linked to the manifest and Issue #13.
```

## Remaining Work

```text
Task: migrate the five exact JPEG files from ChatGPT File Library.
Destination: static/source-artifacts/SG-001/
Verification: each committed file must match the SHA-256 in the custody manifest.
Additional record: add repository checksum ledger.
Manifest update: change repository_binary_migration_pending to repository-custodied after verification.
```

## Ownership and Reassignment

```text
Current session claim: released after this handoff commit.
Durable task owner: GitHub Issue #13 / future admissibility-wiki continuation session.
Manual task requirement from this session: none.
Pending observation requirement: none owned by this session.
```

## Permitted Continuation Scope

A future continuation session may:

```text
- retrieve the exact files from File Library;
- verify hashes;
- commit them into the declared target path;
- add a checksum ledger;
- update the custody manifest and Issue #13;
- validate public display and custody links.
```

A future continuation session must not treat file migration as proof of:

```text
- original creation date;
- earliest upload date;
- derivation;
- priority;
- originality;
- formal correctness;
- admissibility;
- execution authority.
```

## Archive Readiness

```text
thread_archive_ready: true
reason: all unique decisions, evidence identifiers, hashes, completed work, remaining work, ownership state, continuation scope, and boundaries are durably recorded in this handoff, the custody manifest, the formalism page, and GitHub Issue #13.
```
