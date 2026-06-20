#!/usr/bin/env node
import fs from 'node:fs';
import https from 'node:https';

const STATUS_PATH = 'static/publication/publication-verification-status.v0.1.json';
const URLS = [
  'https://stegverse-labs.github.io/admissibility-wiki/',
  'https://stegverse-labs.github.io/admissibility-wiki/formalisms/governance-centered-boundary-centered-admissibility-testing'
];

function checkUrl(url) {
  return new Promise((resolve) => {
    const request = https.get(url, { headers: { 'User-Agent': 'admissibility-wiki-public-verifier' } }, (response) => {
      response.resume();
      resolve({ url, status_code: response.statusCode, ok: response.statusCode >= 200 && response.statusCode < 400 });
    });
    request.on('error', (error) => resolve({ url, status_code: null, ok: false, error: error.message }));
    request.setTimeout(15000, () => {
      request.destroy();
      resolve({ url, status_code: null, ok: false, error: 'timeout' });
    });
  });
}

if (!fs.existsSync(STATUS_PATH)) {
  console.error(`missing ${STATUS_PATH}`);
  process.exit(1);
}

const status = JSON.parse(fs.readFileSync(STATUS_PATH, 'utf8'));
const results = [];
for (const url of URLS) results.push(await checkUrl(url));

const allOk = results.every((item) => item.ok);
status.public_visibility_status = allOk ? 'verified' : 'unverified';
status.latest_public_url_check = {
  checked_at: new Date().toISOString(),
  results,
  all_ok: allOk
};
status.commit_status_result = allOk ? 'public_urls_reachable' : status.commit_status_result;
status.meaning = allOk
  ? 'Configured public Pages URLs are reachable from the verifier.'
  : 'One or more configured public Pages URLs are not reachable from the verifier.';

fs.writeFileSync(STATUS_PATH, `${JSON.stringify(status, null, 2)}\n`);
console.log(`public_pages_verified=${allOk}`);
