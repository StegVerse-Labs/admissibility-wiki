#!/usr/bin/env node
import fs from 'node:fs';

const registryPath = 'static/formalisms/formalism-registry.v0.1.json';
const graphPath = 'docs/formalisms/formalism-graph-index.md';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(registryPath)) fail(`missing registry: ${registryPath}`);
if (!fs.existsSync(graphPath)) fail(`missing graph index: ${graphPath}`);

const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
const graph = fs.readFileSync(graphPath, 'utf8');

for (const heading of ['## Purpose', '## Source Boundary', '## Current Graph Coverage', '## Non-Claims']) {
  if (!graph.includes(heading)) fail(`graph index missing heading: ${heading}`);
}

const mirrored = registry.records.filter((record) => record.state === 'mirrored');

for (const record of mirrored) {
  if (!record.name || !record.wiki_path) fail(`bad mirrored record: ${record.formalism_id}`);
  const expectedLink = `./${record.wiki_path.replace('docs/formalisms/', '')}`;
  if (!graph.includes(expectedLink)) fail(`graph index missing link for ${record.name}: ${expectedLink}`);
  if (!graph.includes(record.source_authority)) fail(`graph index missing source authority for ${record.name}`);
}

for (const required of [
  'does not define any formalism',
  'does not prove any formalism',
  'does not validate any formalism',
  'does not expose private source content'
]) {
  if (!graph.includes(required)) fail(`graph index missing non-claim: ${required}`);
}

console.log(`OK: graph index mirrored records=${mirrored.length}`);
