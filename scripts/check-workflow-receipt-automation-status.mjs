#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/workflow-receipt-automation-status.json';
const CANONICAL_WORKFLOW = '.github/workflows/validate-chain-continuation.yml';
const REQUIRED_ARTIFACTS = [
  'guardian-destination-status',
  'public-activation-receipt'
];
const REQUIRED_WORKFLOW_MARKERS = [
  'validate-chain-continuation:',
  'build-pages:',
  'deploy-pages:',
  'verify-public-pages:',
  'actions/upload-artifact@v4',
  'actions/deploy-pages@v4',
  'workflow_dispatch',
  "github.event_name == 'push'",
  "github.event_name == 'schedule'",
  "cron: '17 * * * *'",
  'Write public activation receipt',
  'Upload public activation receipt'
];

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);
if (!fs.existsSync(CANONICAL_WORKFLOW)) fail(`missing workflow ${CANONICAL_WORKFLOW}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));
const workflow = fs.readFileSync(CANONICAL_WORKFLOW, 'utf8');

if (status.schema !== 'admissibility_wiki_workflow_receipt_automation_status.v0.1') {
  fail('workflow receipt automation status schema mismatch');
}

if (status.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('workflow receipt automation repository mismatch');
}

if (status.status !== 'installed') {
  fail('workflow receipt automation status must be installed');
}

if (status.workflow_paths?.canonical !== CANONICAL_WORKFLOW) {
  fail('workflow receipt automation must point to the canonical workflow');
}

for (const marker of REQUIRED_WORKFLOW_MARKERS) {
  if (!workflow.includes(marker)) fail(`canonical workflow missing marker ${marker}`);
}

for (const artifact of REQUIRED_ARTIFACTS) {
  if (!Object.values(status.receipt_artifacts || {}).includes(artifact)) {
    fail(`missing receipt artifact declaration ${artifact}`);
  }
}

if (status.manual_task_requirement !== 'none') {
  fail('manual_task_requirement must be none');
}

if (!Array.isArray(status.automation_chain) || status.automation_chain.length < 5) {
  fail('automation_chain must list the validation/deploy/receipt chain');
}

if (!status.automation_chain.includes('scheduled_self_deploy')) {
  fail('automation_chain must include scheduled_self_deploy');
}

if (!status.automation_chain.includes('upload_public_activation_receipt_artifact')) {
  fail('automation_chain must include upload_public_activation_receipt_artifact');
}

console.log('workflow receipt automation status OK');
