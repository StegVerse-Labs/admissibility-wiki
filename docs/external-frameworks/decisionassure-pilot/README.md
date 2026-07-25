# DecisionAssure / StegVerse Revised Pilot Package

This directory contains the five-file package previously committed for the bounded DecisionAssure interoperability pilot:

- `trace_rigel_revised.json`
- `canonical_policies.json`
- `canonical_delegations.json`
- `canonicalization_spec.md`
- `verifier_rigel_revised.py`

## Run

```bash
python docs/external-frameworks/decisionassure-pilot/verifier_rigel_revised.py
```

A successful run writes `verification_receipt.json` and returns:

```text
DECISIONASSURE_RIGEL_REVISED_VERIFICATION: PASS
```

## Result represented by this package

```text
DecisionAssure: DENY / CORRUPT / causal_continuity_persisted=false
StegVerse: DENY / POLICY_DRIFT
authority_effect: NONE
```

## Status boundary

This package is now complete as a StegVerse-authored, deterministic pilot submission. It is suitable for collaborator review and reciprocal verifier testing.

It does not claim that DecisionAssure authored these files, that its native verifier has executed them, or that general compatibility, certification, standing, publication authority, or execution authority has been established.
