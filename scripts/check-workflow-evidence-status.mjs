#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/workflow-evidence-status.json';

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

if (status.schema !== 'admissibility_wiki_workflow_evidence_status.v0.1') fail('schema mismatch');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (!['pending_evidence', 'evidence_recorded'].includes(status.status)) fail('invalid status');
if (status.manual_task_requirement !== 'none') fail('manual_task_requirement must be none');
if (status.pending_posture !== 'remain_pending_without_activation_claim') fail('pending posture must avoid activation claim');
if (status.failure_posture !== 'fail_closed_without_public_activation_claim') fail('failure posture must fail closed');
if (!status.latest_checked_commit) fail('latest_checked_commit is required');
if (!status.evidence_target) fail('evidence_target is required');

console.log('workflow evidence status OK');
