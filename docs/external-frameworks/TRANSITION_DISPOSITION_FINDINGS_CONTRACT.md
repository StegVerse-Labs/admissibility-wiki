# Exact manifested transition findings for external frameworks

Status: SOURCE CONTRACT / NOT PUBLICATION PROOF. Coordination owner: [#66](https://github.com/StegVerse-Labs/admissibility-wiki/issues/66); existing public-anchor owner [#50](https://github.com/StegVerse-Labs/admissibility-wiki/issues/50). Parent disposition invariant: StegVerse-Labs/.github #1766 / PR #2714; SDK source adoption candidate: StegVerse-org/StegVerse-SDK #327.

## A finding is an evaluated state transition, not a framework rating

For each framework/version and test, show the *actual* transition attempted and its evidence. Acquisition from official sources, DeepWiki, gitingest or gitdiagram-style adapters supplies provenance and topology only. No source extractor selects a processor, declares admissibility, grants a capability or substitutes for an SDK run.

Use the existing SDK ingress manifest with `processing.capability` and `processing.route_id` to select the same published installed route used for internal manifested processing. Pin original wire bytes and manifest digest, exact source commit/version, test input and governing predicate/version. Retain the source-native artifact without rewriting the framework's claim as a StegVerse claim.

Each individual displayed finding MUST include:

1. **Claim vs evidence:** the framework's sourced claim, official source and exact version; separately state which implementation or runtime behavior was independently demonstrated, without attributing reviewer inferences to the framework.
2. **Declared test:** immutable manifested data/test input hash, declared SDK processing capability and route, proposed predecessor → successor state, constraints/predicates and expected outcome. Provider/framework identity never selects the processing route.
3. **Actual admission stage:** `SOURCE_VALIDATION`, `SYNTHETIC_TEST`, `ATTEMPTED_INGRESS`, `ACTUAL_EXECUTION` or `PUBLIC_PUBLICATION`. A stage label alone is NOT a disposition and cannot silently promote to another evidence class.
4. **Disposition for an actual attempted boundary:** `ALLOW`, `DENY`, `FAIL_CLOSED` or another explicitly defined non-ALLOW class; identify producer, actual boundary, failed predicate, exact failure code, missing/conflicting evidence, existing owner, correction and next lawful retry. Non-ALLOW must not commit the refused consequence.
5. **Custody and proof:** exact organization receipt and immediate predecessor reference, Master Records receipt/reconstruction and exact digest match when an authentic governed run occurred. Missing such receipts requires evaluating the preceding *attachment/admission* attempt; NEVER invent an uncalled downstream disposition.
6. **Outcome presented to readers:** what was actually tested, what happened at the tested boundary, what remains untested, and the next specific manifested test. Source-only crosswalks and unperformed runs must not be called empirical successes or framework failures.

The canonical source validator in `StegVerse-Labs/.github/scripts/validate_transition_disposition.py` is the shared proposed contract for transition receipts and external findings; do not duplicate a divergent evaluation policy per framework. Its source CI is not authentic custody. The SDK opt-in local diagnostic reports in PR #327 are likewise **not** InTr or Master Records receipts.

## Public finding projection

| Field | Required content |
| --- | --- |
| Framework / version / official source | Pin source URL, version, retrieval date and any access/licensing conditions |
| Framework claim | Attribute quotation or concise paraphrase; distinguish documented capability from claimed benefit |
| Evidence acquisition | Name and version of optional extractor, exact upstream source/hash; note unreviewed generated diagrams |
| Submitted manifest | Retain wire manifest/digest, route and capability, source artifact identity, original input hash |
| Predecessor → proposed successor | State IDs plus predecessor digest and governing predicate/version |
| Attempted boundary | SDK manifest admission, SDK→InTr attachment, InTr governed transition, or other *actually invoked* step |
| Disposition and reason | Actual producer, defined ALLOW/non-ALLOW, failure code, predicate and immediate consequence |
| Correction/retry | Existing owner, exact missing input or required repair and next admitted entrypoint |
| Chain and reconstruction | Actual receipt IDs/hash, immediate predecessor, Master Records reconstructed digest and comparison |
| Evidentiary scope | Explicit distinction between source review, synthetic test, local SDK diagnosis, authentic execution and publication |

### Missing input is itself an actionable transition attempt

If a necessary external artifact is unavailable, the framework's unexecuted test has **no runtime disposition**. Evaluate the *actual request to acquire or admit that artifact* and give its specific non-ALLOW disposition only if that acquisition/attachment boundary was genuinely evaluated. Keep an exact next attempt while other independent source work proceeds. Do not publish bare `BLOCKED`, `UNKNOWN` or `NOT_OBSERVED` as a terminal finding.

### Compatibility language

Legacy fields such as `execution_authority_claim` may remain stable machine identifiers. Their descriptions should map to specific governance constraints and state-transition dependencies: who supplies inputs, who may claim/fence executable work, which predicate admits a consequence, and which component retains custody. No AI or framework acquires final governance authority from a compatibility rating or receipt.

This is a common projection template for the already-owned 36-framework worker lanes #62–#65 and coordinator #66. It does **not** mark any additional framework complete, publish a runtime result, claim public-anchor activation or change worker ownership.
