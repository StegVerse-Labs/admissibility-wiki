#!/usr/bin/env node
import fs from 'node:fs';

const DEPLOYMENT_PATH = 'docs/governance/proposal-intake-api-deployment.md';

const requiredMarkers = [
  'local_api_server: installed',
  'local_api_route: POST /api/wiki/proposals/intake',
  'static_intake_page_can_submit_to_configured_endpoint: installed',
  'deploy_config: installed',
  'public_browser_api_endpoint: deploy_pending',
  'automatic_ai_review: not_installed',
  'automatic_decision_publication: not_installed',
  'npm run intake:api',
  'http://127.0.0.1:8787/api/wiki/proposals/intake',
  'http://127.0.0.1:8787/health',
  'Dockerfile.intake-api',
  'render.intake-api.yaml',
  'scripts/check-intake-api-deploy-config.mjs',
  'node scripts/check-intake-api-deploy-config.mjs',
  'INTAKE_OUTPUT_ROOT=static/governance/intake',
  'MAX_BODY_BYTES=256000',
  'The GitHub.io static site itself does not provide server execution.',
  'candidate submission',
  'submission receipt',
  'queue record',
  'queue index',
  'Only a decision record can do that.',
  'Validate deployment configuration.',
  'Confirm no decision record is created by intake.'
];

const forbiddenMarkers = [
  'public_browser_api_endpoint: installed',
  'automatic_ai_review: installed',
  'automatic_decision_publication: installed',
  'automatic_ontology_mutation: installed'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(DEPLOYMENT_PATH)) {
  fail(`missing deployment guide: ${DEPLOYMENT_PATH}`);
}

const text = fs.readFileSync(DEPLOYMENT_PATH, 'utf8');

for (const marker of requiredMarkers) {
  if (!text.includes(marker)) {
    fail(`missing deployment marker: ${marker}`);
  }
}

for (const marker of forbiddenMarkers) {
  if (text.includes(marker)) {
    fail(`deployment guide overclaims: ${marker}`);
  }
}

console.log(`OK: ${DEPLOYMENT_PATH}`);
console.log('deploy_config=installed');
console.log('public_browser_api_endpoint=deploy_pending');
