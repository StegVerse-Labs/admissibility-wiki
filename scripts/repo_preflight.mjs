#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const findings = [];

function add(level, category, message, filePath = undefined) {
  const item = { class: level, category, message };
  if (filePath) item.path = filePath;
  findings.push(item);
}

function exists(filePath) {
  return fs.existsSync(path.join(root, filePath));
}

function read(filePath) {
  return fs.readFileSync(path.join(root, filePath), 'utf8');
}

function json(filePath) {
  return JSON.parse(read(filePath));
}

function workflowFiles() {
  const dir = path.join(root, '.github', 'workflows');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter((name) => name.endsWith('.yml') || name.endsWith('.yaml')).sort();
}

function checkHandoffs() {
  const handoff = 'docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md';
  const siteHandoff = 'docs/SITE_MIRROR_HANDOFF.md';
  if (exists(handoff)) add('PASS', 'handoff_state', 'Primary mirror handoff exists.', handoff);
  else add('FAIL', 'handoff_state', 'Primary mirror handoff is missing.', handoff);
  if (exists(siteHandoff)) add('PASS', 'handoff_state', 'Site mirror handoff exists.', siteHandoff);
  else add('WARN', 'handoff_state', 'Site mirror handoff is missing.', siteHandoff);
}

function checkWorkflows() {
  const workflows = workflowFiles();
  if (workflows.length <= 1) add('PASS', 'workflow_policy', 'Single active workflow policy is satisfied.');
  else add('FAIL', 'workflow_policy', `Workflow sprawl detected: ${workflows.join(', ')}`);
}

function checkPackageScripts() {
  if (!exists('package.json')) {
    add('FAIL', 'governance_validation', 'package.json is missing.', 'package.json');
    return;
  }
  const pkg = json('package.json');
  const scripts = pkg.scripts || {};
  for (const name of ['validate', 'build']) {
    if (scripts[name]) add('PASS', 'governance_validation', `package script exists: ${name}`, 'package.json');
    else add('FAIL', 'governance_validation', `package script missing: ${name}`, 'package.json');
  }
}

function checkStatusArtifacts() {
  const required = [
    'static/status/admissibility-wiki-status.json',
    'static/status/admissibility-wiki-activation.json',
    'static/status/repo-standards-integration-status.json'
  ];
  for (const filePath of required) {
    if (!exists(filePath)) {
      add('FAIL', 'status_artifact_state', 'Required status artifact missing.', filePath);
      continue;
    }
    try {
      json(filePath);
      add('PASS', 'status_artifact_state', 'Status artifact is valid JSON.', filePath);
    } catch (error) {
      add('FAIL', 'status_artifact_state', `Status artifact JSON invalid: ${error.message}`, filePath);
    }
  }
}

function checkGeneratedArtifactGuards() {
  const pkg = exists('package.json') ? json('package.json') : { scripts: {} };
  const scriptsText = JSON.stringify(pkg.scripts || {});
  if (scriptsText.includes('git diff --exit-code')) {
    add('WARN', 'generated_artifact_state', 'Generated-artifact clean-tree guard detected; run preflight before remote CI.', 'package.json');
  } else {
    add('PASS', 'generated_artifact_state', 'No generated-artifact clean-tree guard detected.', 'package.json');
  }
}

function checkMdxHazards() {
  const docsDir = path.join(root, 'docs');
  const hazards = [];
  function walk(dir) {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      if (entry.isFile() && (entry.name.endsWith('.md') || entry.name.endsWith('.mdx'))) {
        const rel = path.relative(root, full).replaceAll(path.sep, '/');
        const text = fs.readFileSync(full, 'utf8');
        if (text.includes('{x}') || text.includes('dot{x}') || text.includes('tilde{x}')) hazards.push(rel);
      }
    }
  }
  walk(docsDir);
  if (hazards.length) add('WARN', 'render_build', `Potential MDX math-expression hazards: ${hazards.join(', ')}`);
  else add('PASS', 'render_build', 'No known simple MDX math-expression hazards found.');
}

checkHandoffs();
checkWorkflows();
checkPackageScripts();
checkStatusArtifacts();
checkGeneratedArtifactGuards();
checkMdxHazards();

const summary = { pass: 0, warn: 0, fail: 0, skip: 0 };
for (const item of findings) summary[item.class.toLowerCase()] += 1;
const status = summary.fail ? 'FAIL' : summary.warn ? 'WARN' : 'PASS';
const report = {
  schema: 'stegverse_repo_preflight_status.v0.1',
  repository: 'StegVerse-Labs/admissibility-wiki',
  status,
  checked_at: new Date().toISOString(),
  summary,
  findings,
  non_claims: [
    'Preflight does not replace release readiness.',
    'Preflight does not authorize deployment.',
    'Preflight does not prove runtime admissibility.'
  ]
};

fs.mkdirSync(path.join(root, 'static/status'), { recursive: true });
fs.writeFileSync(path.join(root, 'static/status/repo-preflight-status.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
process.exit(status === 'FAIL' ? 1 : 0);
