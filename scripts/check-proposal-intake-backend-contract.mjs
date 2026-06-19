#!/usr/bin/env node
import fs from 'node:fs';

const CONTRACT_PATH = 'docs/governance/proposal-intake-backend-contract.md';

const requiredMarkers = [
  'backend_submission: not_installed',
  'durable_receipt_issuance: not_installed',
  'queue_write: not_installed',
  'automatic_ai_review: not_installed',
  'automatic_decision_publication: not_installed',
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
  'return_receipt_response',
  'Queue placement does not accept a proposal.',
  'AI review must not silently publish glossary changes or decision records.',
  'Only a decision record can accept, deny, defer, escalate, refuse, or supersede a proposal.'
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

const forbiddenActiveClaims = [
  'backend_submission: installed',
  'durable_receipt_issuance: installed',
  'queue_write: installed',
  'automatic_ai_review: installed',
  'automatic_decision_publication: installed'
];

for (const marker of forbiddenActiveClaims) {
  if (text.includes(marker)) {
    fail(`backend contract must not claim active status: ${marker}`);
  }
}

console.log(`OK: ${CONTRACT_PATH}`);
console.log('backend_contract=specified_not_active');
