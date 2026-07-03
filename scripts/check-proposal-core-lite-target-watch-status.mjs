#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/proposal-core-lite-target-watch-status.json';
const CANONICAL_WORKFLOW_PATH = '.github/workflows/validate-chain-continuation.yml';
const DECLARED_TASK_PATH = 'static/status/proposal-core-lite-target-watch-status.json';

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);
if (!fs.existsSync(CANONICAL_WORKFLOW_PATH)) fail(`missing ${CANONICAL_WORKFLOW_PATH}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

if (status.schema !== 'proposal_core_lite_target_watch_status.v0.1') fail('schema mismatch');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (status.status !== 'installed') fail('status must be installed');
if (status.workflow_path !== CANONICAL_WORKFLOW_PATH) fail('workflow_path mismatch');
if (status.declared_task_path !== DECLARED_TASK_PATH) fail('declared_task_path mismatch');
if (status.target_repository !== 'StegVerse-Labs/proposal-governance-core-lite') fail('target_repository mismatch');
if (status.artifact_name !== 'proposal-core-lite-target-watch') fail('artifact_name mismatch');
if (status.manual_task_requirement !== 'none') fail('manual_task_requirement must be none');
if (status.pending_posture !== 'remain_pending_without_manual_task_assignment') fail('pending posture must avoid manual task assignment');
if (status.execution_surface !== 'canonical_validate_chain_continuation_workflow') fail('execution_surface must use canonical workflow');

console.log('proposal core-lite target watch status OK');
