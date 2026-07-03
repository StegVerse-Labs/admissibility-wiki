#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const inputPath = process.argv[2];

class IntakeError extends Error {
  constructor(message) {
    super(message);
    this.name = 'IntakeError';
  }
}

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function stableHash(value) {
  const text = typeof value === 'string' ? value : JSON.stringify(value);
  return crypto.createHash('sha256').update(text).digest('hex');
}

function requireObject(value, name) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new IntakeError(`${name} must be an object`);
  }
}

function requireString(value, name) {
  if (!value || typeof value !== 'string') {
    throw new IntakeError(`${name} must be a non-empty string`);
  }
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function readQueueIndex(indexPath) {
  if (!fs.existsSync(indexPath)) {
    return {
      schema: 'admissibility_wiki_proposal_queue_index.v1',
      items: []
    };
  }
  const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
  if (index.schema !== 'admissibility_wiki_proposal_queue_index.v1') {
    throw new IntakeError('queue index schema mismatch');
  }
  if (!Array.isArray(index.items)) {
    throw new IntakeError('queue index items must be an array');
  }
  return index;
}

function intakeSubmission({ submission, rawText }) {
  requireObject(submission, 'submission');
  requireObject(submission.manifest, 'submission.manifest');

  const manifest = submission.manifest;
  if (manifest.schema !== 'admissibility_wiki_submission_manifest.v1') {
    throw new IntakeError('manifest schema mismatch');
  }
  requireString(manifest.submitted_at, 'manifest.submitted_at');
  requireString(manifest.submitter_class, 'manifest.submitter_class');
  requireObject(manifest.target, 'manifest.target');
  requireString(manifest.target.type, 'manifest.target.type');
  requireString(manifest.target.path, 'manifest.target.path');
  requireObject(manifest.proposal, 'manifest.proposal');
  requireString(manifest.proposal.class, 'manifest.proposal.class');
  requireString(manifest.proposal.summary, 'manifest.proposal.summary');
  requireString(manifest.proposal.requested_outcome, 'manifest.proposal.requested_outcome');

  const submittedHash = stableHash(rawText);
  const shortHash = submittedHash.slice(0, 16);
  const proposalId = manifest.proposal_id && manifest.proposal_id !== 'pending'
    ? manifest.proposal_id
    : `proposal-${shortHash}`;
  const receiptId = `receipt-${shortHash}`;
  const queueId = `queue-${shortHash}`;
  const receivedAt = new Date().toISOString();

  const candidatePath = `static/governance/intake/candidates/${proposalId}.json`;
  const receiptPath = `static/governance/intake/receipts/${receiptId}.json`;
  const queuePath = `static/governance/intake/queue/${queueId}.json`;
  const indexPath = 'static/governance/intake/queue/index.json';

  const candidate = {
    schema: 'admissibility_wiki_candidate_submission.v1',
    proposal_id: proposalId,
    received_at: receivedAt,
    status: 'candidate_recorded',
    submission_hash: submittedHash,
    manifest,
    non_claims: [
      'This candidate record does not accept the proposal.',
      'This candidate record does not prove equivalence.',
      'This candidate record does not create commit-time standing.'
    ]
  };

  const receipt = {
    schema: 'admissibility_wiki_submission_receipt.v1',
    receipt_id: receiptId,
    proposal_id: proposalId,
    received_at: receivedAt,
    submission_hash: submittedHash,
    status: 'received_for_queueing',
    non_claims: [
      'This receipt does not accept the proposal.',
      'This receipt does not prove equivalence.',
      'This receipt does not create commit-time standing.',
      'Receipt issuance and queue placement are not decision records.'
    ]
  };

  const queue = {
    schema: 'admissibility_wiki_proposal_queue_record.v1',
    queue_id: queueId,
    proposal_id: proposalId,
    receipt_id: receiptId,
    queued_at: receivedAt,
    status: 'queued_for_review',
    preference_posture: manifest.preferred_triage || 'standard_review',
    target_path: manifest.target.path,
    proposal_class: manifest.proposal.class,
    requested_outcome: manifest.proposal.requested_outcome,
    non_claims: [
      'Queue placement does not accept a proposal.',
      'AI review must not silently publish glossary changes or decision records.',
      'Only a decision record can accept, deny, defer, escalate, refuse, or supersede a proposal.'
    ]
  };

  const index = readQueueIndex(indexPath);
  index.items = index.items.filter((item) => item.queue_id !== queueId);
  index.items.push({
    queue_id: queueId,
    proposal_id: proposalId,
    receipt_id: receiptId,
    queue_path: queuePath,
    status: 'queued_for_review'
  });

  for (const [filePath, record] of [
    [candidatePath, candidate],
    [receiptPath, receipt],
    [queuePath, queue],
    [indexPath, index]
  ]) {
    ensureDir(filePath);
    fs.writeFileSync(filePath, `${JSON.stringify(record, null, 2)}\n`, 'utf8');
  }

  return {
    proposal_id: proposalId,
    receipt_id: receiptId,
    queue_id: queueId,
    candidate_path: candidatePath,
    receipt_path: receiptPath,
    queue_path: queuePath,
    index_path: indexPath,
    status: 'queued_for_review'
  };
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
  console.log(JSON.stringify(result, null, 2));
} catch (error) {
  if (error instanceof IntakeError) {
    fail(error.message);
  }
  throw error;
}
