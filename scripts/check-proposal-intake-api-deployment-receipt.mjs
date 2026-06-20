#!/usr/bin/env node
import fs from 'node:fs';

const RECEIPT_PATH = 'static/status/proposal-intake-api-deployment-receipt.example.json';

const requiredTopLevel = [
  'schema',
  'receipt_id',
  'generated_at',
  'repository',
  'deployment_state',
  'local_api_status',
  'public_endpoint_status',
  'expected_public_route',
  'required_verification_checks',
  'non_claims',
  'next_action'
];

const requiredChecks = [
  'runtime_health_check',
  'valid_manifest_submission',
  'durable_candidate_written',
  'durable_receipt_written',
  'durable_queue_record_written',
  'queue_index_written',
  'malformed_json_rejected',
  'no_decision_record_created_by_intake'
];

const requiredNonClaims = [
  'This receipt example does not prove the public endpoint is deployed.',
  'This receipt example does not accept any proposal.',
  'This receipt example does not create decision authority.',
  'This receipt example does not install automatic AI review or decision publication.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(RECEIPT_PATH)) {
  fail(`missing receipt: ${RECEIPT_PATH}`);
}

const receipt = JSON.parse(fs.readFileSync(RECEIPT_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in receipt)) {
    fail(`missing field: ${field}`);
  }
}

if (receipt.schema !== 'admissibility_wiki_proposal_intake_api_deployment_receipt.v1') {
  fail('unexpected schema');
}
if (receipt.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('unexpected repository');
}
if (receipt.deployment_state !== 'pending_external_runtime') {
  fail('deployment_state must remain pending_external_runtime for example receipt');
}
if (receipt.public_endpoint_status !== 'deploy_pending') {
  fail('public_endpoint_status must remain deploy_pending for example receipt');
}
if (receipt.expected_public_route !== 'POST /api/wiki/proposals/intake') {
  fail('expected_public_route mismatch');
}

if (!Array.isArray(receipt.required_verification_checks)) {
  fail('required_verification_checks must be an array');
}
const checkIds = new Set(receipt.required_verification_checks.map((check) => check.check_id));
for (const check of requiredChecks) {
  if (!checkIds.has(check)) {
    fail(`missing verification check: ${check}`);
  }
}

for (const check of receipt.required_verification_checks) {
  if (check.status !== 'pending') {
    fail(`example verification check must remain pending: ${check.check_id}`);
  }
  if (check.evidence !== null) {
    fail(`example verification evidence must remain null: ${check.check_id}`);
  }
}

if (!Array.isArray(receipt.non_claims)) {
  fail('non_claims must be an array');
}
for (const claim of requiredNonClaims) {
  if (!receipt.non_claims.includes(claim)) {
    fail(`missing non-claim: ${claim}`);
  }
}

console.log(`OK: ${RECEIPT_PATH}`);
console.log('public_endpoint_status=deploy_pending');
console.log(`verification_checks=${receipt.required_verification_checks.length}`);
