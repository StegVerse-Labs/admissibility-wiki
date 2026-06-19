#!/usr/bin/env node
import fs from 'node:fs';

const TEMPLATE_PATH = 'docs/governance/equivalence-proposal-template.md';

const requiredTerms = [
  'relationship_claim',
  'equivalent | overlapping | adjacent | broader | narrower | contradictory | unresolved',
  'review_posture',
  'Evidence Requirements',
  'Claim Comparison',
  'Mismatch Section',
  'Risk Of Overclaiming',
  'Proposed Glossary Placement',
  'Required Decision Record',
  'Validation Checklist',
  'does not by itself',
  'create admissibility standing',
  'replace executable formalism tests'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(TEMPLATE_PATH)) {
  fail(`missing template: ${TEMPLATE_PATH}`);
}

const text = fs.readFileSync(TEMPLATE_PATH, 'utf8');

for (const term of requiredTerms) {
  if (!text.includes(term)) {
    fail(`missing required term: ${term}`);
  }
}

const checklistCount = (text.match(/^- \[ \]/gm) || []).length;
if (checklistCount < 6) {
  fail('template must include at least six checklist items');
}

console.log(`OK: ${TEMPLATE_PATH}`);
console.log(`checklist_items=${checklistCount}`);
