---
title: Portable Governed Return Path
---

# Portable Governed Return Path

This page records the public proof chain for returning a governed result to the originating customer path.

## Proof chain

```text
external LLM or UI
-> LLM-adapter fixture
-> micro-node-compatible transition request
-> SDK fixture validation
-> governed return payload
-> original customer path
```

## Completed repository proofs

```text
StegVerse-002/micro-node-runtime
  -> transition-table-native portable micro-node runtime

StegVerse-org/core-node-runtime-demo
  -> comparison of larger runtime paths against the micro-node contract

StegVerse-org/LLM-adapter
  -> fixture-bound governed return-path proof

StegVerse-org/StegVerse-SDK
  -> SDK-side validation of adapter-originated micro-node fixtures
```

## Compatibility mark

A system is compatible with this proof path when it can:

1. package an external interaction as a transition request;
2. preserve the original return path;
3. receive a terminal decision of `ALLOW`, `DENY`, or `FAIL_CLOSED`;
4. preserve a receipt reference;
5. return the governed result to the originating path without granting execution authority.

## Boundary

The current proof is fixture-bound and demonstrates contract compatibility only. It does not claim live provider activation, production authorization, public endorsement, repository mutation authority, or general validation of any external system.

## Verification commands

```bash
python tools/verify_all.py
python tools/verify_micro_node_compatibility.py
python scripts/verify_micro_node_return_path.py
python scripts/verify_micro_node_adapter_fixture.py
```

## Status

The portable governed return-path proof is established across runtime, adapter, and SDK layers. The next public step is to keep this page synchronized with release tags or additional integration receipts as those become available.
