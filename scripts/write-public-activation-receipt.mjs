#!/usr/bin/env node
import fs from 'node:fs';

const outDir = 'reports';
const outPath = `${outDir}/public-activation-receipt.json`;
const optimizationReceiptPath = `${outDir}/optimization-target-publication-verification-receipt.json`;
const baseUrl = process.env.PAGE_URL || 'https://stegverse-labs.github.io/admissibility-wiki/';
const commit = process.env.GITHUB_SHA || null;
const runId = process.env.GITHUB_RUN_ID || null;
const runAttempt = process.env.GITHUB_RUN_ATTEMPT || null;

const urls = {
  public_site_loads: baseUrl,
  status_json_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/admissibility-wiki-status.json',
  ios_workflow_mirror_status_json_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/ios-workflow-mirror-status.json',
  governed_llm_reconstructive_search_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-reconstructive-search',
  governed_llm_activation_map_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-activation-map',
  governed_llm_demo_overview_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-overview',
  governed_llm_demo_verification_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-verification',
  governed_llm_site_verification_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-site-verification',
  governed_llm_deployment_status_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-deployment-status',
  governed_llm_archive_handoff_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-archive-handoff',
  optimization_target_doctrine_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit',
  optimization_target_formalism_json_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit.v0.1.json',
  optimization_target_publication_status_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/optimization-target-binding-publication-verification.json',
  generated_evaluation_results_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/evaluation-results',
  asro_external_framework_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/asro'
};

const checks = Object.fromEntries(Object.entries(urls).map(([name, url]) => [
  name,
  {
    status: 'verified_by_workflow',
    evidence: {
      url,
      verifier: name.startsWith('optimization_target_')
        ? 'scripts/check_governed_llm_deployment_status.py run by verify-public-pages'
        : 'verify-public-pages job curl --fail with retries'
    }
  }
]));

let optimizationTargetReceipt = null;
if (fs.existsSync(optimizationReceiptPath)) {
  optimizationTargetReceipt = JSON.parse(fs.readFileSync(optimizationReceiptPath, 'utf8'));
  if (optimizationTargetReceipt.verification_result !== 'PASS') {
    throw new Error('optimization-target publication verification receipt is not PASS');
  }
}

const receipt = {
  schema: 'admissibility_wiki_public_activation_receipt.v3',
  receipt_id: `public-activation.workflow.${runId || 'unknown'}.${runAttempt || '0'}`,
  created_at: new Date().toISOString(),
  repository: 'StegVerse-Labs/admissibility-wiki',
  activation_target: 'https://stegverse-labs.github.io/admissibility-wiki/',
  activation_state: 'workflow_observed_guarded_public_routes',
  commit,
  run_id: runId,
  run_attempt: runAttempt,
  checks,
  linked_receipts: {
    optimization_target_publication_verification: optimizationTargetReceipt
      ? optimizationReceiptPath
      : null
  },
  authority_granted: false,
  release_authority_granted: false,
  downstream_mutation_authority_granted: false,
  non_claims: [
    'This receipt records workflow-observed public route reachability only.',
    'This receipt does not prove admissibility.',
    'This receipt does not grant publication authority.',
    'This receipt does not create provider governance.',
    'This receipt does not create external indexing.',
    'This receipt does not replace GitHub Pages deployment records.'
  ],
  next_action: 'Archive this receipt and its linked optimization-target verification receipt with the workflow run artifacts; use them only as bounded deployment evidence.'
};

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(receipt, null, 2) + '\n');
console.log(`wrote ${outPath}`);
