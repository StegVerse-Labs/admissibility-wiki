#!/usr/bin/env node
import fs from 'node:fs';

const DOCKERFILE = 'Dockerfile.intake-api';
const RENDER_BLUEPRINT = 'render.intake-api.yaml';

const dockerMarkers = [
  'FROM node:20-alpine',
  'WORKDIR /app',
  'COPY scripts ./scripts',
  'HOST=0.0.0.0',
  'PORT=8787',
  'INTAKE_OUTPUT_ROOT=static/governance/intake',
  'MAX_BODY_BYTES=256000',
  'EXPOSE 8787',
  'scripts/proposal-intake-api-server.mjs'
];

const renderMarkers = [
  'name: admissibility-wiki-intake-api',
  'runtime: docker',
  'dockerfilePath: ./Dockerfile.intake-api',
  'autoDeploy: false',
  'healthCheckPath: /health',
  'HOST',
  '0.0.0.0',
  'PORT',
  '8787',
  'INTAKE_OUTPUT_ROOT',
  'static/governance/intake',
  'MAX_BODY_BYTES',
  '256000'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function assertMarkers(path, markers) {
  if (!fs.existsSync(path)) {
    fail(`missing file: ${path}`);
  }
  const text = fs.readFileSync(path, 'utf8');
  for (const marker of markers) {
    if (!text.includes(marker)) {
      fail(`${path} missing marker: ${marker}`);
    }
  }
}

assertMarkers(DOCKERFILE, dockerMarkers);
assertMarkers(RENDER_BLUEPRINT, renderMarkers);

console.log(`OK: ${DOCKERFILE}`);
console.log(`OK: ${RENDER_BLUEPRINT}`);
console.log('intake_api_deploy_config=installed');
