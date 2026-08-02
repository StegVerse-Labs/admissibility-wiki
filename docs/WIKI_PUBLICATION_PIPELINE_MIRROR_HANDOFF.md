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
```

## Verification target

A successful successor workflow must show:

```text
validate-chain-continuation: PASS or FAIL with preserved reports
build-pages: PASS
deploy-pages: PASS
verify-public-pages: PASS
```

The MindForge public route must contain both:

```text
Reviewed for architectural boundary semantics
Attribution-Confirmation Participation Loop
```

## Remaining work

1. Observe the workflow triggered by commit `79d0d23d849e0ad3c1e1beee77224a56d856d991` or its successor.
2. Inspect build logs if `build-pages` fails.
3. Confirm a new GitHub Pages deployment timestamp.
4. Confirm the rendered MindForge page contains the authorized statement and participation-loop section.
5. Update publication receipts and the MindForge handoff with run-bound evidence.

## Authority boundary

This repair changes publication availability only. It does not waive, override, reinterpret, or promote any semantic validation result. It grants no certification, endorsement, standing, admissibility, compatibility, or execution authority.

## Archive posture

This thread is not ready for archiving until a successor run proves build, deployment, and rendered-route verification or the remaining failure is durably transferred with exact run and job evidence.
