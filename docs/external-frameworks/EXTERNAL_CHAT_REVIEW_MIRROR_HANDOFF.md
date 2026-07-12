# External Chat Review Mirror Handoff

## Current state

```text
Goal: cooperative external-framework review with bounded correction receipts
Phase: reviewer-delegation-contract-installed
Result: repository contracts installed; live validation pending
```

## Canonical contracts

```text
docs/external-frameworks/schemas/external-chat-cooperative-review-package.schema.json
docs/external-frameworks/schemas/external-chat-correction-receipt.schema.json
docs/external-frameworks/schemas/external-chat-reviewer-delegation.schema.json
docs/external-frameworks/examples/external-chat-cooperative-review-package.example.json
docs/external-frameworks/examples/external-chat-correction-receipt.example.json
docs/external-frameworks/examples/external-chat-reviewer-delegation.example.json
scripts/check_external_chat_review_packets.py
scripts/check_goal5_external_frameworks_all.py
```

The review-packet validator is included in the Goal 5 aggregate.

## Reviewer delegation contract

A reviewer delegation binds:

```text
reviewer_ref
token_sha256
delegation_ref
scopes
valid_from
valid_until
```

Allowed scopes are bounded field scopes, `publication_review`, or an explicit wildcard. A delegation is rejected when its token hash is malformed, its validity window is invalid, its scopes are empty or malformed, or any authority-boundary field is not false.

## Runtime implementation reference

The authenticated transport is implemented in `StegVerse-org/LLM-adapter`:

```text
llm_adapter/external_review_store.py
llm_adapter/external_review_api.py
llm_adapter/combined_gateway.py
tests/test_external_review_api.py
```

The transport stores only the explicit cooperative-review package, never the raw framework artifact by default. It requires reviewer identity, current delegation, and field-scope verification before issuing a correction receipt.

## Boundary

```text
review package != publication authority
review intake receipt != correction receipt
reviewer delegation != certification authority
reviewer delegation != execution authority
correction receipt != publication authority
correction receipt != standing
```

## Next task

```text
1. Verify the Goal 5 aggregate with the reviewer-delegation contract.
2. Add a reviewer-facing console for package lookup and scoped correction preparation.
3. Define a separate wiki-publication transition that consumes reviewed receipts.
4. Require independent publication authority before any compatibility page or report changes.
5. Record live transport and workflow evidence before launch claims.
```
