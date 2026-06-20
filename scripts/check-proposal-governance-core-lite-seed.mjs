#!/usr/bin/env node
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const SEED_ROOT = 'repo-seeds/proposal-governance-core-lite';

const requiredFiles = [
  'README.md',
  'package.json',
  'schemas/proposal-governance-routing.v1.json',
  'schemas/proposal-governance-decision.v1.json',
  'fixtures/post-sandbox-bundle.example.json',
  'fixtures/decision-record.allow-overlap.example.json',
  'scripts/validate-core-lite.mjs',
  'status/proposal-governance-core-lite-status.json'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(SEED_ROOT)) {
  fail(`missing seed root: ${SEED_ROOT}`);
}

for (const file of requiredFiles) {
  const path = `${SEED_ROOT}/${file}`;
  if (!fs.existsSync(path)) {
    fail(`missing seed file: ${path}`);
  }
}

const status = JSON.parse(fs.readFileSync(`${SEED_ROOT}/status/proposal-governance-core-lite-status.json`, 'utf8'));
if (status.repository_target !== 'StegVerse-Labs/proposal-governance-core-lite') {
  fail('seed status target mismatch');
}
if (status.runtime_status !== 'seed_only_not_deployed') {
  fail('seed must not claim deployed runtime');
}
if (status.repo_created !== false) {
  fail('seed must not claim target repo already exists');
}

const output = execFileSync('node', ['scripts/validate-core-lite.mjs'], {
  cwd: SEED_ROOT,
  encoding: 'utf8'
});

if (!output.includes('OK: proposal-governance-core-lite seed')) {
  fail('seed validator did not report OK');
}

console.log(`OK: ${SEED_ROOT}`);
console.log('proposal_governance_core_lite_seed=validated');
console.log('target_repo_status=not_created');
