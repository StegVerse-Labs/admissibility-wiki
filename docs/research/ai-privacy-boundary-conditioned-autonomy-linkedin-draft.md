# AI Privacy Is a Boundary Problem

## Publication status

```text
state: DRAFT_PRESERVED
publication_authority: false
publication_observed: false
source_session_goal: LinkedIn-level synthesis of frontier LLM privacy-policy analysis
canonical_continuation: master-records/orchestration/docs/session-consolidation/privacy-boundary-sdk-spe-session-inventory.md
```

## Source context

This draft responds to the paper *User Privacy and Large Language Models: An Analysis of Frontier Developers' Privacy Policies* and preserves the session-specific framing that privacy governance must move from disclosure language to enforceable execution boundaries.

The source paper must be independently verified before publication. This repository record preserves the argument and editorial state; it does not assert that every factual claim below has completed publication review.

## LinkedIn draft

**Privacy Policies Won't Govern AI**

A Stanford paper examining frontier LLM developers' privacy policies highlights a familiar pattern: user interactions may be retained, processed, or used to improve models under terms that are difficult for ordinary users to evaluate or control.

The deeper issue is not only disclosure quality.

It is architectural.

Privacy policies are documents. Model-training and data-processing pipelines are systems.

Policies describe what an organization says it will do. Systems determine what can actually happen.

As AI moves from a passive tool into embedded infrastructure, governance cannot remain solely at the disclosure layer. An opt-out mechanism is not equivalent to an enforceable execution boundary.

This is where **boundary-conditioned autonomy** becomes relevant.

Autonomy is not an unlimited property that a system simply possesses. It is a permitted operating mode: enabled under defined conditions, constrained when evidence or authority is missing, and revocable when a boundary is crossed.

For privacy, that means:

- data admissibility is enforced at ingestion;
- training eligibility is mechanically gated;
- retention has enforceable expiry conditions;
- revocation propagates through downstream systems;
- every consequential use produces inspectable evidence;
- missing consent or uncertain authority fails closed.

A checkbox is not a boundary.

A boundary is a condition the system cannot lawfully or mechanically cross merely because the data is available.

The next phase of AI privacy must move from:

- transparency to verifiable constraint;
- disclosure to enforceable data admissibility;
- opt-out language to system-level gating;
- retention promises to testable expiry and deletion controls;
- policy compliance to architectural guarantees.

The decisive question is no longer only whether a privacy policy is clear.

It is whether the system is structurally incapable of using data outside the user's authorized conditions.

Until privacy protection is embedded at ingestion, training, retention, and downstream execution boundaries, autonomy is being governed by documentation rather than design.

And documentation alone does not stop drift.

## Boundary-conditioned autonomy interpretation

```text
policy statement != execution constraint
consent language != admissible data use
opt-out request != propagated revocation
retention promise != enforced expiry
model access != training authority
system capability != permitted autonomy
```

A privacy-preserving system should require a current, inspectable authorization state before each governed transition involving collection, retention, training, retrieval, export, or downstream reuse.

## Remaining editorial work

```text
owner: publication/editorial lane
claim_state: UNCLAIMED
required_before_publication:
  - verify the paper metadata and final wording against the authoritative paper
  - confirm that factual statements remain accurate at publication time
  - choose final LinkedIn character target
  - perform final legal and editorial review
release_condition: a named publication owner records an approved final version and publication receipt
```

This draft grants no publication, legal, admissibility, or execution authority.
