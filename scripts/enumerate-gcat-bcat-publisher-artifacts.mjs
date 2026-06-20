#!/usr/bin/env node
import fs from 'node:fs';
import https from 'node:https';

const OWNER = 'GCAT-BCAT-Engine';
const REPO = 'Publisher';
const DIR = 'papers/GCAT-BCAT';
const OUT_DIR = '.sync-output';
const OUT_JSON = `${OUT_DIR}/gcat-bcat-publisher-artifacts.json`;
const OUT_MD = `${OUT_DIR}/gcat-bcat-publisher-artifacts.md`;

function getJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'admissibility-wiki-artifact-enumerator',
        'Accept': 'application/vnd.github+json'
      }
    }, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject(new Error(`GET ${url} failed with ${res.statusCode}: ${body.slice(0, 240)}`));
          return;
        }
        resolve(JSON.parse(body));
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => req.destroy(new Error(`timeout: ${url}`)));
  });
}

function classifyCandidate(name) {
  const lower = name.toLowerCase();
  const slots = [];
  if (lower.includes('math') || lower.includes('formal') || lower.includes('theorem')) slots.push('mathematical_candidates');
  if (lower.includes('proof') || lower.includes('lemma')) slots.push('proof_candidates');
  if (lower.includes('valid') || lower.includes('test') || lower.includes('receipt') || lower.includes('example')) slots.push('validation_candidates');
  return slots;
}

fs.mkdirSync(OUT_DIR, { recursive: true });

let contents = [];
let status = 'ok';
let error = null;

try {
  contents = await getJson(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${encodeURIComponent(DIR).replaceAll('%2F', '/')}`);
  if (!Array.isArray(contents)) contents = [contents];
} catch (err) {
  status = 'fetch_failed';
  error = err.message;
}

const artifacts = contents
  .filter((item) => item.type === 'file')
  .map((item) => ({
    name: item.name,
    path: item.path,
    url: item.html_url,
    sha: item.sha,
    size: item.size,
    candidate_slots: classifyCandidate(item.name),
    artifact_role: 'publication_artifact'
  }));

const report = {
  schema: 'admissibility_wiki_gcat_bcat_publisher_artifact_enumeration.v0.1',
  formalism_id: 'formalism.gcat-bcat',
  canonical_name: 'Governance-Centered and Boundary-Centered Admissibility Testing',
  canonical_source_repository: 'Admissible-Existence/GCAT-BCAT',
  publisher_directory: `${OWNER}/${REPO}/${DIR}`,
  status,
  error,
  artifact_count: artifacts.length,
  artifacts,
  non_claims: [
    'Enumeration does not define the formalism.',
    'Enumeration does not prove or validate the formalism.',
    'Publisher artifacts are publication evidence, not canonical source authority.'
  ]
};

fs.writeFileSync(OUT_JSON, `${JSON.stringify(report, null, 2)}\n`);

const lines = [];
lines.push('# GCAT-BCAT Publisher Artifact Enumeration');
lines.push('');
lines.push(`Status: ${status}`);
if (error) lines.push(`Error: ${error}`);
lines.push('');
lines.push(`Artifact count: ${artifacts.length}`);
lines.push('');
for (const artifact of artifacts) {
  lines.push(`- ${artifact.name}`);
  lines.push(`  - Path: ${artifact.path}`);
  lines.push(`  - URL: ${artifact.url}`);
  lines.push(`  - Candidate slots: ${artifact.candidate_slots.join(', ') || 'unclassified'}`);
}
fs.writeFileSync(OUT_MD, `${lines.join('\n')}\n`);
console.log(`gcat_bcat_publisher_artifacts=${artifacts.length}`);
