#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/no-manual-task-guard-status.json';

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

if (status.schema !== 'admissibility_wiki_no_manual_task_guard_status.v0.1') fail('schema mismatch');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (status.status !== 'installed') fail('status must be installed');
if (status.manual_task_requirement !== 'none') fail('manual_task_requirement must be none');

for (const filePath of status.guarded_files || []) {
  if (!fs.existsSync(filePath)) fail(`missing guarded file ${filePath}`);
  const content = fs.readFileSync(filePath, 'utf8');
  for (const pattern of status.blocked_patterns || []) {
    if (content.includes(pattern)) {
      fail(`${filePath} contains blocked manual-assignment phrase: ${pattern}`);
    }
  }
}

console.log('no manual task assignment guard OK');
