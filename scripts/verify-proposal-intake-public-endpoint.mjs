#!/usr/bin/env node
import fs from 'node:fs';

const endpoint = process.argv[2];
const fixturePath = process.argv[3] || 'fixtures/intake/submission.valid.example.json';
const outPath = process.argv[4] || 'static/status/proposal-intake-api-deployment-receipt.observed.json';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function ensureHttps(url) {
  if (!url.startsWith('https://') && !url.startsWith('http://127.0.0.1:') && !url.startsWith('http://localhost:')) {
    fail('endpoint must be HTTPS unless verifying localhost');
  }
}

if (!endpoint) {
  fail('usage: node scripts/verify-proposal-intake-public-endpoint.mjs <endpoint-url> [fixture-path] [receipt-output-path]');
}
ensureHttps(endpoint);

if (!fs.existsSync(fixturePath)) {
  fail(`missing fixture: ${fixturePath}`);
}

const generatedAt = new Date().toISOString();
const checks = [];

async function recordCheck(checkId, fn) {
  try {
    const evidence = await fn();
    checks.push({ check_id: checkId, status: 'passed', evidence });
  } catch (error) {
    checks.push({ check_id: checkId, status: 'failed', evidence: { message: error.message } });
  }
}

const baseUrl = endpoint.replace(/\/api\/wiki\/proposals\/intake\/?$/, '');
const healthUrl = `${baseUrl}/health`;

await recordCheck('runtime_health_check', async () => {
  const response = await fetch(healthUrl);
  const body = await response.json();
  if (!response.ok || body.ok !== true) {
    throw new Error(`health check failed with status ${response.status}`);
  }
  return { url: healthUrl, status: response.status, service: body.service };
});

let validResponseBody = null;
await recordCheck('valid_manifest_submission', async () => {
  const fixture = fs.readFileSync(fixturePath, 'utf8');
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: fixture
  });
  validResponseBody = await response.json();
  if (response.status !== 201) {
    throw new Error(`expected 201, got ${response.status}`);
  }
  if (!validResponseBody.receipt || validResponseBody.receipt.schema !== 'admissibility_wiki_submission_receipt.v1') {
    throw new Error('missing valid receipt in response');
  }
  if (!validResponseBody.queue_result || validResponseBody.queue_result.queued !== true) {
    throw new Error('missing queued result in response');
  }
  return {
    status: response.status,
    receipt_id: validResponseBody.receipt.receipt_id,
    proposal_id: validResponseBody.receipt.proposal_id,
    queue_id: validResponseBody.queue_result.queue_id
  };
});

await recordCheck('receipt_non_claims_present', async () => {
  if (!validResponseBody?.receipt?.non_claims?.includes('Receipt does not accept the proposal.')) {
    throw new Error('receipt non-claim missing');
  }
  return { present: true };
});

await recordCheck('queue_result_present', async () => {
  if (!validResponseBody?.queue_result?.queued) {
    throw new Error('queue result missing');
  }
  return validResponseBody.queue_result;
});

await recordCheck('malformed_json_rejected', async () => {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: '{bad json'
  });
  const body = await response.json();
  if (response.status !== 400) {
    throw new Error(`expected 400, got ${response.status}`);
  }
  if (body.error !== 'intake_rejected') {
    throw new Error('expected intake_rejected error');
  }
  return { status: response.status, error: body.error };
});

const allPassed = checks.every((check) => check.status === 'passed');
const receipt = {
  schema: 'admissibility_wiki_proposal_intake_api_deployment_receipt.v1',
  receipt_id: `proposal-intake-api-deployment.${allPassed ? 'observed_pass' : 'observed_fail'}.${Date.now()}`,
  generated_at: generatedAt,
  repository: 'StegVerse-Labs/admissibility-wiki',
  deployment_state: allPassed ? 'verified_external_runtime' : 'verification_failed',
  local_api_status: 'installed_and_validated',
  public_endpoint_status: allPassed ? 'verified' : 'not_verified',
  endpoint,
  checks,
  non_claims: [
    'This deployment receipt does not accept any proposal.',
    'This deployment receipt does not create decision authority.',
    'This deployment receipt does not install automatic AI review or decision publication.'
  ]
};

fs.writeFileSync(outPath, `${JSON.stringify(receipt, null, 2)}\n`);

console.log(JSON.stringify({
  outPath,
  public_endpoint_status: receipt.public_endpoint_status,
  deployment_state: receipt.deployment_state,
  checks: checks.length
}, null, 2));

if (!allPassed) {
  process.exit(1);
}
