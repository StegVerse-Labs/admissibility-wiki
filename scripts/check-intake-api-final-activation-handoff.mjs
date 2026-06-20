#!/usr/bin/env node
import fs from 'node:fs';

const HANDOFF_PATH = 'docs/governance/intake-api-final-activation-handoff.md';

const requiredMarkers = [
  'static_dual_mode_intake_ui: installed',
  'repo_local_durable_backend: installed',
  'local_api_server: installed',
  'authorized_intake_workflow: installed',
  'deploy_config: installed',
  'endpoint_verification_tooling: installed',
  'endpoint_verification_workflow: installed',
  'public_browser_api_endpoint: deploy_pending',
  'Dockerfile.intake-api',
  'render.intake-api.yaml',
  'github/workflows/verify-intake-api-endpoint.yml',
  'runtime_health_check: passed',
  'valid_manifest_submission: passed',
  'receipt_non_claims_present: passed',
  'queue_result_present: passed',
  'malformed_json_rejected: passed',
  'receipt issuance does not accept a proposal',
  'queue placement does not create decision authority',
  'Do not add more intake scaffolding unless a verification result identifies a gap.',
  'deploy runtime -> run endpoint verification -> commit observed receipt -> update public endpoint status'
];

const forbiddenMarkers = [
  'public_browser_api_endpoint: installed',
  'automatic AI review remains installed',
  'automatic decision publication remains installed'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(HANDOFF_PATH)) {
  fail(`missing handoff: ${HANDOFF_PATH}`);
}

const text = fs.readFileSync(HANDOFF_PATH, 'utf8');

for (const marker of requiredMarkers) {
  if (!text.includes(marker)) {
    fail(`missing handoff marker: ${marker}`);
  }
}

for (const marker of forbiddenMarkers) {
  if (text.includes(marker)) {
    fail(`handoff overclaims: ${marker}`);
  }
}

console.log(`OK: ${HANDOFF_PATH}`);
console.log('repo_side_intake_activation=complete_enough_for_handoff');
console.log('public_browser_api_endpoint=deploy_pending');
