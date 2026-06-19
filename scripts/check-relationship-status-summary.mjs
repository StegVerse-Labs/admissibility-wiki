#!/usr/bin/env node
import fs from 'node:fs';

const SUMMARY_PATH = 'docs/governance/relationship-status-summary.md';

const requiredRecords = [
  'proposal.example.005 / decision.example.005',
  'proposal.example.006 / decision.example.006',
  'proposal.example.007 / decision.example.007',
  'proposal.example.008 / decision.example.008',
  'proposal.example.009 / decision.example.009'
];

const requiredTerms = [
  'ALLOW_AS_OVERLAP',
  'equivalent_status: not accepted',
  'Duplicate Avoidance Rule',
  'Equivalent-Term Boundary',
  'No listed relationship above accepts an equivalent term.',
  'explicit equivalent-status acceptance',
  'GitHub.io project page',
  'activation-checklist reachability'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(SUMMARY_PATH)) {
  fail(`missing relationship status summary: ${SUMMARY_PATH}`);
}

const text = fs.readFileSync(SUMMARY_PATH, 'utf8');

for (const record of requiredRecords) {
  if (!text.includes(record)) {
    fail(`missing relationship record: ${record}`);
  }
}

for (const term of requiredTerms) {
  if (!text.includes(term)) {
    fail(`missing required boundary term: ${term}`);
  }
}

const equivalentAccepted = /equivalent_status:\s*(accepted|true)/i.test(text);
if (equivalentAccepted) {
  fail('relationship summary must not accept equivalent status for records 005-009');
}

const overlapCount = (text.match(/ALLOW_AS_OVERLAP/g) || []).length;
if (overlapCount < 5) {
  fail('expected at least five ALLOW_AS_OVERLAP records');
}

console.log(`OK: ${SUMMARY_PATH}`);
console.log(`accepted_overlap_records=${overlapCount}`);
console.log('equivalent_status=not accepted');
