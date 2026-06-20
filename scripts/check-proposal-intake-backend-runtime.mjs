#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const SCRIPT_PATH = 'scripts/proposal-intake-backend.mjs';
const FIXTURE_PATH = 'fixtures/intake/submission.valid.example.json';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(SCRIPT_PATH)) {
  fail(`missing backend script: ${SCRIPT_PATH}`);
}

if (!fs.existsSync(FIXTURE_PATH)) {
  fail(`missing fixture: ${FIXTURE_PATH}`);
}

const repoRoot = process.cwd();
const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'admissibility-intake-'));

try {
  fs.mkdirSync(path.join(tmpRoot, 'scripts'), { recursive: true });
  fs.mkdirSync(path.join(tmpRoot, 'fixtures/intake'), { recursive: true });
  fs.copyFileSync(path.join(repoRoot, SCRIPT_PATH), path.join(tmpRoot, SCRIPT_PATH));
  fs.copyFileSync(path.join(repoRoot, FIXTURE_PATH), path.join(tmpRoot, FIXTURE_PATH));

  const output = execFileSync('node', [SCRIPT_PATH, FIXTURE_PATH], {
    cwd: tmpRoot,
    encoding: 'utf8'
  });

  const result = JSON.parse(output);
  const requiredOutputFields = [
    'proposal_id',
    'receipt_id',
    'queue_id',
    'candidate_path',
    'receipt_path',
    'queue_path',
    'index_path',
    'status'
  ];

  for (const field of requiredOutputFields) {
    if (!(field in result)) {
      fail(`runtime result missing field: ${field}`);
    }
  }

  if (result.status !== 'queued_for_review') {
    fail('runtime status must be queued_for_review');
  }

  const candidate = JSON.parse(fs.readFileSync(path.join(tmpRoot, result.candidate_path), 'utf8'));
  const receipt = JSON.parse(fs.readFileSync(path.join(tmpRoot, result.receipt_path), 'utf8'));
  const queue = JSON.parse(fs.readFileSync(path.join(tmpRoot, result.queue_path), 'utf8'));
  const index = JSON.parse(fs.readFileSync(path.join(tmpRoot, result.index_path), 'utf8'));

  if (candidate.schema !== 'admissibility_wiki_candidate_submission.v1') {
    fail('candidate schema mismatch');
  }
  if (receipt.schema !== 'admissibility_wiki_submission_receipt.v1') {
    fail('receipt schema mismatch');
  }
  if (queue.schema !== 'admissibility_wiki_proposal_queue_record.v1') {
    fail('queue schema mismatch');
  }
  if (index.schema !== 'admissibility_wiki_proposal_queue_index.v1') {
    fail('queue index schema mismatch');
  }

  if (receipt.non_claims.some((claim) => claim.includes('accepts the proposal') && !claim.includes('does not'))) {
    fail('receipt must not accept proposal');
  }

  if (queue.status !== 'queued_for_review') {
    fail('queue record must be queued_for_review');
  }

  if (!Array.isArray(index.items) || index.items.length !== 1) {
    fail('queue index must contain exactly one item for runtime fixture');
  }

  console.log('OK: proposal intake backend runtime');
  console.log(`proposal_id=${result.proposal_id}`);
  console.log(`receipt_id=${result.receipt_id}`);
  console.log(`queue_id=${result.queue_id}`);
} finally {
  fs.rmSync(tmpRoot, { recursive: true, force: true });
}
