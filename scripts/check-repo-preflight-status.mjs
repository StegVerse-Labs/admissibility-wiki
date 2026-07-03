#!/usr/bin/env node
import fs from 'node:fs';

const STATUS_PATH = 'static/status/repo-preflight-status.json';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(STATUS_PATH)) fail(`missing ${STATUS_PATH}`);
const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));

if (status.schema !== 'stegverse_repo_preflight_status.v0.1') fail('schema mismatch');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (!['PASS', 'WARN', 'FAIL'].includes(status.status)) fail('bad status');
if (!status.summary || typeof status.summary !== 'object') fail('summary missing');
for (const key of ['pass', 'warn', 'fail', 'skip']) {
  if (!Number.isInteger(status.summary[key]) || status.summary[key] < 0) fail(`bad summary ${key}`);
}
if (!Array.isArray(status.findings) || status.findings.length === 0) fail('findings missing');
if (!Array.isArray(status.non_claims) || status.non_claims.length === 0) fail('non_claims missing');

for (const finding of status.findings) {
  if (!['PASS', 'WARN', 'FAIL', 'SKIP'].includes(finding.class)) fail('bad finding class');
  if (!finding.category) fail('finding category missing');
  if (!finding.message) fail('finding message missing');
}

for (const requiredCategory of [
  'handoff_state',
  'workflow_policy',
  'governance_validation',
  'status_artifact_state',
  'generated_artifact_state',
  'render_build'
]) {
  if (!status.findings.some((finding) => finding.category === requiredCategory)) {
    fail(`missing category: ${requiredCategory}`);
  }
}

for (const required of [
  'Preflight does not replace release readiness.',
  'Preflight does not authorize deployment.',
  'Preflight does not prove runtime admissibility.'
]) {
  if (!status.non_claims.includes(required)) fail(`missing non_claim: ${required}`);
}

console.log('repo preflight status OK');
