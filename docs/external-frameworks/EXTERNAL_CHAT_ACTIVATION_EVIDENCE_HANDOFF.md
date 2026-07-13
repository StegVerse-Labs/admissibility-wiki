# External Chat Activation Evidence Handoff

## Current state

```text
Goal: receive and validate exact deployment-correlated External Chat evidence from StegVerse-Labs/Site
Phase: canonical receiving contract and fail-closed importer installed
Result: CONTRACT_INSTALLED_OBSERVED_SITE_ARTIFACT_PENDING
```

## Source artifact

The source repository is `StegVerse-Labs/Site` and the expected artifact is:

```text
reports/external-chat-activation-evidence.json
```

The record correlates local Site validation, exact commit and workflow identity, Pages deployment URL, post-deployment page and gateway observations, and mutation-disabled posture.

## Installed contracts

```text
docs/external-frameworks/schemas/external-chat-activation-evidence.schema.json
docs/external-frameworks/examples/external-chat-activation-evidence.example.json
scripts/check_external_chat_activation_evidence.py
scripts/import_external_chat_activation_evidence.py
scripts/check_external_chat_activation_importer.py
receipts/external-chat-activation-evidence-contract-2026-07-13.json
scripts/check_goal5_external_frameworks_all.py
```

## Accepted result classes

```text
OBSERVED_NON_MUTATING_PUBLIC_PATHS
LOCAL_VALIDATION_NOT_CONFIRMED
LIVE_EVIDENCE_NOT_AVAILABLE
LIVE_EVIDENCE_NOT_CONFIRMED
```

`OBSERVED_NON_MUTATING_PUBLIC_PATHS` is accepted only when local validation passed, the post-deployment receipt passed, and mutation was observed disabled.

## Import behavior

The importer accepts a local path or HTTP(S) URL through:

```text
python scripts/import_external_chat_activation_evidence.py <source>
STEGVERSE_EXTERNAL_CHAT_ACTIVATION_EVIDENCE_SOURCE=<source>
```

With no source configured it exits without mutation. With a source configured it fails closed unless source repository identity, record identity, authority boundary, result predicates, and evidence SHA-256 all match.

A valid import atomically writes:

```text
static/status/external-chat-activation-evidence.json
static/status/external-chat-activation-evidence.provenance.json
```

## Authority boundary

```text
contract installation != observed deployment evidence
activation evidence != deployment authority
activation evidence != repository mutation authority
activation evidence != publication authority
activation evidence != certification
activation evidence != standing
wiki projection != source authority
mutation remains separately authorized
```

## Next tasks

```text
1. Preserve the first successful Site external-chat-activation-evidence artifact with exact workflow and commit identity.
2. Import that exact artifact through the fail-closed importer.
3. Verify the projected evidence and provenance records through Goal 5.
4. Require mutation_required_disabled = true before recording observed non-mutating public paths.
5. Do not convert the imported observation into certification, compatibility standing, publication authority, or mutation authority.
6. Perform one separately authorized disposable staging mutation only after the non-mutating public evidence is observed and preserved.
```

## Sharing posture

The Admissibility Wiki now has a canonical, content-bound receiving path for External Chat activation evidence. No observed Site artifact has yet been imported by this installation, and no deployment, publication, mutation, certification, or standing claim follows from the contract alone.
