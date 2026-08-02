# Wiki Publication Pipeline Mirror Handoff

## Goal

Keep the public Admissibility Wiki synchronized with current repository source without converting unrelated semantic-validation failures into a repository-wide publication outage.

## Incident

The public GitHub Pages deployment remained approximately one week behind `main` while new source commits continued to land. The canonical workflow coupled `build-pages` to the success of the entire validation job. Any unrelated fail-closed governance validator therefore skipped site build and deployment, leaving all public pages stale.

Canonical failing run inspected:

```text
run: 30681187876
commit: fc19aafc2f8ae7e249cbea731fa2d16b48fafca6
validation job: failure
build-pages: skipped
deploy-pages: skipped
verify-public-pages: skipped
```

The same run also exposed two direct Docusaurus MDX compilation failures:

```text
docs/formalisms/micro-timescale-human-admissibility.md
docs/research/micro-timescale-human-admissibility-observation-protocol.md
```

A later canonical run exposed a separate deterministic publication blocker:

```text
run: 30741874432
head commit: 42a7745319f90397a9f3e410b920104317d5ae22
validation job: failure at semantic enforcement
build-pages job: 91480938308
failed step: Setup Node
exact error: Dependencies lock file is not found
failed build receipt artifact: 8831589852
deploy-pages: skipped
verify-public-pages: skipped
```

The repository contains `package.json` but no `package-lock.json`, `npm-shrinkwrap.json`, or `yarn.lock`. The workflow nevertheless requested `cache: npm` and used `npm ci`, so publication failed before dependency installation or site compilation.

## Installed repair

```text
f3cfcf4fa872a40ab14fd02724520732cb6bd170
  -> converted display mathematics in the formalism to MDX-safe delimiters

8172dc9d8b08741c446c7716b3749a72a59c61e9
  -> converted display mathematics in the observation protocol to MDX-safe delimiters

79d0d23d849e0ad3c1e1beee77224a56d856d991
  -> decoupled build-pages from unrelated validation-job failure
  -> preserved canonical validation as fail-closed
  -> made governance/preflight checks diagnostic for publication
  -> kept site-build failure blocking deployment
  -> added rendered MindForge attribution verification

88c1bad80c2ab2c385552cc4a5aef2859b303de8
  -> installed a distinct read-only publication observer
  -> runs hourly and by workflow_dispatch
  -> inspects canonical workflow runs, jobs, artifacts, deployment-facing route content, and exact MindForge markers
  -> uploads a machine-readable observation receipt
  -> comments COMPLETE evidence on canonical issue #56
  -> fails closed until every release condition is satisfied

e0b042fa32608dcfc3baf6f8b6fb153886cb46e0
  -> isolated manual canonical runs from later push cancellation
  -> added bounded job timeouts

f0e4801614312a6d1a42139d36713220236948ee
  -> restored publication decoupling after an accidental semantic-validation recoupling
  -> retained manual-run isolation and bounded timeouts

08c51241e5b56bb92875bd2e9a2224727ede4a8f
  -> removed unsupported npm caching without a lockfile
  -> replaced npm ci with npm install --no-audit --no-fund
  -> preserved fail-closed semantic validation, site-build enforcement, deployment gating, and observer ownership
```

## Governing distinction

```text
semantic validator FAIL != hide all current public source
semantic validator FAIL = preserve fail-closed status and receipts
site compilation FAIL = block deployment
site compilation PASS = permit current-source publication
publication != validation success
publication != certification
publication != execution authority
observation workflow != deployment workflow
```

## Canonical ownership and claims

```text
canonical deployment workflow: .github/workflows/validate-chain-continuation.yml
machine-owned observation workflow: .github/workflows/observe-wiki-publication.yml
canonical executable task: issue #56
claim: WIKI-PUB-VALIDATION-2026-08-02
role: CLAIMED_FOR_VALIDATION / MACHINE_OWNED
collision boundary: no second Pages deployment workflow or competing Pages source
```

The observation workflow is intentionally read-only with respect to Pages deployment. It may inspect the canonical workflow and public route, upload receipts, and comment verified evidence on issue #56. It does not deploy, publish, waive validation, or create execution authority.

## Verification target

A successful successor workflow after commit `08c51241e5b56bb92875bd2e9a2224727ede4a8f` must show:

```text
validate-chain-continuation: PASS or FAIL with preserved reports
Setup Node: PASS
Install dependencies: PASS
Build site: PASS
build-pages: PASS
deploy-pages: PASS
verify-public-pages: PASS
```

The MindForge public route must contain both:

```text
Reviewed for architectural boundary semantics
Attribution-Confirmation Participation Loop
```

The observation receipt must be available as:

```text
workflow: Observe wiki publication
artifact: wiki-publication-observation
file: receipt.json
state: COMPLETE
release_condition_satisfied: true
```

## Remaining work and durable owner

All remaining work is assigned to issue #56 and `.github/workflows/observe-wiki-publication.yml`:

1. The observer selects the newest canonical workflow run after repair commit `08c51241e5b56bb92875bd2e9a2224727ede4a8f`.
2. It records the run ID, head SHA, job IDs, job conclusions, and artifact IDs.
3. It verifies `build-pages`, `deploy-pages`, and `verify-public-pages` are successful.
4. It fetches the public MindForge route with a cache-busting query.
5. It verifies both required markers.
6. It uploads `wiki-publication-observation/receipt.json`.
7. When COMPLETE, it comments the run-bound evidence on issue #56.
8. A continuation lane then copies the receipt identifiers into this handoff and `docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md`, releases the claim, and closes issue #56.
9. `MF-NOTICE-001` then becomes an optional human-authority communication action; reviewer silence creates no standing.

## Release and expiration conditions

Release condition:

```text
successor run head_sha >= 08c51241e5b56bb92875bd2e9a2224727ede4a8f
AND Setup Node=success
AND Install dependencies=success
AND Build site=success
AND build-pages=success
AND deploy-pages=success
AND verify-public-pages=success
AND both public markers present
AND receipt identifiers copied into both handoffs
AND issue #56 closed
```

The machine observer runs hourly, so the prior 24-hour chat-owned expiration no longer requires retention of a ChatGPT session. A failed observation remains visible as a failed workflow run plus an uploaded BLOCKED receipt. The next run retries automatically.

## Cross-repository propagation

No Site, Publisher, StegGuardian, or master-records propagation is required for this bounded correction unless a live contract later names the Admissibility Wiki page as an outbound source. No propagation may be claimed without a named source contract and destination receipt.

## Authority boundary

This repair and observation automation change publication availability and observability only. They do not waive, override, reinterpret, or promote any semantic validation result. They grant no certification, endorsement, standing, admissibility, compatibility, publication permission beyond existing repository authority, or execution authority.

## Session consolidation and archive posture

The originating session's unique implementation history, requirements, claims, collision boundaries, unresolved tasks, retry behavior, exact failure evidence, and release conditions are durably transferred to:

```text
docs/WIKI_PUBLICATION_PIPELINE_MIRROR_HANDOFF.md
docs/MINDFORGE_COMMIT_TIME_BOUNDARY_MIRROR_HANDOFF.md
docs/session-consolidation/2026-08-02-mindforge-publication-session.md
.github/workflows/observe-wiki-publication.yml
issue #56
```

The publication task remains active, but it is no longer chat-owned. Continuation is machine-owned and issue-governed. The originating session may be archived without losing execution state.
