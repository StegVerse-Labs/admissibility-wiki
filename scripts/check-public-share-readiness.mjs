#!/usr/bin/env node
import fs from 'node:fs';

const READINESS_PATH = 'docs/governance/public-share-readiness.md';

const requiredMarkers = [
  'share_status: conditionally_ready',
  'recommended_share_mode: invite_feedback_on_wiki_structure_and_terms',
  'not_recommended_as: fully_active_submission_system',
  'Ready To Share For',
  'Not Yet Ready To Claim',
  'active backend proposal submission',
  'durable automatic receipt issuance',
  'automatic proposal queue write',
  'automatic AI review execution',
  'automatic decision publication',
  'GitHub.io project URL configured',
  'Pages source must be GitHub Actions',
  'npm run validate',
  'backend_submission: not_installed',
  'queue_write: not_installed',
  'No equivalent-term relationship has been accepted yet.',
  'Minimum Public Share Checklist',
  'The backend intake system is not active yet'
];

const forbiddenMarkers = [
  'share_status: ready',
  'backend_submission: installed',
  'automatic_ai_review: installed',
  'automatic_decision_publication: installed',
  'custom-domain activation: complete'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(READINESS_PATH)) {
  fail(`missing public readiness page: ${READINESS_PATH}`);
}

const text = fs.readFileSync(READINESS_PATH, 'utf8');

for (const marker of requiredMarkers) {
  if (!text.includes(marker)) {
    fail(`missing readiness marker: ${marker}`);
  }
}

for (const marker of forbiddenMarkers) {
  if (text.includes(marker)) {
    fail(`readiness page overclaims status: ${marker}`);
  }
}

console.log(`OK: ${READINESS_PATH}`);
console.log('share_status=conditionally_ready');
console.log('backend_intake=not_active');
