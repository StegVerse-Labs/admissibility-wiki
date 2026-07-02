#!/usr/bin/env node
import fs from 'node:fs';

const outDir = 'reports';
const outPath = `${outDir}/public-activation-receipt.json`;
const baseUrl = process.env.PAGE_URL || 'https://stegverse-labs.github.io/admissibility-wiki/';
const commit = process.env.GITHUB_SHA || null;
const runId = process.env.GITHUB_RUN_ID || null;
const runAttempt = process.env.GITHUB_RUN_ATTEMPT || null;

const urls = {
  public_site_loads: baseUrl,
  governed_llm_demo_overview_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-overview',
  governed_llm_demo_verification_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-verification',
  generated_evaluation_results_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/evaluation-results'
};

const checks = Object.fromEntries(Object.entries(urls).map(([name, url]) => [
  name,
  {
    status: 'verified_by_workflow',
    evidence: {
      url,
      verifier: 'verify-public-pages job curl --fail with retries'
    }
  }
]));

const receipt = {
  schema: 'admissibility_wiki_public_activation_receipt.v1',
  receipt_id: `public-activation.workflow.${runId || 'unknown'}.${runAttempt || '0'}`,
  created_at: new Date().toISOString(),
  repository: 'StegVerse-Labs/admissibility-wiki',
  activation_target: 'https://stegverse-labs.github.io/admissibility-wiki/',
  activation_state: 'workflow_observed_public_routes',
  commit,
  run_id: runId,
  run_attempt: runAttempt,
  checks,
  non_claims: [
    'This receipt records workflow-observed public route reachability only.',
    'This receipt does not prove admissibility.',
    'This receipt does not grant publication authority.',
    'This receipt does not replace GitHub Pages deployment records.'
  ],
  next_action: 'Archive this receipt with the workflow run artifacts and use it as deployment evidence for the governed LLM public documentation path.'
};

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(receipt, null, 2) + '\n');
console.log(`wrote ${outPath}`);
