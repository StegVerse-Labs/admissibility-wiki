# DecisionAssure Pilot Canonicalization Specification

## Scope

This specification defines the bounded canonicalization used by the revised Rigel pilot package. It does not claim to reproduce DecisionAssure's native canonicalization unless independently confirmed by DecisionAssure.

## JSON canonical form

1. Parse each input as a JSON object.
2. Reject duplicate keys, non-finite numbers, and non-object top-level values.
3. Serialize with UTF-8, lexicographically sorted object keys, no insignificant whitespace, and `ensure_ascii=false`.
4. Compute SHA-256 over the serialized bytes.

Equivalent Python expression:

```python
json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
```

## Evaluation order

1. Validate schemas and referenced identifiers.
2. Resolve the delegation by `delegation_ref` and confirm actor, action, status, and scope.
3. Resolve both the referenced pre-commit policy and the current policy.
4. Determine whether a policy mutation became effective before commit.
5. Compare the DecisionAssure result with the independently derived StegVerse result.
6. Fail closed on missing, malformed, ambiguous, or inconsistent evidence.

## Pilot decision rule

For `trace_rigel_revised`, the current policy is v2 and denies `publish_associated_result`. Because the policy mutation occurred before commit, a v1 continuity path cannot authorize the action. The expected bounded result is:

```text
DENY / POLICY_DRIFT
authority_effect = NONE
```

## Non-claims

Passing this verifier establishes only deterministic consistency of the supplied pilot files. It does not establish native DecisionAssure execution, certification, endorsement, general interoperability, standing, publication authority, or execution authority.
