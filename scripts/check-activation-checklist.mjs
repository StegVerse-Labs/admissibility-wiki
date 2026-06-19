#!/usr/bin/env node
import fs from 'node:fs';

const CHECKLIST_PATH = 'static/status/admissibility-wiki-activation.json';
const EXPECTED_URL = 'https://stegverse-labs.github.io/admissibility-wiki/';

const requiredTopLevel = [
  'schema',
  'generated_at',
  'repository',
  'target_url',
  'hosting_mode',
  'custom_domain',
  'required_repository_configuration',
  'activation_checks',
  'known_404_causes',
  'current_next_action'
];

const requiredRepoConfig = [
  'docusaurus_url',
  'docusaurus_baseUrl',
  'github_pages_source',
  'deploy_workflow',
  'build_output',
  'deploy_gate'
];

const requiredCheckIds = [
  'pages_source_github_actions',
  'aggregate_validation_success',
  'deploy_workflow_success',
  'root_url_loads',
  'glossary_route_loads',
  'status_json_loads',
  'ontology_json_loads',
  'example_proposal_loads'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function requireObject(value, name) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    fail(`${name} must be an object`);
  }
}

function requireArray(value, name) {
  if (!Array.isArray(value)) {
    fail(`${name} must be an array`);
  }
}

if (!fs.existsSync(CHECKLIST_PATH)) {
  fail(`missing activation checklist: ${CHECKLIST_PATH}`);
}

const checklist = JSON.parse(fs.readFileSync(CHECKLIST_PATH, 'utf8'));

for (const field of requiredTopLevel) {
  if (!(field in checklist)) {
    fail(`missing top-level field: ${field}`);
  }
}

if (checklist.schema !== 'admissibility_wiki_activation.v1') {
  fail('unexpected schema');
}

if (checklist.repository !== 'StegVerse-Labs/admissibility-wiki') {
  fail('repository must be StegVerse-Labs/admissibility-wiki');
}

if (checklist.target_url !== EXPECTED_URL) {
  fail(`target_url must be ${EXPECTED_URL}`);
}

if (checklist.hosting_mode !== 'github_pages_project_site') {
  fail('hosting_mode must be github_pages_project_site');
}

requireObject(checklist.custom_domain, 'custom_domain');
if (checklist.custom_domain.configured !== false) {
  fail('custom_domain.configured must remain false for GitHub.io activation');
}
if (checklist.custom_domain.cname_file_expected !== false) {
  fail('custom_domain.cname_file_expected must remain false');
}

requireObject(checklist.required_repository_configuration, 'required_repository_configuration');
for (const field of requiredRepoConfig) {
  if (!(field in checklist.required_repository_configuration)) {
    fail(`missing required_repository_configuration field: ${field}`);
  }
}

if (checklist.required_repository_configuration.docusaurus_url !== 'https://stegverse-labs.github.io') {
  fail('unexpected docusaurus_url');
}
if (checklist.required_repository_configuration.docusaurus_baseUrl !== '/admissibility-wiki/') {
  fail('unexpected docusaurus_baseUrl');
}
if (checklist.required_repository_configuration.github_pages_source !== 'GitHub Actions') {
  fail('github_pages_source must be GitHub Actions');
}
if (checklist.required_repository_configuration.deploy_workflow !== '.github/workflows/deploy.yml') {
  fail('deploy_workflow must be .github/workflows/deploy.yml');
}
if (checklist.required_repository_configuration.deploy_gate !== 'npm run validate') {
  fail('deploy_gate must be npm run validate');
}

requireArray(checklist.activation_checks, 'activation_checks');
const ids = new Set(checklist.activation_checks.map((check) => check.check_id));
for (const id of requiredCheckIds) {
  if (!ids.has(id)) {
    fail(`missing activation check: ${id}`);
  }
}

for (const check of checklist.activation_checks) {
  if (!check.check_id || typeof check.check_id !== 'string') {
    fail('each activation check must have check_id');
  }
  if (!check.description || typeof check.description !== 'string') {
    fail(`activation check ${check.check_id} must have description`);
  }
  if (!check.status || typeof check.status !== 'string') {
    fail(`activation check ${check.check_id} must have status`);
  }
  if (typeof check.blocking !== 'boolean') {
    fail(`activation check ${check.check_id} must have boolean blocking`);
  }
}

requireArray(checklist.known_404_causes, 'known_404_causes');
if (checklist.known_404_causes.length === 0) {
  fail('known_404_causes must not be empty');
}

const causes = checklist.known_404_causes.join('\n');
if (!causes.includes('aggregate validation')) {
  fail('known_404_causes must mention aggregate validation failures');
}

console.log(`OK: ${CHECKLIST_PATH}`);
console.log(`checks=${checklist.activation_checks.length}`);
console.log(`target_url=${checklist.target_url}`);
console.log(`deploy_gate=${checklist.required_repository_configuration.deploy_gate}`);
