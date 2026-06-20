#!/usr/bin/env node
import fs from 'node:fs';
import https from 'node:https';

const MANIFEST_PATH = 'static/sync/formalism-source-sync.v0.1.json';
const OUTPUT_DIR = '.sync-output';
const OUTPUT_PATH = `${OUTPUT_DIR}/public-formalism-source-refs.json`;
const REPORT_PATH = `${OUTPUT_DIR}/public-formalism-source-refs.md`;

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    const request = https.get(url, {
      headers: {
        'User-Agent': 'admissibility-wiki-formalism-source-sync',
        'Accept': 'application/vnd.github+json'
      }
    }, (response) => {
      let body = '';
      response.on('data', (chunk) => {
        body += chunk;
      });
      response.on('end', () => {
        if (response.statusCode < 200 || response.statusCode >= 300) {
          reject(new Error(`GET ${url} failed with ${response.statusCode}: ${body.slice(0, 300)}`));
          return;
        }
        try {
          resolve(JSON.parse(body));
        } catch (error) {
          reject(error);
        }
      });
    });
    request.on('error', reject);
    request.setTimeout(15000, () => {
      request.destroy(new Error(`timeout fetching ${url}`));
    });
  });
}

if (!fs.existsSync(MANIFEST_PATH)) {
  fail(`missing manifest: ${MANIFEST_PATH}`);
}

const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const records = [];

for (const source of manifest.sources) {
  if (source.canonical_source_visibility !== 'public') {
    records.push({
      source_id: source.source_id,
      formalism_term: source.formalism_term,
      canonical_source_repository: source.canonical_source_repository,
      fetch_status: 'skipped_private_or_nonpublic',
      current_source_ref: null,
      default_branch: null,
      non_claims: ['Private or non-public sources are not fetched by the public sync workflow.']
    });
    continue;
  }

  const [owner, repo] = source.canonical_source_repository.split('/');
  if (!owner || !repo) {
    records.push({
      source_id: source.source_id,
      formalism_term: source.formalism_term,
      canonical_source_repository: source.canonical_source_repository,
      fetch_status: 'invalid_repository_name',
      current_source_ref: null,
      default_branch: null,
      non_claims: ['Invalid repository name prevents source-ref fetch.']
    });
    continue;
  }

  try {
    const repoInfo = await getJson(`https://api.github.com/repos/${owner}/${repo}`);
    const branch = repoInfo.default_branch || 'main';
    const branchInfo = await getJson(`https://api.github.com/repos/${owner}/${repo}/branches/${branch}`);
    records.push({
      source_id: source.source_id,
      formalism_term: source.formalism_term,
      canonical_source_repository: source.canonical_source_repository,
      fetch_status: 'ok',
      current_source_ref: branchInfo.commit?.sha || null,
      default_branch: branch,
      non_claims: ['Fetched source ref does not prove or validate the formalism.']
    });
  } catch (error) {
    records.push({
      source_id: source.source_id,
      formalism_term: source.formalism_term,
      canonical_source_repository: source.canonical_source_repository,
      fetch_status: 'fetch_failed',
      current_source_ref: null,
      default_branch: null,
      error: error.message,
      non_claims: ['Failed fetch does not imply source absence or invalidity.']
    });
  }
}

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify({
  schema: 'admissibility_wiki_public_formalism_source_refs.v0.1',
  authority_boundary: manifest.authority_boundary,
  records
}, null, 2)}\n`);

const lines = [];
lines.push('# Public Formalism Source Refs');
lines.push('');
lines.push('This report fetches current refs only for public canonical formalism repositories.');
lines.push('');
for (const record of records) {
  lines.push(`## ${record.formalism_term}`);
  lines.push('');
  lines.push(`- Source: \`${record.canonical_source_repository}\``);
  lines.push(`- Fetch status: \`${record.fetch_status}\``);
  lines.push(`- Default branch: \`${record.default_branch || 'none'}\``);
  lines.push(`- Current source ref: \`${record.current_source_ref || 'none'}\``);
  if (record.error) {
    lines.push(`- Error: ${record.error}`);
  }
  lines.push('');
}
fs.writeFileSync(REPORT_PATH, `${lines.join('\n')}\n`);
console.log(`public_formalism_source_ref_records=${records.length}`);
