# Admissibility Wiki

The Admissibility Wiki is the public vocabulary layer for transition governance, commit-time authority, receipt-bound execution, and governed continuity.

This repository is a Docusaurus-ready knowledge base for StegVerse concepts, formal vocabulary, comparison pages, and minimal public proof paths.

## Purpose

This wiki exists to make the StegVerse governance vocabulary visible, stable, linkable, and reviewable without requiring Wikipedia approval first.

It is not a substitute for Wikipedia and does not claim independent notability by itself. It is a public reference layer that can help researchers, developers, reviewers, journalists, and contributors understand the concepts accurately.

## Done State

This repository is considered initially established when it has:

- a publishable Docusaurus configuration;
- a core glossary;
- StegVerse implementation mapping pages;
- comparison pages that explain common governance distinctions;
- a minimal public proof path;
- essays suitable for public linking;
- version-controlled Markdown pages that can be cited, reviewed, and expanded.

## Local Development

```bash
npm install
npm run start
```

## Build

```bash
npm run build
```

## Deploy

This repository includes a GitHub Pages workflow at `.github/workflows/deploy.yml`.

Before enabling deployment, configure GitHub Pages to use **GitHub Actions** as the source.

## Site Structure

```text
docs/
  glossary/
  stegverse/
  comparisons/
  proof-path/
  essays/
```

## Editorial Standard

Pages should be:

- neutral;
- source-aware;
- distinction-focused;
- version-controlled;
- careful not to overclaim;
- clear about whether a claim is conceptual, implemented, experimental, or proposed.

## Relationship to StegVerse

StegVerse is the originating ecosystem. The Admissibility Wiki is the public vocabulary and explanation layer.

The goal is not to make every StegVerse artifact promotional. The goal is to define the language of admissible transition governance clearly enough that others can evaluate, compare, critique, reuse, or extend it.
