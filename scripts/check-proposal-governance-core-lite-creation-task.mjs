#!/usr/bin/env node
import fs from 'node:fs';

const TASK_PATH = 'docs/governance/proposal-governance-core-lite-creation-task.md';
const STATUS_PATH = 'static/status/proposal-governance-core-lite-seed-status.json';

const taskMarkers = [
  'StegVerse-Labs/proposal-governance-core-lite',
  'repo-seeds/proposal-governance-core-lite/',
  'target_repository_exists: false',
  'seed_status: installed_and_validatable',
  'runtime_status: not_deployed',
  'npm_run_validate_passes_in_target_repo: true',
  'ingestion_cge_return_contract_documented: true',
  'master_records_copy_contract_documented: true',
  'public_display_consequence_contract_documented: true',
  'Do not claim the target repo is active until it exists independently and validates independently.'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function requireFile(path) {
  if (!fs.existsSync(path)) {
    fail(`missing file: ${path}`);
  }
}

requireFile(TASK_PATH);
requireFile(STATUS_PATH);

const taskText = fs.readFileSync(TASK_PATH, 'utf8');
for (const marker of taskMarkers) {
  if (!taskText.includes(marker)) {
    fail(`creation task missing marker: ${marker}`);
  }
}

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));
if (status.target_repository !== 'StegVerse-Labs/proposal-governance-core-lite') {
  fail('target_repository mismatch');
}
if (status.target_repository_exists !== false) {
  fail('target_repository_exists must remain false until verified');
}
if (status.seed_status !== 'installed_and_validatable') {
  fail('seed_status must remain installed_and_validatable');
}
if (status.target_repo_status !== 'not_created') {
  fail('target_repo_status must remain not_created');
}

console.log(`OK: ${TASK_PATH}`);
console.log(`OK: ${STATUS_PATH}`);
console.log('proposal_governance_core_lite_creation_task=external_blocker_recorded');
