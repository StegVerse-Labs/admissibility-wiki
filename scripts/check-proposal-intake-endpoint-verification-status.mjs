#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/proposal-intake-endpoint-verification-status.json';

const requiredFields = [
  'schema',
  'generated_at',
  'repository',
  'verifier',
  'verification_workflow',
  'expected_endpoint_path',
  'expected_health_path',
  'observed_receipt_path',
  'verification_status',
  'public_endpoint_status',
  'required_evidence',
  'non_claims',
  'next_action'
];

const requiredEvidence = [
  'runtime_health_check',
  'valid_manifest_submission',
  'receipt_non_claims_present',
  'queue_result_present',
  'malformed_json_rejected'
];

const requiredNonClaims = [
  'Verification tooling does not prove the public endpoint is deployed.',
  'Verification tooling does not accept proposals.',
  'Verification tooling does not create decision authority.',
  'Verification tooling does not install automatic AI review or decision publication.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) {
  fail(`missing status: ${STATUS_PATH}`);
}

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

for (const field of requiredFields) {
  if (!(field in status)) {
    fail(`missing field: ${field}`);
  }
}

if (status.schema !== 'admissibility_wiki_proposal_intake_endpoint_verification_status.v1') {
  fail('unexpected schema');
}
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('unexpected repository');
}
if (status.verifier !== 'scripts/verify-proposal-intake-public-endpoint.mjs') {
  fail('unexpected verifier path');
}
if (status.verification_workflow !== '.github/workflows/verify-intake-api-endpoint.yml') {
  fail('unexpected verification workflow path');
}
if (status.public_endpoint_status !== 'deploy_pending') {
  fail('public_endpoint_status must remain deploy_pending until evidence is recorded');
}

for (const evidence of requiredEvidence) {
  if (!status.required_evidence.includes(evidence)) {
    fail(`missing required evidence: ${evidence}`);
  }
}
for (const claim of requiredNonClaims) {
  if (!status.non_claims.includes(claim)) {
    fail(`missing non-claim: ${claim}`);
  }
}

console.log(`OK: ${STATUS_PATH}`);
console.log('verification_status=ready_for_external_runtime');
console.log('public_endpoint_status=deploy_pending');
