---
title: TV/TVC
---

# TV/TVC

TV/TVC refers to the Token Vault and Token Vault Core layer used in StegVerse discussions as an authority and evidence provider.

## Role

TV/TVC should be treated as a provider of governed inputs, not as the whole decision system.

It may provide:

- tokenized authority references;
- evidence references;
- governance boundaries for protected values;
- controlled access references;
- verification material used by downstream decision engines.

## Separation

A concise working separation is:

```text
TV/TVC = authority and evidence provider
CGE    = decision and enforcement manager
Repos  = actors declaring actions
```

## Related Pages

- [StegCGE](./stegcge.md)
- [Governance Boundary](../glossary/governance-boundary.md)
