#!/usr/bin/env node
import fs from 'node:fs';
import { intakeSubmission, IntakeError } from './lib/proposal-intake-core.mjs';

const inputPath = process.argv[2];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!inputPath) {
  fail('usage: node scripts/proposal-intake-backend.mjs <submission.json>');
}

if (!fs.existsSync(inputPath)) {
  fail(`missing input file: ${inputPath}`);
}

try {
  const rawText = fs.readFileSync(inputPath, 'utf8');
  const submission = JSON.parse(rawText);
  const result = intakeSubmission({ submission, rawText });
  console.log(JSON.stringify({
    proposal_id: result.proposal_id,
    receipt_id: result.receipt_id,
    queue_id: result.queue_id,
    candidate_path: result.candidate_path,
    receipt_path: result.receipt_path,
    queue_path: result.queue_path,
    index_path: result.index_path,
    status: result.status
  }, null, 2));
} catch (error) {
  if (error instanceof IntakeError) {
    fail(error.message);
  }
  throw error;
}
