#!/usr/bin/env node
import http from 'node:http';
import { intakeSubmission, IntakeError } from './lib/proposal-intake-core.mjs';

const PORT = Number(process.env.PORT || 8787);
const HOST = process.env.HOST || '127.0.0.1';
const OUTPUT_ROOT = process.env.INTAKE_OUTPUT_ROOT || 'static/governance/intake';
const MAX_BODY_BYTES = Number(process.env.MAX_BODY_BYTES || 256_000);

function sendJson(res, status, body) {
  const payload = JSON.stringify(body, null, 2);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'POST, OPTIONS',
    'access-control-allow-headers': 'content-type'
  });
  res.end(payload);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    let body = '';
    req.setEncoding('utf8');
    req.on('data', (chunk) => {
      size += Buffer.byteLength(chunk);
      if (size > MAX_BODY_BYTES) {
        reject(new IntakeError('request body exceeds maximum size'));
        req.destroy();
        return;
      }
      body += chunk;
    });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') {
    sendJson(res, 200, { ok: true });
    return;
  }

  if (req.method === 'GET' && req.url === '/health') {
    sendJson(res, 200, {
      ok: true,
      service: 'admissibility_wiki_proposal_intake_api',
      durable_write: 'repo_local_filesystem',
      decision_authority: false
    });
    return;
  }

  if (req.method !== 'POST' || req.url !== '/api/wiki/proposals/intake') {
    sendJson(res, 404, {
      error: 'not_found',
      expected: 'POST /api/wiki/proposals/intake'
    });
    return;
  }

  try {
    const rawText = await readBody(req);
    const submission = JSON.parse(rawText);
    const result = intakeSubmission({
      submission,
      rawText,
      outputRoot: OUTPUT_ROOT
    });

    sendJson(res, 201, {
      receipt: result.receipt,
      queue_result: result.queue_result,
      artifact_paths: {
        candidate_path: result.candidate_path,
        receipt_path: result.receipt_path,
        queue_path: result.queue_path,
        index_path: result.index_path
      },
      non_claims: result.non_claims
    });
  } catch (error) {
    const message = error instanceof SyntaxError ? 'invalid JSON body' : error.message;
    sendJson(res, 400, {
      error: 'intake_rejected',
      message,
      non_claims: [
        'Rejected intake does not create a proposal decision.',
        'Rejected intake does not create equivalent-term standing.',
        'Rejected intake does not prove or disprove the submitted claim.'
      ]
    });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`proposal intake API listening on http://${HOST}:${PORT}`);
});
