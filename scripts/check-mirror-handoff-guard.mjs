#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/mirror-handoff-guard-status.json';

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

if (status.schema !== 'admissibility_wiki_mirror_handoff_guard_status.v0.1') fail('schema mismatch');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (status.status !== 'installed') fail('status must be installed');
if (status.manual_task_requirement !== 'none') fail('manual_task_requirement must be none');

const handoffPath = status.handoff_path;
if (!handoffPath || !fs.existsSync(handoffPath)) fail(`missing handoff ${handoffPath}`);

const handoff = fs.readFileSync(handoffPath, 'utf8');

for (const section of status.required_sections || []) {
  if (!handoff.includes(section)) fail(`handoff missing required section: ${section}`);
}

for (const phrase of status.required_phrases || []) {
  if (!handoff.includes(phrase)) fail(`handoff missing required phrase: ${phrase}`);
}

const addendumPath = status.addendum_path;
if (!addendumPath || !fs.existsSync(addendumPath)) fail(`missing handoff addendum ${addendumPath}`);

const addendum = fs.readFileSync(addendumPath, 'utf8');

for (const phrase of status.required_addendum_phrases || []) {
  if (!addendum.includes(phrase)) fail(`handoff addendum missing required phrase: ${phrase}`);
}

console.log('mirror handoff guard OK');
