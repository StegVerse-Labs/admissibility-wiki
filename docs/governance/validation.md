---
title: Validation
---

# Validation

The Admissibility Wiki uses automated validation to protect the public vocabulary layer from broken builds and malformed ontology changes.

## Done State

Validation is healthy when:

- the ontology JSON parses successfully;
- every ontology term has required fields;
- every ontology term uses an allowed maturity posture;
- term IDs are unique;
- the Docusaurus site builds successfully;
- GitHub Actions reports a passing validation workflow.

## Local Commands

Run ontology validation only:

```bash
npm run validate:ontology
```

Run ontology validation and the Docusaurus build:

```bash
npm run validate
```

## Workflow

The workflow lives at:

```text
.github/workflows/validate.yml
```

It runs on:

- pull requests to `main`;
- pushes to `main`;
- manual workflow dispatch.

## Ontology Rules

The validator checks:

- root fields exist;
- `terms` is an array;
- term fields exist;
- term IDs use lowercase letters, numbers, and underscores;
- term IDs are unique;
- page paths start with `/`;
- posture values are allowed;
- related terms are arrays.

## Allowed Postures

```text
conceptual
implemented
experimental
proposed
external
```

## Failure Handling

If ontology validation fails:

1. Open the failed Actions run.
2. Read the listed validation error.
3. Update `static/ontology/admissibility-vocabulary.v0.1.json`.
4. Re-run validation.

If Docusaurus build fails:

1. Check for broken links.
2. Check sidebar references.
3. Check front matter.
4. Check Markdown syntax.
5. Re-run the workflow after correction.
