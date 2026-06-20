#!/usr/bin/env node
import fs from 'node:fs';

const CONTRACT_PATH = 'docs/governance/proposal-intake-backend-contract.md';

const requiredMarkers = [
  'repo_local_backend: installed',
  'backend_script: scripts/proposal-intake-backend.mjs',
  'durable_candidate_write: installed',
  'durable_receipt_issuance: installed_repo_local',
  'durable_queue_write: installed_repo_local',
  'queue_index_write: installed_repo_local',
  'browser_api_endpoint: not_installed',
  'automatic_ai_review: not_installed',
  'automatic_decision_publication: not_installed',
  'npm run intake:proposal -- fixtures/intake/submission.valid.example.json',
  'static/governance/intake/candidates/',
  'static/governance/intake/receipts/',
  'static/governance/intake/queue/',
  'static/governance/intake/queue/index.json',
  'npm run validate:proposal-intake-runtime',
  'POST /api/wiki/proposals/intake',
  'Request Body',
  'Response Body',
  'receive_request',
  'parse_manifest',
  'validate_manifest_schema',
  'classify_submission_lane',
  'assign_preference_posture',
  'compute_submission_hashes',
  'write_candidate_record',
  'write_queue_record',
  'issue_submission_receipt',
  'Queue placement does not accept a proposal.',
  'AI review must not silently publish glossary changes or decision records.',
  'Only a decision record can accept, deny, defer, escalate, refuse, or supersede a proposal.'
];

const forbiddenClaims = [
  'browser_api_endpoint: installed',
  'automatic_ai_review: installed',
  'automatic_decision_publication: installed',
  'Receipt issuance and queue placement are decision records.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(CONTRACT_PATH)) {
  fail(`missing contract: ${CONTRACT_PATH}`);
}

const text = fs.readFileSync(CONTRACT_PATH, 'utf8');

for (const marker of requiredMarkers) {
  if (!text.includes(marker)) {
    fail(`missing marker: ${marker}`);
  }
}

for (const marker of forbiddenClaims) {
  if (text.includes(marker)) {
    fail(`backend contract overclaims status: ${marker}`);
  }
}

console.log(`OK: ${CONTRACT_PATH}`);
console.log('repo_local_backend=installed');
console.log('browser_api_endpoint=not_installed');
