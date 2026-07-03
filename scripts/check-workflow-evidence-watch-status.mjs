#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/workflow-evidence-watch-status.json';
const WORKFLOW_PATH = '.github/workflows/validate-chain-continuation.yml';

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);
if (!fs.existsSync(WORKFLOW_PATH)) fail(`missing ${WORKFLOW_PATH}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));
const workflow = fs.readFileSync(WORKFLOW_PATH, 'utf8');

if (status.schema !== 'admissibility_wiki_workflow_evidence_watch_status.v0.1') fail('schema mismatch');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (status.status !== 'installed') fail('status must be installed');
if (status.workflow_path !== WORKFLOW_PATH) fail('workflow_path mismatch');
if (status.artifact_name !== 'public-activation-receipt') fail('artifact_name mismatch');
if (status.manual_task_requirement !== 'none') fail('manual_task_requirement must be none');
if (status.activation_claim !== 'not_advanced_by_this_watch') fail('watcher must not advance activation claim');
if (status.failure_posture !== 'fail_closed_without_public_activation_claim') fail('failure posture must fail closed');
if (!workflow.includes('verify-public-pages:')) fail('canonical workflow missing verify-public-pages job');
if (!workflow.includes('public-activation-receipt')) fail('canonical workflow missing public activation receipt artifact');

console.log('workflow evidence watcher status OK');
