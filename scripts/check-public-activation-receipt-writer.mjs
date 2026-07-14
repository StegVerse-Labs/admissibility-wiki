#!/usr/bin/env node
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';

const WRITER = 'scripts/write-public-activation-receipt.mjs';
const OUT = 'reports/public-activation-receipt.json';
const REQUIRED_CHECKS = [
  'public_site_loads',
  'status_json_reachable',
  'ios_workflow_mirror_status_json_reachable',
  'governed_llm_reconstructive_search_reachable',
  'governed_llm_activation_map_reachable',
  'governed_llm_demo_overview_reachable',
  'governed_llm_demo_verification_reachable',
  'governed_llm_site_verification_reachable',
  'governed_llm_deployment_status_reachable',
  'governed_llm_archive_handoff_reachable',
  'optimization_target_doctrine_reachable',
  'optimization_target_formalism_json_reachable',
  'optimization_target_publication_status_reachable',
  'external_translation_reconstruction_receipt_reachable',
  'generated_evaluation_results_reachable',
  'asro_external_framework_reachable'
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
if (receipt.schema !== 'admissibility_wiki_public_activation_receipt.v3') fail('schema mismatch');
if (receipt.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (receipt.activation_state !== 'workflow_observed_guarded_public_routes') fail('activation_state mismatch');
if (receipt.activation_target !== 'https://stegverse-labs.github.io/admissibility-wiki/') fail('activation_target mismatch');
if (receipt.commit !== 'validator-local-sha') fail('commit binding mismatch');
if (receipt.run_id !== 'validator-local-run') fail('run_id binding mismatch');

for (const check of REQUIRED_CHECKS) {
  const value = receipt.checks?.[check];
  if (!value) fail(`missing check: ${check}`);
  if (value.status !== 'verified_by_workflow') fail(`check status mismatch: ${check}`);
  if (!value.evidence?.url) fail(`check evidence url missing: ${check}`);
}

const reconstructionUrl = receipt.linked_receipts?.external_translation_reconstruction;
if (reconstructionUrl !== 'https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json') {
  fail('external translation reconstruction receipt binding mismatch');
}

const nonClaims = receipt.non_claims || [];
if (!nonClaims.some((claim) => claim.includes('does not create provider governance'))) {
  fail('missing provider governance non-claim');
}
if (!nonClaims.some((claim) => claim.includes('does not create external indexing'))) {
  fail('missing external indexing non-claim');
}

console.log('public activation receipt writer OK');
