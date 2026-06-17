const sidebars = {
  tutorialSidebar: [
    'index',
    {
      type: 'category',
      label: 'Activation',
      items: [
        'activation/github-pages-cloudflare',
      ],
    },
    {
      type: 'category',
      label: 'Governance',
      items: [
        'governance/editorial-policy',
        'governance/page-template',
        'governance/validation',
      ],
    },
    {
      type: 'category',
      label: 'Glossary',
      items: [
        'glossary/admissibility',
        'glossary/transition',
        'glossary/authority-class',
        'glossary/policy-reference',
        'glossary/evidence-posture',
        'glossary/review-posture',
        'glossary/drift',
        'glossary/commit-time-authority',
        'glossary/commit-time-validity',
        'glossary/receipt-bound-execution',
        'glossary/governance-boundary',
        'glossary/reconstructability',
      ],
    },
    {
      type: 'category',
      label: 'StegVerse',
      items: [
        'stegverse/stegcore',
        'stegverse/stegcge',
        'stegverse/tv-tvc',
        'stegverse/transition-table',
      ],
    },
    {
      type: 'category',
      label: 'Comparisons',
      items: [
        'comparisons/admissibility-vs-continuity',
        'comparisons/approval-vs-execution',
        'comparisons/visibility-vs-governance',
        'comparisons/auditability-vs-admissibility',
      ],
    },
    {
      type: 'category',
      label: 'Proof Path',
      items: [
        'proof-path/minimal-public-proof-path',
        'proof-path/transition-cell-example',
        'proof-path/receipt-example',
        'proof-path/replay-example',
      ],
    },
    {
      type: 'category',
      label: 'Ontology',
      items: [
        'ontology/machine-readable-vocabulary',
      ],
    },
    {
      type: 'category',
      label: 'Essays',
      items: [
        'essays/why-admissibility-matters',
        'essays/consequence-standing',
      ],
    },
  ],
};

export default sidebars;
