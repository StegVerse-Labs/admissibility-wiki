import fs from 'node:fs';

const docPath = 'docs/stegverse/entity-sandbox-runner-admissibility-plane.md';
const statusPath = 'static/status/entity-sandbox-runner-admissibility-plane-status.json';
const errors = [];

function requireFile(path) {
  if (!fs.existsSync(path)) errors.push('missing:' + path);
}

requireFile(docPath);
requireFile(statusPath);

if (fs.existsSync(docPath)) {
  const doc = fs.readFileSync(docPath, 'utf8');
  for (const token of ['StegGhost/entity-sandbox-runner', 'admissibility_plane_activation_candidate', 'CGE route fingerprint', 'transition receipt emission', 'It does not issue commit-time permission']) {
    if (!doc.includes(token)) errors.push('missing_doc_token:' + token);
  }
}

if (fs.existsSync(statusPath)) {
  const status = JSON.parse(fs.readFileSync(statusPath, 'utf8'));
  if (status.source_repo !== 'StegGhost/entity-sandbox-runner') errors.push('source_repo_mismatch');
  if (status.release_goal !== 'admissibility_plane_activation_candidate') errors.push('release_goal_mismatch');
  if (status.wiki_status !== 'documentation_surface_installed') errors.push('wiki_status_mismatch');
  if (status.activation_state !== 'pending_external_evidence') errors.push('activation_state_mismatch');
}

if (errors.length) {
  throw new Error(JSON.stringify({ status: 'failed', errors }));
}

console.log(JSON.stringify({ status: 'ok', checked: [docPath, statusPath] }, null, 2));
