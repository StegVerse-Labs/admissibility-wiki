#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/workflow-receipt-automation-status.json';
const REQUIRED_WORKFLOWS = [
  '.github/workflows/deploy.yml',
  '.github/workflows/record-latest-success.yml'
];
const REQUIRED_ARTIFACTS = [
  'admissibility-wiki-workflow-failure',
  'admissibility-wiki-workflow-success'
];

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

if (status.schema !== 'admissibility_wiki_workflow_receipt_automation_status.v0.1') {
  fail('workflow receipt automation status schema mismatch');
}

if (status.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('workflow receipt automation repository mismatch');
}

if (status.status !== 'installed') {
  fail('workflow receipt automation status must be installed');
}

for (const workflowPath of REQUIRED_WORKFLOWS) {
  if (!fs.existsSync(workflowPath)) fail(`missing workflow ${workflowPath}`);
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

console.log('workflow receipt automation status OK');
