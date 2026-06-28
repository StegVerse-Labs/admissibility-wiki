# Decision Vocabulary

Canonical decision values:

```text
ALLOW
DENY
CONDITIONAL
FAIL_CLOSED
```

Meanings:

- `ALLOW`: current commit-time standing is sufficient for the proposed transition.
- `DENY`: current commit-time standing was checked and is not sufficient.
- `CONDITIONAL`: named conditions must be satisfied before a new standing determination is made.
- `FAIL_CLOSED`: standing cannot be safely reconstructed from available authority, policy, delegation, evidence, context, validity, or recoverability state.

Deprecated aliases:

- `DEFER`: use `CONDITIONAL` when named conditions are pending; use `FAIL_CLOSED` when safe standing cannot be determined.
- `FAIL-CLOSED`: use `FAIL_CLOSED`.

Decision values are governance outcomes. Proof-status values such as `PASS`, `PARTIAL`, and `FAIL` describe whether a proof path supports its claimed result.
