#!/usr/bin/env node
import fs from 'node:fs';

const path = 'static/publication/publication-verification-status.v0.1.json';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(path)) fail(`missing ${path}`);

const status = JSON.parse(fs.readFileSync(path, 'utf8'));

for (const field of [
  'schema',
  'repository',
  'latest_checked_commit',
  'commit_status_result',
  'public_visibility_status',
  'required_distinction',
  'publication_paths',
  'next_actions',
  'non_claims'
]) {
  if (!(field in status)) fail(`missing ${field}`);
}

if (status.schema !== 'admissibility_wiki_publication_verification_status.v0.1') fail('bad schema');
if (status.repository !== 'StegVerse-Labs/admissibility-wiki') fail('bad repository');
if (status.public_visibility_status !== 'unverified' && status.public_visibility_status !== 'verified') fail('bad public_visibility_status');
if (!Array.isArray(status.publication_paths) || status.publication_paths.length === 0) fail('publication_paths must not be empty');
if (!Array.isArray(status.next_actions) || status.next_actions.length === 0) fail('next_actions must not be empty');
if (!Array.isArray(status.non_claims) || status.non_claims.length === 0) fail('non_claims must not be empty');

console.log('OK: publication verification status');
