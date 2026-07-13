# ST-017 Sandbox-First Adoption — Goal 5

## Scope

This packet installs repository-specific isolated validation inside the existing `Validate chain continuation` workflow and its iOS mirror.

```text
repository: StegVerse-Labs/admissibility-wiki
issue: #11
workflow: .github/workflows/validate-chain-continuation.yml
ios_mirror: iosnoperiod/github/workflows/validate-chain-continuation.yml
SANDBOX: NOT_RUN
GITHUB_ACTIONS: NOT_OBSERVED
PUBLIC_OUTPUT: NOT_VERIFIED
```

## Required order

```text
proposed change
-> isolated temporary repository copy
-> generated external-framework prerequisites
-> Goal 5 aggregate validation
-> governance artifact validation
-> Docusaurus build
-> ST-017 structural validation
-> retained sandbox report
-> existing canonical validation chain
-> main-only capture, replay, build, deploy, and public-verification jobs
```

The sandbox report is `reports/sandbox-first-validation.report.json` and is uploaded as `admissibility-wiki-st017-sandbox-report` even when a command fails.

## Authority boundary

Sandbox success does not authorize runtime execution, binary execution, artifact promotion, canonical status mutation, deployment, public verification, release, downstream propagation, compatibility, standing, consequence authority, or admissibility.

Pull requests do not run the main-only OPA capture, fresh-runner replay, Cedar build, Pages build, Pages deployment, or public endpoint verification jobs.

No release tag is authorized.
