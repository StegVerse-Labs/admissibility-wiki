# Contributing to the Admissibility Wiki

The Admissibility Wiki is a controlled vocabulary and explanation layer for transition governance, commit-time authority, receipt-bound execution, and governed continuity.

Contributions should improve clarity, precision, source posture, or implementation mapping without turning the wiki into promotional material.

## Done State for a Contribution

A contribution is ready when it:

- defines the concept clearly;
- distinguishes concept from implementation;
- avoids unsupported claims;
- links related terms;
- uses neutral language;
- updates the machine-readable vocabulary when adding or changing a core term;
- passes the Docusaurus build.

## Contribution Types

Accepted contribution types include:

- glossary definitions;
- comparison pages;
- proof-path examples;
- implementation boundary maps;
- activation runbooks;
- ontology updates;
- editorial corrections;
- source posture improvements.

## Editorial Requirements

Every page should state what kind of content it contains:

- concept;
- implementation;
- proof artifact;
- operational runbook;
- essay;
- external comparison;
- proposed future work.

Do not present proposed or experimental work as implemented.

## Machine-Readable Vocabulary Updates

When adding a core term, update:

```text
static/ontology/admissibility-vocabulary.v0.1.json
```

Each term should include:

- `id`;
- `label`;
- `category`;
- `definition`;
- `page`;
- `posture`;
- `related_terms`.

## Pull Request Checklist

Before submitting a pull request, confirm:

```text
npm install
npm run build
```

Then check:

- no broken links;
- no duplicate definitions;
- no unsupported implementation claims;
- no promotional language;
- relevant sidebar entries are updated;
- ontology updates are included when needed.

## Review Standard

Reviewers should ask:

1. Is the term or page useful to the public vocabulary layer?
2. Does it preserve the distinction between admissibility, continuity, auditability, execution, and visibility?
3. Does it avoid claiming that StegVerse has solved more than the current artifacts demonstrate?
4. Does it improve external understanding?

## Style

Write plainly.

Prefer short sections, explicit distinctions, and stable vocabulary over persuasive language.
