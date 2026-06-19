#!/usr/bin/env node
import fs from 'node:fs';

const GLOSSARY_PAGES = [
  'docs/glossary/admissibility.md',
  'docs/glossary/transition.md',
  'docs/glossary/authority-class.md',
  'docs/glossary/policy-reference.md',
  'docs/glossary/evidence-posture.md',
  'docs/glossary/review-posture.md',
  'docs/glossary/drift.md',
  'docs/glossary/commit-time-authority.md',
  'docs/glossary/commit-time-validity.md',
  'docs/glossary/receipt-bound-execution.md',
  'docs/glossary/governance-boundary.md',
  'docs/glossary/reconstructability.md'
];

const REQUIRED_MARKERS = [
  '## Transition Origin',
  'Transition Table Elements:',
  'Transition Blocks:',
  'Derived From:',
  'Standing:',
  'Authority Source:',
  'Commit-Time Relevance:',
  'Reconstructability Relevance:'
];

let missingPages = [];

for (const page of GLOSSARY_PAGES) {
  if (!fs.existsSync(page)) {
    console.error(`FAIL: missing glossary page: ${page}`);
    process.exit(1);
  }

  const text = fs.readFileSync(page, 'utf8');
  const missingMarkers = REQUIRED_MARKERS.filter((marker) => !text.includes(marker));

  if (missingMarkers.length > 0) {
    missingPages.push({ page, missingMarkers });
  }
}

if (missingPages.length > 0) {
  console.log('WARN: transition origin migration is incomplete.');
  for (const entry of missingPages) {
    console.log(`- ${entry.page}`);
    for (const marker of entry.missingMarkers) {
      console.log(`  missing: ${marker}`);
    }
  }
  console.log('status=advisory_only');
  process.exit(0);
}

console.log('OK: all tracked glossary pages include Transition Origin sections.');
