#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const SERVER_PATH = 'scripts/proposal-intake-api-server.mjs';
const FIXTURE_PATH = 'fixtures/intake/submission.valid.example.json';
const PORT = 8799;

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForHealth() {
  for (let i = 0; i < 30; i += 1) {
    try {
      const response = await fetch(`http://127.0.0.1:${PORT}/health`);
      if (response.ok) return;
    } catch (_) {
      await wait(100);
    }
  }
  fail('API server did not become healthy');
}

if (!fs.existsSync(SERVER_PATH)) {
  fail(`missing API server: ${SERVER_PATH}`);
}
if (!fs.existsSync(FIXTURE_PATH)) {
  fail(`missing fixture: ${FIXTURE_PATH}`);
}

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'admissibility-intake-api-'));
const outputRoot = path.join(tmpRoot, 'intake-output');
const server = spawn('node', [SERVER_PATH], {
  cwd: process.cwd(),
  env: {
    ...process.env,
    PORT: String(PORT),
    HOST: '127.0.0.1',
    INTAKE_OUTPUT_ROOT: outputRoot
  },
  stdio: ['ignore', 'pipe', 'pipe']
});

let stderr = '';
server.stderr.on('data', (chunk) => {
  stderr += chunk.toString();
});

try {
  await waitForHealth();

  const fixture = fs.readFileSync(FIXTURE_PATH, 'utf8');
  const response = await fetch(`http://127.0.0.1:${PORT}/api/wiki/proposals/intake`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: fixture
  });

  if (response.status !== 201) {
    const body = await response.text();
    fail(`expected 201 from intake endpoint, got ${response.status}: ${body}`);
  }

  const body = await response.json();
  if (!body.receipt || body.receipt.schema !== 'admissibility_wiki_submission_receipt.v1') {
    fail('response missing valid receipt');
  }
  if (!body.queue_result || body.queue_result.queued !== true) {
    fail('response missing queued result');
  }
  if (!body.artifact_paths) {
    fail('response missing artifact paths');
  }
  for (const filePath of Object.values(body.artifact_paths)) {
    if (!fs.existsSync(filePath)) {
      fail(`expected durable artifact missing: ${filePath}`);
    }
  }

  const badResponse = await fetch(`http://127.0.0.1:${PORT}/api/wiki/proposals/intake`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: '{bad json'
  });
  if (badResponse.status !== 400) {
    fail(`expected 400 for malformed JSON, got ${badResponse.status}`);
  }

  console.log('OK: proposal intake API server');
  console.log(`receipt_id=${body.receipt.receipt_id}`);
  console.log(`queue_id=${body.queue_result.queue_id}`);
} finally {
  server.kill('SIGTERM');
  fs.rmSync(tmpRoot, { recursive: true, force: true });
  if (stderr.trim()) {
    console.error(stderr.trim());
  }
}
