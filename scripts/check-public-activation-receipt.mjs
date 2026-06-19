#!/usr/bin/env node
import fs from 'node:fs';

const RECEIPT_PATH = 'static/status/public-activation-receipt.example.json';

const requiredTopLevel = [
  'schema',
  'receipt_id',
  'created_at',
  'repository',
  'activation_target',
  'activation_state',
  'checks',
  'non_claims',
  'next_action'
];

const requiredChecks = [
  'public_site_loads',
  'dns_resolves',
  'https_valid',
  'ontology_json_reachable',
  'status_json_reachable',
  'governance_records_reachable',
  'public_navigation_works'
];

const requiredNonClaims = [
  'This receipt does not activate the site.',
  'This receipt does not prove admissibility.',
  'This receipt does not grant publication authority.',
  'This receipt is an example template until real evidence replaces pending values.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(RECEIPT_PATH)) {
  fail(`missing activation receipt: ${RECEIPT_PATH}`);
}

const receipt = JSON.parse(fs.readFileSync(RECEIPT_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in receipt)) {
    fail(`missing top-level field: ${field}`);
  }
}

if (receipt.schema !== 'admissibility_wiki_public_activation_receipt.v1') {
  fail('unexpected schema');
}

if (receipt.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('repository must be StegVerse-Labs/admissibility-wiki');
}

if (receipt.activation_target !== 'admissibility.stegverse.org') {
  fail('activation_target must be admissibility.stegverse.org');
}

if (receipt.activation_state !== 'pending_external_verification') {
  fail('example receipt must remain pending_external_verification');
}

if (!receipt.checks || typeof receipt.checks !== 'object' || Array.isArray(receipt.checks)) {
  fail('checks must be an object');
}

for (const check of requiredChecks) {
  const value = receipt.checks[check];
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    fail(`missing check object: ${check}`);
  }
  if (value.status !== 'pending') {
    fail(`example check must remain pending: ${check}`);
  }
  if (value.evidence !== null) {
    fail(`example evidence must remain null until real verification: ${check}`);
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
console.log(`checks=${requiredChecks.length}`);
console.log(`activation_state=${receipt.activation_state}`);
