#!/usr/bin/env node
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';

const WRITER = 'scripts/write-public-activation-receipt.mjs';
const OUT = 'reports/public-activation-receipt.json';
const REQUIRED_CHECKS = [
  'public_site_loads',
  'governed_llm_demo_overview_reachable',
  'governed_llm_demo_verification_reachable',
  'generated_evaluation_results_reachable'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(WRITER)) fail(`missing writer: ${WRITER}`);

fs.rmSync(OUT, { force: true });
const result = spawnSync(process.execPath, [WRITER], {
  stdio: 'pipe',
  encoding: 'utf8',
  env: {
    ...process.env,
    PAGE_URL: 'https://stegverse-labs.github.io/admissibility-wiki/',
    GITHUB_SHA: 'validator-local-sha',
    GITHUB_RUN_ID: 'validator-local-run',
    GITHUB_RUN_ATTEMPT: '1'
  }
});

if (result.status !== 0) {
  console.error(result.stdout);
  console.error(result.stderr);
  fail('receipt writer exited non-zero');
}

if (!fs.existsSync(OUT)) fail(`writer did not create ${OUT}`);

const receipt = JSON.parse(fs.readFileSync(OUT, 'utf8'));
if (receipt.schema !== 'admissibility_wiki_public_activation_receipt.v1') fail('schema mismatch');
if (receipt.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (receipt.activation_state !== 'workflow_observed_public_routes') fail('activation_state mismatch');
if (receipt.activation_target !== 'https://stegverse-labs.github.io/admissibility-wiki/') fail('activation_target mismatch');
if (receipt.commit !== 'validator-local-sha') fail('commit binding mismatch');
if (receipt.run_id !== 'validator-local-run') fail('run_id binding mismatch');

for (const check of REQUIRED_CHECKS) {
  const value = receipt.checks?.[check];
  if (!value) fail(`missing check: ${check}`);
  if (value.status !== 'verified_by_workflow') fail(`check status mismatch: ${check}`);
  if (!value.evidence?.url) fail(`check evidence url missing: ${check}`);
}

console.log('public activation receipt writer OK');
