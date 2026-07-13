# ST-017 Sandbox-First Adoption — Goal 5

## Scope

This packet installs repository-specific isolated validation through the existing PR-visible `Validate chain continuation` workflow without changing the workflow file or its iOS mirror.

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
-> existing check_full_validation_chain.py entry point
-> isolated temporary repository copy
-> generated external-framework prerequisites
-> Goal 5 aggregate validation
-> governance artifact validation
-> Docusaurus build
-> ST-017 structural validation
-> retained sandbox report
-> remaining canonical validation chain
-> main-only capture, replay, build, deploy, and public-verification jobs
```

The exact sandbox report is written to `reports/sandbox-first-validation.report.json`. Its complete JSON payload is embedded as `st017_sandbox` in `reports/full_validation_chain_report.json`, which the existing workflow already uploads as the `full-validation-chain-report` artifact even when validation fails.

This integration preserves the current workflow count and keeps `.github/workflows/validate-chain-continuation.yml` byte-identical to `iosnoperiod/github/workflows/validate-chain-continuation.yml`.

## Authority boundary

Sandbox success does not authorize runtime execution, binary execution, artifact promotion, canonical status mutation, deployment, public verification, release, downstream propagation, compatibility, standing, consequence authority, or admissibility.

Pull requests do not run the main-only OPA capture, fresh-runner replay, Cedar build, Pages build, Pages deployment, or public endpoint verification jobs.

No release tag is authorized.
